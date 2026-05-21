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
      <div style={{ marginBottom: "8px" }}>현재 화재 발생: {count}건</div>
      <div
        style={{
          fontSize: "12px",
          fontWeight: "normal",
          color: "#aaaaaa",
          letterSpacing: "0.5px",
        }}
      >
        <span
          style={{
            fontSize: "13px",
            fontWeight: "bold",
            color: "#f32121",
            padding: "2px 6px",
            borderRadius: "3px",
          }}
        >
          중앙 조준점에서 불을 클릭하여 진압하세요!
        </span>
        <br />
        이동: W/A/S/D | 상하: E/Q | 부스터: Shift
      </div>
    </div>
  );
}
