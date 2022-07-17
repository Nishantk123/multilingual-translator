from fastapi import FastAPI, File, UploadFile, Body
import csv
from io import StringIO
from googletrans import Translator
from pydantic import BaseModel
app = FastAPI()

translator = Translator()

def predict_lang_google(text):
    return translator.detect(text).lang

def translate_text(text, g_code="en-US"):
    translator = Translator()
    d = translator.translate(text, dest=g_code)
    print(d)
    return d
class Lang(BaseModel):
    lang: str

@app.post("/user")
async def write_home(lang: str = Body(..., embed=True), file: UploadFile = File(...)):
    data = []
    contents = await file.read()
    decoded = contents.decode(encoding="utf8", errors='ignore')
    buffer = StringIO(decoded)
    csvReader = csv.DictReader(buffer)
    print(csvReader)

    for rows in csvReader:     
        print(rows) 
        data.append(rows)      

    print(data)    
    buffer.close()
    filter_data = []
    translator = Translator()
    g_code="hi"
    g_code = lang
    for key in data:
        print(key)
        obj_data = {}
        key_list = list(key.keys())

        for d in key_list:
            print(d)
            obj_data[d]  = translator.translate(key.get(d), dest=g_code).text
            filter_data.append(obj_data)

        # data = translator.translate(key.get("data"), dest=g_code)
        # data1 = translator.translate(key.get("data1"),  dest=g_code)
        # obj_data["data"] = str(data.text)
        # obj_data["data1"] = str(data1.text)
        # filter_data.append(obj_data)

    # print(filter_data)

    for yo in filter_data:
        print(yo)

    # field names
    fields = ['data', 'data1']
 
    # name of csv file
    filename ="final.csv"

    #filename = "university_records.csv"
    
   # writing to csv file
    with open(filename, 'w', encoding="utf-8") as csvfile:
        # creating a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames = fields)
        
        # writing headers (field names)
        writer.writeheader()
        
        # writing data rows
        writer.writerows(filter_data)
    return filter_data
    # return{
    #     "Name": "Kashyap",
    #     "Age": 29
    # }