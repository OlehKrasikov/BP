from fastapi import FastAPI, HTTPException, UploadFile, File, Form,BackgroundTasks
from fastapi.responses import FileResponse
from PIL import Image
import numpy as np
import uuid
import os
from fastapi.middleware.cors import CORSMiddleware

import fcm

app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://51.21.181.179",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOAD_DIR = "uploads"
RESULT_DIR = "results"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

def cleanup_files(*filepaths: str):
    for path in filepaths:
        try:
            if os.path.exists(path):
                os.remove(path)
                print(f"Removed: {path}")
        except Exception as e:
            print(f"Error deleting {path}: {e}")


@app.post("/segment-image")
async def segment_image(
    background_tasks: BackgroundTasks,
    image: UploadFile = File(...),
    n_clusters: int = Form(...),
    f_coefficient: float = Form(...),
    accuracy: float = Form(...),
    maxIterations: int = Form(...),
    colorDistance: float = Form(...)
):
    file_id = str(uuid.uuid4())
    input_path = os.path.join(UPLOAD_DIR, f"{file_id}.png")
    output_path = os.path.join(RESULT_DIR, f"{file_id}_seg.png")

    with open(input_path, "wb") as f:
        f.write(await image.read())
    try:
        image = Image.open(input_path).convert("RGB")
        image.thumbnail((500,500))
        width, height = image.size
        data = np.array(image).reshape(-1, 3)
        
        coords = []
        for y in range(height):
            for x in range(width):
                coords.append([y, x])
        coords = np.array(coords)
        data = np.hstack((data, coords))

        clusters_centers, membership_matrix = fcm.fcm(n_clusters, f_coefficient, data, maxIterations, accuracy, colorDistance,height,width)
        arr = fcm.cluster_image(membership_matrix, clusters_centers.shape[0])
        arr = arr.reshape(height, width,3)
        image = Image.fromarray(arr,'RGB')
        
        image.save(output_path)

        background_tasks.add_task(cleanup_files, input_path, output_path)

        return FileResponse(output_path, media_type="image/png")
    except Exception as e:
        cleanup_files(input_path, output_path)
        raise HTTPException(status_code=500, detail=str(e))   
