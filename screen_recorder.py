# 录屏封装


from pathlib import Path
from datetime import datetime
import subprocess

class ScreenRecorder:
    def __init__(self,fps=10):
        root = Path(__file__).resolve().parent
        self.ffmpeg_path = root/"bin"/"ffmpeg.exe"
        self.output_dir = root/"records"
        self.fps = fps
        self.process = None
        self.output_path = None


    def start(self):
        if not self.ffmpeg_path.exists():
            raise FileNotFoundError(f"未找到FFmpeg: {self.ffmpeg_path}")

        self.output_dir.mkdir(exist_ok=True)
        self.output_path = self.output_dir/(datetime.now().strftime("%Y%m%d_%H%M%S")+".mp4")
        self.process = subprocess.Popen(
            [
                str(self.ffmpeg_path),"-y",
                "-f","gdigrab",
                "-framerate",str(self.fps),
                "-i","desktop",
                "-c:v","libx264",
                "-preset","ultrafast",
                "-pix_fmt","yuv420p",
                str(self.output_path)
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return str(self.output_path)


    def stop(self):
        if self.process:
            self.process.communicate(input=b"q")
            self.process = None
        return str(self.output_path) if self.output_path else None
    


if __name__ == "__main__":
    recorder = ScreenRecorder()

    try:
        recorder.start()

        # 自动化代码

    finally:
        video_path = recorder.stop()