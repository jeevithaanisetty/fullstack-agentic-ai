from fastapi import APIRouter
from fastapi import UploadFile, File, HTTPException
from services.vedio_service import VedioService
from services.audio_service import AudioService
from services.transcription_service import TranscriptionService

router=APIRouter()      #APIRouter(prefix="/api", tags="["Vedio"])

@router.get("/health")
def health():
    return{
        "status":"Healthy"
    }

@router.post("/upload_vedio")
async def upload_vedio(file:UploadFile=File(...)):
    try:
        vedio_path= VedioService.save_vedio(file)
        audio_path=AudioService.extract_audio(vedio_path)
        transcript= TranscriptionService.trancsribe_audio(audio_path)
        transcript_path=f"transcripts/{file.filename}.json"
        TranscriptionService.save_transcript(transcript,transcript_path)
        return{
            "status":"success",
            "vedio_id": file.filename,
            "message": "Transcript generated successfully"
        }
    except HTTPException as e :
            raise e
    except Exception as e:
        raise HTTPException(
                status_code=500,
                detail=str(e)
            )