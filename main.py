from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests


app = FastAPI()
app.mount("/media", StaticFiles(directory="media"), name="media")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def randomDogs(requestUser: Request):
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    if response.status_code == 200:
        data = response.json()
        image = data["message"]
        return templates.TemplateResponse(
            name="index.html",
            context={"request": requestUser, "image_url": image}
        )
        
    return HTMLResponse("<h1>Error loading dog image 😢</h1>", status_code=500)

@app.get("/dog")
async def changeDog():
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    if response.status_code == 200:
        data = response.json()
        return JSONResponse({"image_url": data["message"]})
    return JSONResponse({"error": "Could not fetch image"}, status_code=500)