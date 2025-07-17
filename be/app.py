from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

# Load model và các công cụ
model = joblib.load("knn_model.pkl")
scaler = joblib.load("scaler.pkl")
encoders = joblib.load("encoders.pkl")
top_features = joblib.load("top_features.pkl")


# Initialize FastAPI app
app = FastAPI(
    title="Network Intrusion Detection API",
    description="API for detecting network intrusions using the KDD Cup dataset model",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictionInput(BaseModel):
    duration: int
    protocol_type: str
    service: str
    flag: str
    src_bytes: int
    dst_bytes: int
    land: int
    wrong_fragment: int
    urgent: int
    hot: int
    num_failed_logins: int
    logged_in: int
    num_compromised: int
    root_shell: int
    su_attempted: int
    num_root: int
    num_file_creations: int
    num_shells: int
    num_access_files: int
    num_outbound_cmds: int
    is_host_login: int
    is_guest_login: int
    count: int
    srv_count: int
    serror_rate: float
    srv_serror_rate: float
    rerror_rate: float
    srv_rerror_rate: float
    same_srv_rate: float
    diff_srv_rate: float
    srv_diff_host_rate: float
    dst_host_count: int
    dst_host_srv_count: int
    dst_host_same_srv_rate: float
    dst_host_diff_srv_rate: float
    dst_host_same_src_port_rate: float
    dst_host_srv_diff_host_rate: float
    dst_host_serror_rate: float
    dst_host_srv_serror_rate: float
    dst_host_rerror_rate: float
    dst_host_srv_rerror_rate: float


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/predict")
def predict(input_data: PredictionInput):
    # Chuyển đổi input thành dataframe
    input_df = pd.DataFrame([input_data.dict()])

    # Encode các cột text
    for col in ['protocol_type', 'service', 'flag']:
        le = encoders[col]
        input_df[col] = le.transform(input_df[col])

    # Chọn top đặc trưng
    input_df = input_df[top_features]

    # Scale dữ liệu
    input_scaled = scaler.transform(input_df)

    # Dự đoán
    y_pred = model.predict(input_scaled)[0]
    y_proba = model.predict_proba(input_scaled)[0]

    # Giải mã nhãn
    label = encoders['attack'].inverse_transform([y_pred])[0]

    # Lấy xác suất tương ứng với nhãn được dự đoán
    class_names = encoders['attack'].inverse_transform([0, 1])
    probabilities = {class_names[i]: float(
        f"{prob:.4f}") for i, prob in enumerate(y_proba)}

    return {
        "prediction": label,
        "probabilities": probabilities
    }


# Added endpoint to get model information
@app.get("/model_info")
def model_info():
    """Return information about the model and its features"""
    return {
        "model_type": "KNeighborsClassifier",
        "top_features": top_features,
        "total_features": len(top_features)
    }
