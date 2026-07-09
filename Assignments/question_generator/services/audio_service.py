import os
import subprocess

from config import AUDIO_DIR

class AudioService:
    @staticmethod
    def extract_audio(vedio_path:str) -> str:
        file_name=os.path.splitext(os.path.basename(vedio_path))[0]
        audio_path=os.path.join(
            AUDIO_DIR,
            f"{file_name}.wav"
        )

        command=[
            "ffmpeg",
            "-i", vedio_path,
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            "-y",
            audio_path
        ]
        
        try:
            subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return audio_path
        except subprocess.CalledProcessError as e:
            raise Exception(
                f"FFmpeg Error : \n{e.stderr.decode()}"
            )