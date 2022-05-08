from typing import List, Optional
#fastapi
from fastapi import FastAPI, Request, Form, Depends, HTTPException, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
#image and pytorch
import torch
from torchvision import transforms
import torchvision.transforms.functional as TF
from PIL import Image

#CONFIG
SIZE = (224, 224)

#db
from sqlalchemy.orm import Session
# import crud, models, schemas
# from database import SessionLocal, engine

#applicaltion libraries
from datetime import date
import json

# models.Base.metadata.create_all(bind=engine)

#start the app
app = FastAPI()

# Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

#mounting static files
app.mount("/static", StaticFiles(directory="./app/static"), name="static")

#setting up the Jinja
templates = Jinja2Templates(directory="./app/templates")

@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse('main.html', context={'request': request})

@app.post("/classify/")
async def create_upload_file(request: Request, files: list[UploadFile]):
    result = {"filename": [file.filename for file in files]}
    return templates.TemplateResponse('results.html', context={"request": request, "result": result})

