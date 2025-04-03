from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import User, Product, Order
from database import get_db
from utils import verify_token, oauth2_scheme
from pydantic import BaseModel

router = APIRouter(prefix="/admin", tags=["Admin"])