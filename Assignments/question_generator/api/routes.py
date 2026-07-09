from fastapi import APIRouter
from fastapi import UploadFile, File, HTTPException
from services.vedio_service import VedioService

router=APIRouter()      #APIRouter(prefix="/api", tags="["Vedio"])

@router.get("/health")
def health():
    return{
        "status":"Healthy"
    }

@router.post("/upload_vedio")
async def upload_vedio(file:UploadFile=File(...)):
    try:
        response= VedioService.save_vedio(file)
        return{
            "status":"success",
            "data": response
        }
    except HTTPException as e :
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )