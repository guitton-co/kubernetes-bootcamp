export const dynamic = "force-dynamic";

export default function Home() {
  return (
    <main
      style={{
        fontFamily: "system-ui, sans-serif",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        minHeight: "100vh",
        gap: "0.5rem",
      }}
    >
      <h1>Hello from Next.js on Kubernetes 🚀</h1>
      <p>
        Served by pod: <code>{process.env.POD_NAME ?? "unknown"}</code>
      </p>
    </main>
  );
}
