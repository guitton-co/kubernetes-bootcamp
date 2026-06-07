# Environment Setup

Do this **before** the first live session. It takes ~30 minutes. If anything
fights you, drop it in the Slack channel — setup snags are exactly what it's for.

You need three things: command-line tools, a Kubernetes cluster, and a visual
IDE to look at it.

## 1. Command-line tools

| Tool | What it's for | Install |
|---|---|---|
| `git` | clone your fork | preinstalled on most systems |
| `uv` | Python + deps (for the data example) | https://docs.astral.sh/uv/getting-started/installation/ |
| `kubectl` | talk to the cluster | https://kubernetes.io/docs/tasks/tools/ |
| `helm` | install charts | https://helm.sh/docs/intro/install/ |
| `helmfile` | one-command stack install | https://github.com/helmfile/helmfile/releases |

On macOS with Homebrew this is just:

```sh
brew install uv kubectl helm helmfile
```

Verify:

```sh
kubectl version --client && helm version && helmfile version
```

## 2. A Kubernetes cluster

Pick **one** option. Local is simplest; the cloud option is there if your laptop
is underpowered or you want something closer to production.

### Option A — Local (recommended to start)

Any of these gives you a one-node cluster:

- **Docker Desktop** → Settings → Kubernetes → *Enable Kubernetes*.
- **kind**: `kind create cluster --name bootcamp`
- **k3d**: `k3d cluster create bootcamp`

Check it:

```sh
kubectl get nodes
```

> Airflow is chunky. Give Docker Desktop at least 4 CPUs and 8 GB RAM
> (Settings → Resources), or use the `LocalExecutor` already set in the
> data example.

### Option B — Cloud VM + K3s

Useful when local resources are tight. Spin up a small cloud VM, then:

```sh
# On the VM
curl -sfL https://get.k3s.io | sh -
sudo cat /etc/rancher/k3s/k3s.yaml   # this is your kubeconfig
```

**The gotcha that wastes everyone an afternoon:** the k3s kubeconfig points at
`127.0.0.1`, which is the VM's loopback, not reachable from your laptop. Copy
the file locally and rewrite the server address to the VM's **public IP**:

```sh
# On your laptop, after copying k3s.yaml down
sed -i '' 's/127.0.0.1/<VM_PUBLIC_IP>/' k3s.yaml   # macOS
# sed -i 's/127.0.0.1/<VM_PUBLIC_IP>/' k3s.yaml     # Linux
export KUBECONFIG=$PWD/k3s.yaml
kubectl get nodes
```

Make sure the VM's firewall allows inbound TCP on port **6443** from your IP.

## 3. A visual Kubernetes IDE

The course leans on seeing the cluster, not memorising commands. Two free
options — **FreeLens is the no-friction default in 2026**:

- **FreeLens** (recommended): open-source MIT fork, no account needed.
  Download from https://github.com/freelensapp/freelens/releases
- **Lens Desktop**: the official app. Free for personal/education use but
  requires a Lens ID login. https://k8slens.dev/

Either one auto-detects your kubeconfig. Open it, pick your `bootcamp` context,
and you should see your node and (after `helmfile sync`) your Pods.

> Avoid OpenLens — as of 2026 it's effectively unmaintained; FreeLens is its
> active successor.

## You're ready when

```sh
kubectl get nodes        # shows a Ready node
helmfile sync            # deploys Postgres + Airflow into the 'data' namespace
kubectl -n data get pods # pods moving toward Running
```

…and you can see those same Pods in FreeLens/Lens.
