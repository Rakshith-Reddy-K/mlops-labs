from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from predict import predict_data


app = FastAPI()

class Message(BaseModel):
    text: str

class SpamResponse(BaseModel):
    response:str

@app.get("/", status_code=status.HTTP_200_OK)
async def health_ping():
    return {"status": "healthy"}

@app.post("/predict", response_model=SpamResponse)
async def predict_spam(spam_text: Message):
    try:
        prediction = predict_data(spam_text.text)
        return SpamResponse(response=prediction)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


    
