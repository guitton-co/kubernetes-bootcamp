// Liveness/readiness endpoint used by the Kubernetes probes.
export const dynamic = "force-dynamic";

export function GET() {
  return Response.json({ status: "ok" });
}
