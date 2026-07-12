from fastapi import APIRouter
from fastapi import UploadFile, File, HTTPException
from pydantic import BaseModel
from services.vedio_service import VedioService
from services.audio_service import AudioService
from services.transcription_service import TranscriptionService
from services.question_service import QuestionService

router=APIRouter()      #APIRouter(prefix="/api", tags="["Vedio"])
class WatchRequest(BaseModel):
    vedio_id:str
    watch_time:int

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
        transcript= TranscriptionService.transcribe_audio(audio_path)
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
    
@router.post("/generate_questions")
async def generate_questions(request:WatchRequest):
    try:
        transcript=TranscriptionService.load_transcript(
               f"transcripts/{request.vedio_id}.json"
        )
        watched_vedio=TranscriptionService.get_transcrpit_by_watch_time(
               transcript,
               request.watch_time
        )
        questions=QuestionService.generate_questions(watched_vedio)
        return {
               "status":"success",
               "watch_time":request.watch_time,
               "questions":questions
        }
    except Exception as e :
        raise HTTPException(status_code=500, detail=str(e))
