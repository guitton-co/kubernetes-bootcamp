# Live Sessions — 2 × 30 min (Google Meet)

Two sessions, each ~30 min. Demo in Lens/FreeLens (see [`lens.md`](lens.md));
change things in Git.

- **Session 1** — setup-first: every student has cluster access, can see the
  cluster in Lens, and has deployed their first workload before they log off.
- **Session 2** — project-driven: built from the student project proposals that
  land between sessions. Each project gets a 5-min K8s-pattern walkthrough plus
  a short live demo at the end.

The cohort shares one managed cluster. Namespace convention is
`<resource>-<github-handle>` (e.g. `web-mxkrn`, `data-mxkrn`) — drilled in S1
so nobody stomps each other's work.

---

## Session 1 — Get on the cluster (30 min)

Goal: by minute 20, everyone has `kubectl get nodes` working, has Lens
connected, and has a Pod of their own running. Last 10 min introduce the
object model on top of what they just deployed.

| Min   | Topic                                 | Live demo                                                                                                                                                                  | What students do                                                |
| ----- | ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| 0–5   | **Cluster access**                    | `export KUBECONFIG=...kubeconfig.yaml`; `kubectl get nodes` → 3 Ready nodes                                                                                                | Same on their machine. Anyone failing → fix in chat now.        |
| 5–10  | **Lens tour**                         | Open Lens, add the kubeconfig, navigate: Nodes → Workloads → Networking → Storage. Show that everything is just an API resource.                                          | Click around. No theory yet.                                    |
| 10–18 | **Your first workload**               | Deploy `examples/web-service` into `web-<handle>`. Watch the Deployment → ReplicaSet → Pod chain appear live in Lens. `kubectl -n web-<handle> port-forward svc/web 8080`. | Each student deploys to **their own namespace**. Confirm 2 Pods running. |
| 18–25 | **Read the cluster: the four lenses** | Open one Pod in Lens — show **Logs**, **Shell**, **Events**, **YAML**. Events tab = the "why it broke" tab.                                                               | Open their Pod, find logs + events.                             |
| 25–30 | **Recap + project setup**             | Point at `examples/cronjob/` + `examples/data-pipeline/` + `examples/nextjs-app/` for self-study. Remind: **PR with project proposal by Mon 6 Jul**.                       | Pick a project idea, write the proposal PR by Monday.           |

**Hard rules drilled in S1:**

- Always use `kubectl -n <your-ns>` or set `kubens` — never deploy to `default`.
- Namespace = `<resource>-<github-handle>`. The example `kubectl apply` lines
  in the repo READMEs say `web`, `nextjs`, `data` — students must rename.
- Image pushes from Apple Silicon need `docker buildx build --platform linux/amd64`
  (see `SETUP.md`).

**Self-study covered by repo, not S1:**

CronJob (`examples/cronjob/`), ConfigMap/Secret patterns (visible in
`apps/postgres`), Ingress (`examples/nextjs-app/k8s/ingress.yaml`). Each has a
README and runs on the shared cluster. Slack `#help` is the support channel.

---

## Session 2 — Your projects, the K8s patterns they need (30 min)

**Built from project proposals.** Pre-session work (Mon 6 Jul – Wed 15 Jul):

1. Read every proposal PR. Identify the K8s pattern each one needs.
2. Group projects by pattern. Common buckets to expect:
   - **Web service** → Deployment + Service + Ingress (covered in S1 already → recap only)
   - **Scheduled job** → CronJob + concurrency/TTL patterns
   - **Stateful** → PVC + StatefulSet (Postgres in `apps/postgres` is the reference)
   - **Async pipeline** → Helm chart consumption (Airflow in `examples/data-pipeline`)
   - **Multi-service** → Service-to-Service networking, ConfigMap/Secret injection
3. Pick 2–3 pattern blocks to cover live. Leave the rest as repo pointers + Slack.
4. Order: pattern demo → live edit → student-project mapping.

| Min   | Topic                            | Source (fill after proposals land)                                                          |
| ----- | -------------------------------- | ------------------------------------------------------------------------------------------- |
| 0–3   | **Recap S1 + map the cohort**    | 1-slide: project list grouped by pattern. "Here's what we need to cover for your projects." |
| 3–10  | **Pattern block 1**              | _TBD from proposals_ — e.g. Ingress + TLS, CronJob, StatefulSet                             |
| 10–17 | **Pattern block 2**              | _TBD from proposals_                                                                        |
| 17–22 | **Pattern block 3 OR Helm deep** | If 3+ projects use community charts: contrast hand-written `apps/postgres` vs `apache-airflow/airflow` |
| 22–28 | **Student demos**                | Each student: 30s screen-share of their project running in Lens. State 1 thing that fought them. |
| 28–30 | **Wrap + async**                 | Slack stays open after the cohort; office-hours offer.                                      |

**Stretch patterns that might appear (kept inline, not in S1):**

- **CRDs / Operators** — Strimzi Kafka is the clean teaching example:
  ```sh
  kubectl create namespace kafka-<handle>
  kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka-<handle>' -n kafka-<handle>
  kubectl apply -f https://strimzi.io/examples/latest/kafka/kafka-single-node.yaml -n kafka-<handle>
  ```
  Anchor: Helm packages _known_ apps; operators teach K8s about _new_ kinds of
  app via CRDs.
- **HPA / autoscaling** — only if a project has variable load.
- **NetworkPolicy** — only if a project asks for tenant isolation.

---

## Async week between sessions (Mon 6 – Thu 16 Jul)

- Students iterate on their project in their own namespaces.
- Louis on Slack `#help` daily; PR reviews on each project repo.
- By end-of-week each project should have: namespace + Deployment(s) +
  Service + at least one of (Ingress | CronJob | PVC | ConfigMap).

## References (for your S2 prep, not for sharing)

- `docs/louis/2026-06-26-curriculum/CKAD_Curriculum_v1.35.pdf` — domain
  checklist (App Design 20%, Build & Deploy 20%, Env & Config 25%, Observability
  15%, Services & Networking 20%). Use to sanity-check coverage gaps per project.
- killercoda K8s + Helm labs — pattern for hands-on flow if a pattern block
  needs a fallback exercise.
- kodekloud Lens IDE course — visual-first framing already baked into the
  Lens-tour stop in S1.
