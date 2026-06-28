# Example: Web service (FastAPI on Kubernetes)

Containerise a small app, push the image, and run it with a Deployment +
Service + (optional) Ingress.

## Build & push the image

> On Apple Silicon (M1/M2/M3), build for `linux/amd64` — the cohort cluster
> nodes are amd64, an arm64 image will fail with `exec format error`.

```sh
cd examples/web-service
docker buildx build --platform linux/amd64 \
  -t ghcr.io/<your-username>/k8s-kata-web:latest --push .
```

Then set that image name in `k8s/deployment.yaml` (replace `<your-username>`).

## Deploy

The cohort cluster is shared — every namespace must be suffixed with your
GitHub handle. Set `HANDLE` once per shell:

```sh
export HANDLE=<your-github-handle>
kubectl create namespace web-$HANDLE
kubectl -n web-$HANDLE apply -f k8s/
kubectl -n web-$HANDLE get pods
```

## Reach it

```sh
kubectl -n web-$HANDLE port-forward svc/web 8080:80
# open http://localhost:8080
```

## Make it yours

Replace `app.py` with your own service (a Marimo app, a model endpoint, a Node
API). Keep a `/health` route so the probes in `k8s/deployment.yaml` still work,
or update them to match your app. Always deploy into `web-$HANDLE`.
