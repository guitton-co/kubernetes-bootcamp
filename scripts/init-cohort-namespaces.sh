#!/usr/bin/env bash
#
# Pre-create per-student namespaces on the shared cohort cluster and apply
# a ResourceQuota + LimitRange to each. Run once when all GitHub handles
# are collected (after the prerequisite email replies land).
#
# Usage:
#   ./scripts/init-cohort-namespaces.sh handle1 handle2 handle3 ...
#
# Idempotent — safe to re-run when a new handle joins.

set -euo pipefail

if [[ $# -eq 0 ]]; then
  echo "Usage: $0 <github-handle> [github-handle ...]" >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QUOTA_FILE="${SCRIPT_DIR}/../apps/resource-quota/quota.yaml"

# Namespaces every student gets pre-created. Add more here if needed.
NAMESPACES=("web" "nextjs" "cron" "troubleshooting" "project")

for handle in "$@"; do
  for ns in "${NAMESPACES[@]}"; do
    full="${ns}-${handle}"
    echo "==> ${full}"
    kubectl create namespace "${full}" --dry-run=client -o yaml | kubectl apply -f -
    kubectl -n "${full}" apply -f "${QUOTA_FILE}"
  done
done

echo
echo "Done. Created namespaces + ResourceQuota for: $*"
echo "Verify with: kubectl get ns | grep -E '$(IFS=\|; echo "$*")'"
