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

## Session 1 — Get on the cluster (~30 min)

Goal: everyone has `kubectl get nodes` working, has Lens connected, and has
deployed a working Pod by the end. Then a short tour of the four lenses
(Logs / Shell / Events / YAML) on a Pod we **pre-broke** so they see the
debugging pattern they'll need on their own projects.

No image builds in S1. Students apply pre-built images (`ghcr.io/louisguitton/k8s-kata-web:latest`).
Building + pushing their own images is async-week work.

Block-based, not minute-locked. Adjust live based on the room.

| Block | Topic                                | What we do                                                                                                                                                                                                                                              |
| ----- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1     | **Cluster access — everyone in**     | Demo `export KUBECONFIG=...` + `kubectl get nodes`. Quick round-robin in Slack `#help`: paste your `kubectl get nodes` output. Pre-S1 screencast covers the Lens-add-cluster step, so we just confirm it.                                                |
| 2     | **Lens tour — the resource graph**   | Open Lens, walk: Nodes → Workloads → Networking → Storage. Show that Deployment, ReplicaSet, Pod are the same chain in three places. **Anchor**: "this is what your projects will look like."                                                           |
| 3     | **First workload — pre-built image** | Apply `examples/web-service/k8s/` (image `ghcr.io/louisguitton/k8s-kata-web:latest`) into your pre-created `web-<handle>` namespace. Watch the Deployment → ReplicaSet → Pod chain appear live. `kubectl -n web-<handle> port-forward svc/web 8080:80`. |
| 4     | **The four lenses on a broken Pod**  | Apply `examples/troubleshooting/k8s/`. Walk through Events tab on `broken-image` (ImagePullBackOff), previous-logs on `broken-command` (CrashLoopBackOff), Shell + curl on `broken-probe` (Pod Running, not Ready). The Events tab is the headline.     |
| 5     | **Q&A**                              | Open mic. Anything stuck or unclear. ~5 min budget.                                                                                                                                                                                                     |
| 6     | **Wrap + project proposals**         | Point at `docs/project-ideas.md` (5 seed projects) and the PR template. **Proposal PR due Mon 6 Jul.** Reiterate Slack `#help` is the async channel.                                                                                                    |

**Hard rules stated up front (one slide):**

- Your namespaces are pre-created: `web-<handle>`, `nextjs-<handle>`,
  `cron-<handle>`, `troubleshooting-<handle>`, `project-<handle>`. They have
  a `ResourceQuota` (1 CPU req, 1 GB mem, 15 Pods).
- Always set `export HANDLE=<your-github-handle>` and use `-n web-$HANDLE`.
  Never deploy to `default` or to an unsuffixed namespace.
- The shared `data` namespace (Postgres + Airflow) is **read-only** — don't
  redeploy `examples/data-pipeline`. Use the shared instance.
- Image pushes from Apple Silicon need `docker buildx build --platform linux/amd64`
  (covered in `SETUP.md`, comes up in async week).

**Self-study covered by repo, not S1:**

CronJob (`examples/cronjob/`), ConfigMap/Secret patterns (visible in
`apps/postgres`), Ingress (`examples/nextjs-app/k8s/ingress.yaml`), more
debugging drills (`examples/troubleshooting/`). Each has a README and runs on
the shared cluster. Slack `#help` is the support channel.

## Pre-S1 prep (Louis, by Thu 2 Jul EOD)

- Send screencast: "save the kubeconfig + add cluster to Lens + first nav."
  Upload to Drive, post in Slack.
- Run `scripts/init-cohort-namespaces.sh <handle1> <handle2> ...` once all
  handles are in (deadline Mon 29 Jun per runbook). Creates the 5 namespaces
  per student + applies `apps/resource-quota/quota.yaml`.
- Post Slack thread "post your `kubectl get nodes` output" — due Thu 2 Jul EOD.
  Non-blocking, but lets you triage setup issues before showtime.

## Troubleshooting (share with students if they hit issues)

| Symptom | Fix |
|---|---|
| `kubectl: command not found` | `brew install kubectl` (mac) or follow `SETUP.md` §1. |
| `error: KUBECONFIG environment variable not set` | `export KUBECONFIG=/path/to/k8s-bootcamp-guittonco-2026-06-kubeconfig.yaml`; persist in `~/.zshrc`. |
| `Unable to connect to the server: dial tcp ... i/o timeout` | Network/VPN/firewall blocking 443 to the DO control plane. Switch network, try again. |
| `forbidden: User "..." cannot create resource ... in namespace "default"` | You're using the wrong namespace. `kubectl get ns \| grep <your-handle>` should list your pre-created namespaces; deploy with `-n web-<handle>`. |
| Lens shows "No clusters added" | File → Add Cluster → from kubeconfig → point at the downloaded file. Multi-kubeconfig is supported. |
| Pod `Pending` forever | Likely `ResourceQuota` exceeded. `kubectl -n <ns> describe quota` shows usage; `kubectl -n <ns> describe pod <pod>` shows the actual reason. |
| Pod `ImagePullBackOff` for your own image | Image not pushed, or package is private. `gh` → Your Packages → Settings → Public. Or check arch — `linux/amd64`, not arm64. |
| Pod `CrashLoopBackOff` | App is exiting. `kubectl -n <ns> logs <pod> --previous` to read the last crashed container's logs. |

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

| Min   | Topic                            | Source (fill after proposals land)                                                                     |
| ----- | -------------------------------- | ------------------------------------------------------------------------------------------------------ |
| 0–3   | **Recap S1 + map the cohort**    | 1-slide: project list grouped by pattern. "Here's what we need to cover for your projects."            |
| 3–10  | **Pattern block 1**              | _TBD from proposals_ — e.g. Ingress + TLS, CronJob, StatefulSet                                        |
| 10–17 | **Pattern block 2**              | _TBD from proposals_                                                                                   |
| 17–22 | **Pattern block 3 OR Helm deep** | If 3+ projects use community charts: contrast hand-written `apps/postgres` vs `apache-airflow/airflow` |
| 22–28 | **Student demos**                | Each student: 30s screen-share of their project running in Lens. State 1 thing that fought them.       |
| 28–30 | **Wrap + async**                 | Slack stays open after the cohort. No synchronous office hours — everything async in `#help`.          |

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
- Louis on Slack `#help`, M–F, **24h SLA, intra-day best-effort**. No
  synchronous office hours; everything happens in `#help` or on the project PR.
- Louis can pull student code via `gh classroom` and inspect their namespace
  directly on the shared cluster — fast triage without a call.
- `@here` only when truly blocked. Default to channel post.
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
