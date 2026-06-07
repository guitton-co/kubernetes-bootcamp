# Example: Next.js app (on Kubernetes)

A hello-world Next.js (App Router, TypeScript) app, containerised with the
standalone build and deployed with a Deployment + Service + (optional) Ingress.
Same shape as `../web-service`, but for the JS/TS stack.

## Run locally first

```sh
npm install
npm run dev        # http://localhost:3000
```

## Build & push the image

```sh
cd examples/nextjs-app
docker build -t ghcr.io/<your-username>/k8s-kata-nextjs:latest .
docker push ghcr.io/<your-username>/k8s-kata-nextjs:latest
```

Then set that image name in `k8s/deployment.yaml`.

> On kind/k3d you can skip the registry:
> `docker build -t k8s-kata-nextjs:latest .`
> `kind load docker-image k8s-kata-nextjs:latest` (use that name in the manifest).

## Deploy

```sh
kubectl create namespace nextjs
kubectl -n nextjs apply -f k8s/
kubectl -n nextjs get pods
```

## Reach it

With an Ingress controller: http://nextjs.localhost

Without one (simplest):

```sh
kubectl -n nextjs port-forward svc/nextjs 3000:80
# open http://localhost:3000
```

The home page prints the serving pod's hostname — scale the Deployment in Lens
and refresh to watch requests land on different pods.

## Make it yours

Replace the page and API routes with your app. Keep `/api/health` (or update the
probes in `k8s/deployment.yaml`) so Kubernetes can tell when a pod is ready.

## Notes

- `next.config.mjs` sets `output: "standalone"` — the Dockerfile depends on it.
- The image runs as a non-root user and listens on port 3000.
