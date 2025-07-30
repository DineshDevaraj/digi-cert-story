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


@app.post("/next-page", response_class=HTMLResponse)
async def goto_next_page(
    request: Request,
    page: int = Cookie(None),
    form_scenario: Optional[str] = Form(None, alias="scenario"),
    form_approach: Optional[str] = Form(None, alias="approach"),
    cookie_scenario: Optional[str] = Cookie(None, alias="scenario"),
    cookie_approach: Optional[str] = Cookie(None, alias="approach"),
):
    response = templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "scenario": form_scenario or cookie_scenario,
            "approach": form_approach or cookie_approach,
        },
    )

    if form_scenario is not None and cookie_scenario is None:
        response.set_cookie(key="scenario", value=form_scenario)
    if form_approach is not None and cookie_approach is None:
        response.set_cookie(key="approach", value=form_approach)
    response.set_cookie(key="page", value=page + 1)

    return response


@app.post("/prev-page", response_class=HTMLResponse)
async def goto_prev_page(
    response: Response,
    page: int = Cookie(None),
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
