import pathlib
import io
import uuid
from fastapi import (
    FastAPI,
    Request,
    File,
    UploadFile,
    HTTPException
)
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from PIL import Image

BASE_DIR = pathlib.Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploaded"

app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
def home_view(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/")
def home_detail_view(request: Request):
    return {"message": "success"}


@app.post("/img-echo", response_class=FileResponse)
async def img_echo_view(file: UploadFile = File(...)):
    UPLOAD_DIR.mkdir(exist_ok=True)
    bytes_str = io.BytesIO(await file.read())
    try:
        img = Image.open(bytes_str)
    except:
        raise HTTPException(detail="Invalid image", status_code=400)
    fname = pathlib.Path(file.filename)
    fext = fname.suffix
    dest = UPLOAD_DIR / f"{uuid.uuid1()}{fext}"
    # with open(str(dest), 'wb') as out:
    #     out.write(bytes_str.read())
    img.save(dest)

    return dest
