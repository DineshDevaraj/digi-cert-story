from fastapi import FastAPI, Request, Form, Cookie, Response, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(
    request: Request,
    page: int = Cookie(None),
    scenario: str = Cookie(None),
    approach: str = Cookie(None),
):
    if page is None:
        response = templates.TemplateResponse("page1.html", {"request": request, "page": 1})
        response.set_cookie(key="page", value=1)
        return response

    return templates.TemplateResponse(
        f"page{page}.html",
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
