from typing import List, Optional
#fastapi
from fastapi import FastAPI, Request, Form, Depends, HTTPException, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
#image and pytorch
import torch
from torchvision import transforms
import torchvision.transforms.functional as TF
from PIL import Image
import io
from starlette.responses import StreamingResponse


#applicaltion libraries
import json

#CONFIG AND HELPERS
SIZE = (224, 224)
MODEL_NAME = './app/resnet50.pt'
MODEL = torch.load(MODEL_NAME, map_location=torch.device('cpu'))
MODEL.eval()
CLASSES_FILE = './app/idx2class.json'

with open(CLASSES_FILE, 'r') as f:
    IDX2CLASS = json.load(f)


def get_prediction(inp, model=MODEL, idx2class=IDX2CLASS):
    '''Helper function to get prediction

    :param inp: reshaped image of size (224, 224)
    :param model: pytorch model to be used
    :param idx2class: dictionary that returns label based on index

    :returns: index of the predicted image
    '''
    with torch.no_grad():
        out = model(inp)
        out = out.argmax(dim=1).item()

    label = idx2class.get(str(out))
    if label:
        return label
    else:
        return 'Something strange happened during prediction, please try again'

#start the app
app = FastAPI()

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
    
    request_object_content = await files[0].read()
    img = Image.open(io.BytesIO(request_object_content)).resize(SIZE)
    
    inp = TF.to_tensor(img)
    inp.unsqueeze_(0)
    idx = get_prediction(inp=inp)

    img.save( f"./app/static/{[file.filename for file in files][0]}")

    result = {"filename": [file.filename for file in files][0],
            "picture": f"../static/{[file.filename for file in files][0]}",
            "idx": idx}

    return templates.TemplateResponse('results.html', context={"request": request, "result": result})

