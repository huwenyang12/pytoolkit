# 截图封装


from pathlib import Path
from datetime import datetime
from PIL import ImageGrab


def capture(output_dir="screenshots"):
    output_dir = Path(__file__).resolve().parent/output_dir
    output_dir.mkdir(exist_ok=True)

    path = output_dir/(datetime.now().strftime("%Y%m%d_%H%M%S")+".png")
    ImageGrab.grab().save(path)
    return str(path)