from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from model import predict_sentiment
from prometheus_client import make_asgi_app, Counter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Create Prometheus metrics
REQUESTS = Counter('sentiment_analysis_requests_total', 'Total sentiment analysis requests')

# Create metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

class SentimentRequest(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    sentiment: int
    confidence: float

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_model=SentimentResponse)
async def predict(request: SentimentRequest):
    REQUESTS.inc()
    sentiment, confidence = predict_sentiment(request.text)
    return SentimentResponse(sentiment=sentiment, confidence=confidence)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)