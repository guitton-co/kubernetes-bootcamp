# Example: Web service (FastAPI on Kubernetes)

Containerise a small app, push the image, and run it with a Deployment +
Service + (optional) Ingress.

## Build & push the image

```sh
cd examples/web-service
docker build -t ghcr.io/<your-username>/k8s-kata-web:latest .
docker push ghcr.io/<your-username>/k8s-kata-web:latest
```

Then set that image name in `k8s/deployment.yaml`.

> On kind/k3d you can skip the registry and load the image directly:
> `kind load docker-image k8s-kata-web:latest` (and use that name in the manifest).

## Deploy

```sh
kubectl create namespace web
kubectl -n web apply -f k8s/
kubectl -n web get pods
```

## Reach it

With an Ingress controller: open http://web.localhost

Without one (simplest):

```sh
kubectl -n web port-forward svc/web 8080:80
# open http://localhost:8080
```

## Make it yours

Replace `app.py` with your own service (a Marimo app, a model endpoint, a Node
API). Keep a `/health` route so the probes in `k8s/deployment.yaml` still work,
or update them to match your app.
