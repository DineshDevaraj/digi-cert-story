from fastapi import FastAPI, Request, Form, Cookie
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, page: int = Cookie(None), 
                    scenario: str = Cookie(None), approach: str = Cookie(None)):
    if page is None:
        response = templates.TemplateResponse("page1.html", {"request": request})
        response.set_cookie(key="page", value=1)
        return response 

    return templates.TemplateResponse(f"page{page}.html", {
        "request": request, "scenario": scenario, "approach": approach})


@app.post("/next-page", response_class=HTMLResponse)
async def goto_next_page(request: Request, page: int = Cookie(None),
                      scenario: str = Form(...), approach: str = Form(...)):
    response = templates.TemplateResponse("result.html", {
        "request": request, "scenario": scenario, "approach": approach})
    response.set_cookie(key="scenario", value=scenario)
    response.set_cookie(key="approach", value=approach)
    response.set_cookie(key="page", value=page+1)
    return response

# uvicorn main:app --reload --host 0.0.0.0 --port 7071
