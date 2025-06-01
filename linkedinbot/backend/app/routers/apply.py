# post/ apply endpoint
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..services.login import LinkedInLogin

router = APIRouter(prefix="/api", tags=["authentication"])



class LoginRequest(BaseModel):
    username: str
    password: str
    action: str

@router.post("/")
async def login(request: LoginRequest):

    linkedin= LinkedInLogin()

    result = linkedin.login_with_credentials(
        linkedin_email=request.username,
        linkedin_password=request.password
    )
    # Replace with your actual authentication logic
    if result== True:
        return {
            "success": True,
            "message": "Login successful",
            "token": "your_jwt_token_here",
            "action": request.action
        }
    else:
        raise HTTPException(
            status_code=401,
            detail={"success": False, "message": "Invalid username or password"}
        )