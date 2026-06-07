# The Visual Debugging Cheatsheet (Lens / FreeLens)

The whole point of the course: you can do ~80% of daily Kubernetes work by
looking, not by memorising `kubectl`. Here's the workflow.

## The five things to look at

1. **Workloads → Pods** — is it `Running`? `Pending`? `CrashLoopBackOff`?
2. **Workloads → Deployments** — desired vs available replicas.
3. **Network → Services** — what's exposed, and does it have endpoints?
4. **Events** (Pod detail, bottom) — Kubernetes narrates *why* things fail here.
5. **Logs** (Pod → log icon) — stream stdout/stderr, multiple containers at once.

## Debugging a broken workload, visually

| Symptom | Where to look | Usual cause |
|---|---|---|
| `Pending` forever | Pod → Events | no node resources, or unbound PVC |
| `ImagePullBackOff` | Pod → Events | wrong image name/tag, or private registry |
| `CrashLoopBackOff` | Pod → Logs | app erroring on startup (bad config/env) |
| Service returns nothing | Service → Endpoints | selector labels don't match Pod labels |

A Service with **zero endpoints** is the classic silent failure: the Service
selector and the Pod labels have drifted apart. Lens shows this at a glance;
the CLI makes you cross-reference two `get` commands.

## Three actions you'll use constantly

- **Logs**: Pod → log icon. Follow live, search, pin multiple containers.
- **Shell**: Pod → terminal icon → exec into the container to poke around.
- **Port-forward**: Service/Pod → forward, to reach something with no Ingress
  (e.g. the Airflow UI, or `svc/web`).

## When NOT to use Lens

Lens is for *seeing* and *debugging*. For anything repeatable — installing the
stack, applying manifests — stay declarative (`helmfile sync`, `kubectl apply`)
so it's reproducible and reviewable. Look in Lens; change in Git.
