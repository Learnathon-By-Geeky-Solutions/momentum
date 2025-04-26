from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import uuid
import http.client
import json
import os
import random
from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema
from app.database import get_db
from app import models, schemas
from app.utils import get_current_user, conf
from sslcommerz_lib import SSLCOMMERZ

load_dotenv()
router = APIRouter()


def send_sms(to: str, text: str):
    try:
        conn = http.client.HTTPSConnection(os.getenv("INFOBIP_BASE_URL"))
        payload = json.dumps(
            {
                "messages": [
                    {
                        "destinations": [{"to": to}],
                        "from": os.getenv("INFOBIP_SENDER"),
                        "text": text,
                    }
                ]
            }
        )
        headers = {
            "Authorization": f'App {os.getenv("INFOBIP_API_KEY")}',
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        conn.request("POST", "/sms/2/text/advanced", payload, headers)
        res = conn.getresponse()
        response_data = res.read()
        print(f"SMS sent to {to}: {response_data}")
    except Exception as e:
        print(f"SMS sending failed: {e}")


async def send_email(to: str, subject: str, body: str):
    message = MessageSchema(subject=subject, recipients=[to], body=body, subtype="html")
    fm = FastMail(conf)
    await fm.send_message(message)


@router.post("/initiate-payment")
def initiate_payment(
    request: Request,
    paybill_data: schemas.PayBillRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    bill = (
        db.query(models.Bill)
        .filter(models.Bill.order_id == paybill_data.order_id)
        .first()
    )

    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    if bill.status == "Confirmed":
        return {"message": "Bill payment already cleared."}
    is_sandbox = os.getenv("SSLCOMMERZ_IS_SANDBOX", "True").lower() == "true"

    sslcz = SSLCOMMERZ(
        {
            "store_id": os.getenv("SSLCOMMERZ_STORE_ID"),
            "store_pass": os.getenv("SSLCOMMERZ_STORE_PASS"),
            "issandbox": is_sandbox,
        }
    )

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    random_suffix = random.randint(1000, 9999)
    unique_tran_id = f"ORDER_{bill.order_id}_{timestamp}{random_suffix}"

    post_body = {
        "total_amount": str(bill.amount),
        "currency": "BDT",
        "tran_id": unique_tran_id,
        "success_url": f"{request.base_url}ssl-success",
        "fail_url": f"{request.base_url}ssl-fail",
        "cancel_url": f"{request.base_url}ssl-cancel",
        "emi_option": 0,
        "cus_name": current_user.username,
        "cus_email": current_user.email,
        "cus_phone": current_user.phone or "01711111111",
        "cus_add1": current_user.address or "N/A",
        "cus_city": "Dhaka",
        "cus_country": "Bangladesh",
        "shipping_method": "NO",
        "product_name": "Order Products",
        "product_category": "Ecommerce",
        "product_profile": "general",
    }

    response = sslcz.createSession(post_body)

    if not response.get("GatewayPageURL"):
        raise HTTPException(
            status_code=500, detail="Failed to initiate SSLCommerz session"
        )

    return {"gateway_url": response["GatewayPageURL"]}


@router.post("/ssl-success")
async def ssl_success(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    tran_id = form.get("tran_id")
    card_type = form.get("card_type")

    order_id = tran_id.split("_")[1]

    bill = db.query(models.Bill).filter(models.Bill.order_id == order_id).first()
    if not bill:
        return {"message": "Bill not found"}

    bill.status = "Confirmed"
    bill.method = card_type
    db.commit()

    order = (
        db.query(models.Order).filter(models.Order.order_id == bill.order_id).first()
    )
    if not order:
        return {"message": "Order not found"}

    user = db.query(models.User).filter(models.User.user_id == order.user_id).first()
    if not user:
        return {"message": "User not found"}

    artisan = (
        db.query(models.User)
        .join(models.Brand)
        .join(models.Product)
        .join(
            models.OrderItem, models.Product.product_id == models.OrderItem.product_id
        )
        .filter(models.OrderItem.order_id == order.order_id)
        .first()
    )

    print(user)
    print(artisan)

    if user.phone:
        send_sms(
            user.phone,
            f"Dear {user.username}, your order has been confirmed. Thanks for shopping with us.",
        )
    if artisan and artisan.email:
        await send_email(
            artisan.email,
            "New Order Received",
            f"You have received a new order from {user.username}.",
        )

    return {"message": "Payment successful and notifications sent"}


@router.post("/ssl-fail")
async def ssl_fail(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    tran_id = form.get("tran_id")
    bill = (
        db.query(models.Bill)
        .filter(models.Bill.order_id == tran_id.split("_")[1])
        .first()
    )
    if bill:
        bill.status = "Failed"
        db.commit()
    return {"message": "Payment failed"}


@router.post("/ssl-cancel")
async def ssl_cancel(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    tran_id = form.get("tran_id")
    bill = (
        db.query(models.Bill)
        .filter(models.Bill.order_id == tran_id.split("_")[1])
        .first()
    )
    if bill:
        bill.status = "Cancelled"
        db.commit()
    return {"message": "Payment cancelled"}

