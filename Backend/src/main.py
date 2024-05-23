from fastapi import FastAPI, Form, UploadFile, File
import uvicorn
from src.Extractor import extract
import uuid
import os
from fastapi.staticfiles import StaticFiles
#http://127.0.0.1:8000/static/upload_form.html
app = FastAPI()

# Mount the directory containing static files (e.g., HTML files)
app.mount("/static", StaticFiles(directory="D:\DS\AZURE\OSR\Data_Extraction_Healthcare_Project\Backend\src"), name="static")

@app.post('/extract_text')
async def extract_text(
        file_type: str = Form(...),
        file: UploadFile = File(...)
):

    content = file.file.read()
    file_path = "../Uploads"+str(uuid.uuid4())+".pdf"
    with open(file_path, "wb") as f:
        f.write(content)

    try:
        data = extract(file_path, file_type)
    except Exception as e:
        data = {
            'error': str(e)
        }

    if os.path.exists(file_path):
        os.remove(file_path)

    return data

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)