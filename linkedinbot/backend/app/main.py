# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from .routers.apply import router as apply_router

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router BEFORE mounting static files
app.include_router(apply_router)

# Mount static files (CSS, JS, images, etc.)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Serve the main HTML file at root
@app.get("/")
async def read_root():
    return FileResponse("frontend/index.html")

@app.get("/job-apply")
async def job_apply_page():
    return FileResponse("frontend/job_apply.html")

@app.get("/cv_scrape.html")
async def cv_scrape_page():
    return FileResponse("frontend/cv_scrape.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)