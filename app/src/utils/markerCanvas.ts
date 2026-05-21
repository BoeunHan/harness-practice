/**
 * 텍스트 깨짐을 원천 차단하는 고해상도(High-DPI) 마커 생성 함수
 */
export function createHighDPICircleMarker(
  text: string,
  borderColor: string,
  borderWidth: number = 6,
) {
  const canvas = document.createElement("canvas");

  // 1. 고해상도 처리를 위해 실제 캔버스 픽셀 사이즈를 2배(200x200)로 크게 잡습니다.
  const baseSize = 120;
  const scale = 2;
  canvas.width = baseSize * scale;
  canvas.height = baseSize * scale;

  const ctx = canvas.getContext("2d");

  if (ctx) {
    // 2. 좌표계를 scale(2배)만큼 확장시켜서 부드러운 안티앨리어싱 효과를 유도합니다.
    ctx.scale(scale, scale);

    const centerX = baseSize / 2;
    const centerY = baseSize / 2;
    const radius = baseSize / 2 - borderWidth;

    // 그림자 효과 살짝 넣어주면 3D 지도에서 가독성이 급상승합니다.
    ctx.shadowColor = "rgba(0, 0, 0, 0.25)";
    ctx.shadowBlur = 6;
    ctx.shadowOffsetY = 3;

    // 원 배경 그리기 (흰색)
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI, false);
    ctx.fillStyle = "#FFFFFF";
    ctx.fill();

    // 그림자 끄고 테두리선 선명하게 그리기
    ctx.shadowColor = "transparent";
    ctx.lineWidth = borderWidth;
    ctx.strokeStyle = borderColor;
    ctx.stroke();

    // 3. 텍스트 배치 (Canvas 내부에서 직접 렌더링하므로 글자 깨짐이 완전히 사라집니다)
    if (text) {
      ctx.fillStyle = "#111111"; // 완전 생블랙보다는 고급스러운 먹색
      ctx.font = "bold 18px sans-serif"; // 캔버스 해상도에 맞는 적절한 폰트 크기
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";

      // 글자 수가 많아 원 밖으로 나가는 현상을 막기 위해 최대 너비 제한 지정
      ctx.fillText(text, centerX, centerY, radius * 1.6);
    }
  }

  return canvas;
}
