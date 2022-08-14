from fastapi import FastAPI, File, UploadFile, Body
import csv
from io import StringIO
from googletrans import Translator
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import io
import os
import pandas as pd
app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
translator = Translator()

def predict_lang_google(text):
    return translator.detect(text).lang

def translate_text(text, g_code="en-US"):
    translator = Translator()
    d = translator.translate(text, dest=g_code)
    return d
class Lang(BaseModel):
    lang: str

@app.post("/user")
async def write_home(lang: str = Body(..., embed=True), file: UploadFile = File(...)):
    data = []
    contents = await file.read()
    decoded = contents.decode(encoding="utf8", errors='ignore')
    buffer = StringIO(decoded)
    datacsv = csv.reader(buffer)
    translator = Translator()
    g_code = lang
    convert_data =[]
    translated_text = dict()
    index = 0
    for row in datacsv:
        yodata=[]
        for k in row:
            if k in translated_text:
                yodata.append(translated_text[k])
            else:
                try:
                    d =  translator.translate(k, dest=g_code).text
                    translated_text[k] = d
                    yodata.append(d)
                except:
                    yodata.append(d)
        index = index + 1
        print(index, yodata)
        convert_data.append(yodata)

    with open('final.csv', 'w', encoding="utf-8") as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        # write.writerow(fields)
        write.writerows(convert_data)
    stream = io.StringIO()
    filename ="final.csv"
    file_name="final"
    file_path = os.getcwd() + "/" + filename
    return FileResponse(file_path, filename=filename)

