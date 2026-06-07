"""Minimal FastAPI service — the 'deploy an app on K8s' starting point.

Replace with your own service (a Marimo app, a model endpoint, a Node API).
Keep the /health route: the Kubernetes probes below depend on it.
"""
from fastapi import FastAPI

app = FastAPI(title="k8s-kata web")


@app.get("/")
def root():
    return {"message": "Hello from Kubernetes!"}


@app.get("/health")
def health():
    return {"status": "ok"}
