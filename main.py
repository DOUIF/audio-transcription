# coding=utf-8
import os
from datetime import datetime
from pathlib import Path

import aiofiles
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from service import transcribe_audio

app = FastAPI()

templates = Jinja2Templates(directory="templates")

upload_dir = "uploads"
os.makedirs(upload_dir, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/upload")
async def upload_file(file: UploadFile = File(...), validation: str = Form(...)):
    if not validation or not validation.strip():
        raise HTTPException(status_code=400, detail="Validation text is required")

    if validation != os.getenv("SECRET_KEY"):
        raise HTTPException(status_code=401, detail="Validation text is incorrect")

    audio_path = await __get_upload_file(file)
    transcription_path = await transcribe_audio(audio_path)
    return FileResponse(
        transcription_path,
        media_type='text/plain',
        filename=transcription_path.name,
    )


async def __get_upload_file(file: UploadFile) -> Path:
    file_path = Path(upload_dir, f"{datetime.now().strftime('%FT%H%M%S')}_{file.filename}")

    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    return file_path
