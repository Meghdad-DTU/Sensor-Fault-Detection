from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from uvicorn import run as app_run

from sensorFaultDetection.utils import read_yaml
from sensorFaultDetection.pipeline.training_pipeline import TrainingPipeline
from sensorFaultDetection.pipeline.prediction_pipeline import PredictionPipeline

try:
    params = read_yaml('params.yaml')    
    APP_HOST = params.APP_HOST
    APP_PORT = params.APP_PORT
except Exception as e:
    raise e



app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def trainRouteClient():
    try:       
        training_pipeline = TrainingPipeline()             
        if training_pipeline.is_pipeline_running:
            return Response('Training pipeline is already running!')

        training_pipeline.run_pipeline()

        return Response("Training successful!!")

    except Exception as e:
        return Response(f"Error Occurred! {e}")




@app.get("/predict")
async def predictRouteClient():    

    try:  
        df = None

        prediction_pipeline = PredictionPipeline(df)

        prediction_pipeline.predict()

        return Response(
            "Prediction successful and predictions are stored in s3 bucket !!"
        )

    except Exception as e:
        return Response(f"Error Occurred! {e}")


if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)