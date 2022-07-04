import shutil
import time
import io
from fastapi.testclient import TestClient
from PIL import Image, ImageChops
from app.main import app, BASE_DIR, UPLOAD_DIR

client = TestClient(app)

def test_get_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_post_home():
    response = client.post("/")
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]



def test_post_img_echo():
    image_saved_path = BASE_DIR / "images"
    for path in image_saved_path.glob("*"):
        try:
            img = Image.open(path)
        except:
            img = None
        response = client.post("/img-echo", files={"file": open(path, 'rb')})
        fext = str(path.suffix).replace(".", "")
        if img is None:
            assert response.status_code == 400
        else:
            assert response.status_code == 200
            r_stream = io.BytesIO(response.content)
            echo_img = Image.open(r_stream)
            difference = ImageChops.difference(img, echo_img).getbbox()
            assert difference is None

    time.sleep(3)
    shutil.rmtree(UPLOAD_DIR)
    
    