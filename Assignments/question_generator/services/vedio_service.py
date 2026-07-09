import os
import uuid
import shutil

from fastapi import UploadFile, HTTPException
from config import UPLOAD_DIR

class VedioService:
    Allowed_Extensions={
        ".mp4",
        ".mov",
        ".avi",
        ".mkv"
    }

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
        return {
        "vedio_id":vedio_id,
            "file_name":filename,
            "file_path":filepath
        }