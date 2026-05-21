interface FireDashboardProps {
  count: number;
}

export default function FireDashboard({ count }: FireDashboardProps) {
  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        backgroundColor: "rgba(0, 0, 0, 0.6)",
        color: "#ffffff",
        padding: "12px 20px",
        zIndex: 1000,
        textAlign: "center",
        fontSize: "16px",
        fontWeight: "bold",
      }}
    >
      현재 화재 발생: {count}건
    </div>
  );
}
