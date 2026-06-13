from fastapi import FastAPI
import os
import socket

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "status": "Online",
        "pod_name": os.getenv("HOSTNAME", "Unknown-Pod"),
        "pod_ip": socket.gethostbyname(socket.gethostname()),
        "message": "MicroK8s is working"
    }

@app.get("/healthz")
def health_check():
    return {"status": "healthy"}