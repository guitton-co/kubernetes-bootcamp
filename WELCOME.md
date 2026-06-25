# Bienvenue — Setup d'accueil

> Written in English to match the repo. Say the word and I'll ship a French
> version for participants.

Welcome to the cohort. Do these steps **in order before the first live
session** — budget ~30 minutes. Anything that fights you goes straight into
the Slack channel; setup snags are exactly what it's for.

## Access — get these first

| What | Link | Done |
|---|---|---|
| Slack channel (Q&A + support) | _<invite link>_ | ☐ |
| GitHub Classroom assignment (your fork) | _<classroom link>_ | ☐ |
| Payment (€149, Qonto) | _<payment link>_ | ☐ |
| Live session slots (2 × 30 min, Google Meet) | _<calendar link>_ | ☐ |

_(Fill the links in before sending.)_

## Then set up your environment

1. **Accept the GitHub Classroom assignment** → you get your own fork of
   `kubernetes-bootcamp`. **Set it to public** (your fork must be public or
   Airflow's gitSync will refuse to pull your DAGs).
2. **Install the tools** — follow [`SETUP.md`](SETUP.md) §1 (uv, kubectl, helm,
   helmfile, Docker).
3. **Connect to the shared cohort cluster** — you do _not_ need a local
   Kubernetes. Louis is sharing a managed cluster on Digital Ocean:
   ```sh
   # Save the attached kubeconfig somewhere safe, then:
   export KUBECONFIG=/path/to/k8s-bootcamp-guittonco-2026-06-kubeconfig.yaml
   kubectl get nodes        # should show 3 Ready nodes
   ```
   **Namespace rule (important):** the cluster is shared with the rest of the
   cohort. Every namespace you create must be suffixed with your GitHub handle
   (`web-<handle>`, `data-<handle>`, etc.) — see Session 1.
4. **Connect a visual IDE** — [`SETUP.md`](SETUP.md) §3 (FreeLens recommended).
   Point it at the same kubeconfig.
5. **Replace `<your-username>`** in the three files flagged in the repo README
   (your fork's gitSync repo and the two app images).

## You're ready when

```sh
kubectl get nodes                          # 3 Ready nodes on the shared cluster
kubectl get ns | grep <your-github-handle> # nothing yet — you'll create your own in Session 1
```

…and you can see the cluster in FreeLens/Lens.

## Before the first session, think about your project

It's a free project — pick something **you** want to run on Kubernetes (a dlt
pipeline, a SQLMesh project, a Marimo app, a service…). Open a PR with the
proposal template and Louis will confirm scope. Two or three lines is enough.
