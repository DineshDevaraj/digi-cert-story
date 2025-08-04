from fastapi import FastAPI, Request, Form, Cookie, Response, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Optional

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Mount static files if needed
app.mount("/static", StaticFiles(directory="static"), name="static")

source_folder = {}
scenario = ["Validate Website", "Network Management System"]
approach = ["Theoretical", "Command Line Interface", "Python"]
for i, s in enumerate(scenario):
    for j, a in enumerate(approach):
        source_folder[(s, a)] = f"track{i+1}{j+1}"


@app.get("/", response_class=HTMLResponse)
async def read_root(
    request: Request,
    page: int = Cookie(None),
    scenario: str = Cookie(None),
    approach: str = Cookie(None),
):
    page = page or 1
    if page in (1, 2):
        response = templates.TemplateResponse(f"page{page}.html", {"request": request, "page": page})
        response.set_cookie(key="page", value=page)
        return response

    folder = source_folder[(scenario, approach)]
    return templates.TemplateResponse(
        f"{folder}/page{page}.html",
        {"request": request, "page": page, "scenario": scenario, "approach": approach},
    )


@app.post("/submit-scenario-approach", response_class=HTMLResponse)
async def set_scenario_approach(
    response: Response,
    scenario: Optional[str] = Form(...),
    approach: Optional[str] = Form(...),
):
    response.set_cookie(key="scenario", value=scenario)
    response.set_cookie(key="approach", value=approach)
    response.status_code = status.HTTP_200_OK
    return response


@app.post("/next-page", response_class=HTMLResponse)
async def goto_next_page(
    response: Response,
    page: int = Cookie(...),
):
    response.set_cookie(key="page", value=page + 1)
    response.status_code = status.HTTP_200_OK
    return response


@app.post("/prev-page", response_class=HTMLResponse)
async def goto_prev_page(
    response: Response,
    page: int = Cookie(...),
):
    response.set_cookie(key="page", value=page - 1)
    response.status_code = status.HTTP_200_OK
    return response


@app.post("/restart", response_class=HTMLResponse)
async def restart(
    response: Response,
):
    response.set_cookie(key="page", value=2)
    response.delete_cookie(key="scenario")
    response.delete_cookie(key="approach")
    response.status_code = status.HTTP_200_OK
    return response


# uvicorn main:app --reload --host 0.0.0.0 --port 7071
