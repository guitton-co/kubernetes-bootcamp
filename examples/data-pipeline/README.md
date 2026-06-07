# Example: Data pipeline (Airflow on Kubernetes)

Runs the official Airflow chart against the Postgres you deploy from
`apps/postgres`, with DAGs synced straight from your fork.

## Deploy

```sh
# from the repo root
helmfile sync
kubectl -n data get pods -w
```

## See the Airflow UI

```sh
kubectl -n data port-forward svc/airflow-webserver 8080:8080
# open http://localhost:8080  (default login: admin / admin)
```

…or right-click the service in Lens/FreeLens → *port-forward*.

## Make it yours

1. Edit `airflow-values.yaml`: set `dags.gitSync.repo` to **your** fork.
2. Drop your DAGs in `dags/` (replace `example_pipeline.py`).
3. `helmfile sync` again — gitSync pulls your changes, no image rebuild.

Swap the toy DAG for a dlt source, a SQLMesh run, a DuckDB transform — whatever
you pitched.
