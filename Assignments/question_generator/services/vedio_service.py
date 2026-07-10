import os
import uuid
import shutil

from fastapi import UploadFile, HTTPException
from config import UPLOAD_DIR

from services.audio_service import AudioService

class VedioService:
    Allowed_Extensions={
        ".mp4",
        ".mov",
        ".avi",
        ".mkv"
    }
    @staticmethod
    def save_vedio(file:UploadFile):
        extension=os.path.splitext(file.filename)[1].lower()
        if extension not in VedioService.Allowed_Extensions:
            raise HTTPException(
                status_code=400,
                detail="unsupported vedio format."
            )
        
        vedio_id=str(uuid.uuid4())
        filename=f"{vedio_id}{extension}"
        filepath=os.path.join(
            UPLOAD_DIR,filename
        )
        with open (filepath,"wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        return filepath