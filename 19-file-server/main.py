# imports 
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
import shutil
import os

app = FastAPI()

# FLOW / PIPELINE

# 1: ensure the folder exists
UPLOAD_FOLDER = "uploads" # this is the folder that will be used to store the files
if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)


# 2: Static files setting
# http://127.0.0.1:8000/upload/<file name>
app.mount("/static", StaticFiles(directory=UPLOAD_FOLDER), name="files")

# 3: the upload route API
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename
    file_path = os.path.join(UPLOAD_FOLDER, filename) # type:ignore

    if not filename:
        raise HTTPException(status_code=400, detail="Filename is required")
    with open(file_path, "wb") as f_buffer: # "wb" is for writing binary data
        shutil.copyfileobj(file.file, f_buffer)
        # f_buffer.write(file.file.read())
    return {"Message": "File uploaded successfully", "filename": filename, "path": f"/http://127.0.0.1:8000/files/{filename}"}


# 4: the download route API
@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return {"Message": "File downloaded successfully", "filename": filename, "path": f"/http://127.0.0.1:8000/files/{filename}"}