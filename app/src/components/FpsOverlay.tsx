interface FpsOverlayProps {
  isLocked: boolean;
  onRequestLock: () => void;
}

export default function FpsOverlay({
  isLocked,
  onRequestLock,
}: FpsOverlayProps) {
  if (isLocked) return null;

  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        backgroundColor: "rgba(0, 0, 0, 0.6)",
        color: "white",
        zIndex: 1000,
      }}
    >
      <h2 style={{ fontSize: "2rem", marginBottom: "1rem" }}>일시정지</h2>
      <button
        onClick={onRequestLock}
        style={{
          padding: "0.75rem 2rem",
          fontSize: "1rem",
          cursor: "pointer",
          backgroundColor: "white",
          color: "black",
          border: "none",
          borderRadius: "4px",
          marginBottom: "1rem",
        }}
      >
        클릭하여 재개
      </button>
      <p style={{ fontSize: "0.9rem", opacity: 0.8 }}>
        ESC를 눌러 조작을 일시정지할 수 있습니다
      </p>
    </div>
  );
}
