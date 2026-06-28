# Project Ideas

You'll spend the two weeks between Sessions 1 and 2 deploying a project of
your choice to Kubernetes. **Bring your own** if you have one — otherwise pick
from this list.

Each idea maps cleanly to a Kubernetes pattern, so you'll learn one new K8s
object per project.

Propose your project with a 2-line PR using
[`.github/pull_request_template.md`](../.github/pull_request_template.md) by
**Mon 6 Jul**.

---

## 1. Personal API (FastAPI / Flask / Express)

Wrap something useful behind HTTP — a model endpoint, a webhook handler, a
calculator, anything.

| K8s object | Why |
|---|---|
| `Deployment` | Run multiple replicas of your API |
| `Service` (ClusterIP) | Stable internal address |
| `Ingress` | Optional: expose at a real URL |
| `ConfigMap` | App config without rebuilding the image |

**Starting point**: `examples/web-service` is exactly this pattern.

---

## 2. Scheduled scraper / backup / report

Anything that runs on a cron — daily scrape, hourly backup, weekly digest.

| K8s object | Why |
|---|---|
| `CronJob` | The schedule + the work definition |
| `PersistentVolumeClaim` | Store output between runs |
| `Secret` | API keys / credentials |
| `ConfigMap` | Schedule + non-secret config |

**Starting point**: `examples/cronjob` shows the CronJob → Job → Pod chain.

---

## 3. Marimo / Streamlit dashboard

A single-page interactive analytics dashboard, served as a long-running app.

| K8s object | Why |
|---|---|
| `Deployment` | Single-replica is fine (most dashboards aren't HA) |
| `Service` + `Ingress` | Reach it from a browser |
| `ConfigMap` | Connection strings, dashboard config |
| `Secret` | DB credentials |

**Starting point**: `examples/nextjs-app` is the same shape (front-end app
behind Service + Ingress).

---

## 4. Batch data pipeline (dlt / SQLMesh / DuckDB / Python script)

A pipeline that runs on a schedule and writes to a database. **Use the shared
`data` namespace's Postgres** rather than spinning up your own.

| K8s object | Why |
|---|---|
| `CronJob` | Trigger the pipeline run |
| `Secret` | Postgres credentials (read from the shared `data` namespace) |
| `ConfigMap` | Source config, table names, etc. |

**Starting point**: `examples/data-pipeline/dags/example_pipeline.py` is an
Airflow DAG; you can do the same thing as a plain CronJob if you don't need
Airflow's UI.

---

## 5. Chat bot (Discord / Telegram / Slack)

A long-running bot that reacts to messages.

| K8s object | Why |
|---|---|
| `Deployment` (replicas: 1) | Long-lived process |
| `Secret` | Bot token |
| `ConfigMap` | Bot config (channels, commands) |

**Starting point**: pattern is the same as the FastAPI app minus the Ingress.
Bot connects out, so no inbound traffic needed.

---

## Rules of the road

- **Namespace**: deploy into your own — `<resource>-<github-handle>`. The
  cohort cluster is shared.
- **Image**: build for `linux/amd64` and push to `ghcr.io/<your-handle>/...`
  (see `SETUP.md`). Set the package public.
- **Resources**: each namespace has a `ResourceQuota` (1 CPU request,
  1 GB memory, 15 Pods). Plenty for these projects.
- **Scope**: aim for **deploys**, not perfection. A working CronJob with
  one task beats a half-built API with auth.

Stuck choosing? Post in Slack `#help` and we'll narrow it down together.
