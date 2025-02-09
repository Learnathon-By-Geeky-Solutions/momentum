



from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import SessionLocal
import models
import schemas
from utils import auth_utils  # Corrected import

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class AuthService:

    def __init__(self, db: Session):
        self.db = db

    def google_sign_in(self, code: str):
        user_info = auth_utils.get_user_info(code)  # Corrected method call
        if not user_info:
            raise HTTPException(status_code=400, detail="Invalid Google authentication")

        email = user_info.get("email")
        google_id = user_info.get("id")  # Google returns "id" instead of "google_id"
        full_name = user_info.get("name")

        db_user = self.db.query(models.User).filter(models.User.email == email).first()
        if db_user:
            if not db_user.google_id:
                db_user.google_id = google_id
                self.db.commit()
                self.db.refresh(db_user)
            return db_user

        new_user = models.User(
            google_id=google_id,
            email=email,
            full_name=full_name,
            username=None,
            password=None,
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def register_user(self, user: schemas.UserCreate):
        existing_user = self.db.query(models.User).filter(
            (models.User.email == user.email) | (models.User.username == user.username)
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=400, detail="A user with this email or username already exists"
            )

        hashed_password = auth_utils.hash_password(user.password)  # Corrected call
        new_user = models.User(
            username=user.username,
            email=user.email,
            password=hashed_password,
            full_name=user.full_name,
            address=user.address,
            phone=user.phone,
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

@app.get("/login/google")
def login_google():
    return RedirectResponse(auth_utils.get_google_auth_url())  # Corrected method call

@app.get("/auth/callback")
def google_auth_callback(code: str, db: Session = Depends(get_db)):
    return AuthService(db).google_sign_in(code)

@app.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return AuthService(db).register_user(user)













