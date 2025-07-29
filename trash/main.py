from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mount static files if needed
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("page1.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
async def handle_form(request: Request, scenario: str = Form(...), approach: str = Form(...)):
    # Process form data here (e.g., authentication, saving to DB, etc.)
    return templates.TemplateResponse("result.html", {
        "request": request, "scenario": scenario, "approach": approach})

# uvicorn main:app --reload --host 0.0.0.0 --port 7071
