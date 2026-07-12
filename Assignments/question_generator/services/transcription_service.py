import os
import json
import whisper

class TranscriptionService:
    model=whisper.load_model("base")

    @staticmethod
    def transcribe_audio(audio_path: str):
        result=TranscriptionService.model.transcribe(
            audio_path,
            word_timestamps=False
        )
        return result
    
    @staticmethod
    def save_transcript(result, transcript_path:str):
        os.makedirs(os.path.dirname(transcript_path),exist_ok=True)
        with open (transcript_path,"w",encoding="utf-8") as file:
            json.dump(
                result,
                file,
                indent=4,
                ensure_ascii=False
            )
        
    @staticmethod
    def load_transcript(transcript_path:str):
        with open (transcript_path,"r", encoding="utf-8")as file :
            return json.load(file)
        
    @staticmethod
    def get_transcrpit_by_watch_time(transcript,watch_time:int):
        watched=""
        for segment in transcript["segments"]:
            if segment["end"]<= watch_time:
                watched += segment["text"] + " "
        return watched.strip()

