# Example: Data pipeline (Airflow on Kubernetes)

Runs the official Airflow chart against the Postgres deployed from
`apps/postgres`, with DAGs synced straight from a fork of this repo.

> **For the cohort: this stack is deployed once, into the shared `data`
> namespace, by Louis. Don't `helmfile sync` it into your own namespace —
> Airflow on this cluster is expensive (~6 Pods, ~1 GB) and we don't have
> headroom for 7 copies.** Use the shared instance as a reference and as a
> place to drop your own DAGs (see "Add your own DAGs" below).

## See the (shared) Airflow UI

In Airflow 3 the webserver is the **API server**:

```sh
kubectl -n data port-forward svc/airflow-api-server 8080:8080
# open http://localhost:8080
```

…or right-click the service in Lens/FreeLens → *port-forward*.

Default credentials: `admin` / `admin` (chart NOTES print this).

## Add your own DAGs

Drop a `.py` file in this repo's `examples/data-pipeline/dags/` and push to
your fork. gitSync currently points at Louis's fork; for the cohort, raise a
PR on the main repo and once merged the shared instance will pick it up.

## Run it standalone (post-cohort, on your own cluster)

```sh
# from the repo root, against YOUR cluster, NOT the shared cohort one
helmfile sync
kubectl -n data get pods -w
```

Then edit `airflow-values.yaml` to point `dags.gitSync.repo` at your fork.
Swap the toy DAG for a dlt source, a SQLMesh run, a DuckDB transform.
