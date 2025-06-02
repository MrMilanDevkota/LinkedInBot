# routers/apply.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.login import LinkedInLogin

router = APIRouter(prefix="/api", tags=["authentication"])

class LoginRequest(BaseModel):
    username: str
    password: str
    action: str

@router.post("/login")  # This creates the endpoint /api/login
async def login(request: LoginRequest):
    try:
        linkedin = LinkedInLogin()
        
        result = linkedin.login_with_credentials(
            linkedin_email=request.username,
            linkedin_password=request.password
        )
        
        # Check if login was successful
        if result == True:
            return {
                "success": True,
                "message": "Login successful",
                "token": "your_jwt_token_here",  # Replace with actual JWT generation
                "action": request.action
            }
        else:
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )
            
    except Exception as e:
        # Log the error for debugging
        print(f"Login error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during login"
        )