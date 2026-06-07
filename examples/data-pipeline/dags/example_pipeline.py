"""A tiny, self-contained DAG so you can see Airflow run on Kubernetes.

Swap this out for your own project: a dlt source, a SQLMesh run, a DuckDB
transform, whatever you pitched. The point is that it schedules and runs
inside the cluster — watch it happen visually in Lens/FreeLens.
"""
from __future__ import annotations

import pendulum
from airflow.decorators import dag, task


@dag(
    schedule="@daily",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=False,
    tags=["bootcamp", "example"],
)
def example_pipeline():
    @task
    def extract() -> list[dict]:
        # Pretend this is dlt / an API pull / a SQL read.
        return [{"city": "Berlin", "temp_c": 21}, {"city": "Paris", "temp_c": 24}]

    @task
    def transform(rows: list[dict]) -> float:
        avg = sum(r["temp_c"] for r in rows) / len(rows)
        print(f"Average temp across {len(rows)} cities: {avg:.1f}C")
        return avg

    transform(extract())


example_pipeline()
