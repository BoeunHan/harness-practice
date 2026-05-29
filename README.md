# 멀티 에이전트 하네스 & 3D Cesium 화재 진화 시뮬레이터

> 본 프로젝트는 AI-DLC 환경에서 개발자가 파이프라인의 제어권을 쥐는 구조를 설계하고, 
<br/>배경지식이 없던 3D 공간 정보 도메인의 개발 속도를 어디까지 가속할 수 있는지 직접 검증하기 위해 7일간 수행한 데모 프로젝트입니다.

---

## 7일 로드맵 & 주요 결과

*   **1 ~ 4일 차:** 멀티 에이전트 하네스 파이프라인 구축 및 개발자 인터랙션 분기 구조 설계/구현
*   **5 ~ 7일 차:** 구축한 하네스를 통해 Cesium 기반 3D 화재 진화 시뮬레이터 MVP 완성 및 생산성 검증

---

## 기술 스택

### 하네스 파이프라인
*   Python, Claude Code CLI(model: Claude 4.6 Sonnet), questionary

### 3D 시뮬레이터
*   React, Vite, TypeScript, Cesium

---

## 하네스 아키텍처

단순한 텍스트 기반의 일방향 AI 코드 생성이 아닌, 개발자가 중간 단계에서 파이프라인을 통제할 수 있는 **인터랙션 분기 구조**를 구현했습니다.
<img width="1436" height="1252" alt="하네스 아키텍처" src="https://github.com/user-attachments/assets/370af141-3b9d-42f0-a2fb-ce421caadd74" />

---
## 폴더 구조

```text
.
├── app/                  # [Frontend App] Cesium 기반 3D 시뮬레이터 프로덕트
│   └── src/
│       ├── components/   # UI 컴포넌트 (지도, 대시보드 등)
│       ├── hooks/        # 카메라 제어 및 레이저 캐스팅 커스텀 훅 모듈
│       ├── types/        # 타입 정의
│       ├── App.tsx       # 메인 애플리케이션 엔트리
│       └── main.tsx
│
├── harness/              # [AI Pipeline Engine] 파이프라인 엔지니어링 Python 모듈
│   ├── debug/            # 현재 실행한 에이전트에게 제공한 prompt 전체 완성본 (디버깅용)
│   ├── agents/           # Planner, Executor, Reviewer 에이전트 핵심 로직 및 에이전트별 프롬프트 규칙
│   ├── tools/            # 클로드 실행, 파일 탐색, cli 출력 등 도구 모음
│   ├── workflow.py       # 하네스 파이프라인 구동 스크립트
│   └── main.py           # 실행 진입점
│
└── docs/                        # [Pipeline Docs] 파이프라인 실행 진입 및 에이전트 산출물
    ├── 00_example_project/      # 각 프로젝트의 파이프라인 산출 문서 모음
    └── target.template.json     # 각 프로젝트 진입 시 기본적으로 필요한 문서의 템플릿
```

---
## 주요 구현 기능
- 건물과 지형의 3D 환경 반영
- FPS 스타일 3D 가상 공간 카메라 제어 (WASDEQ 키를 통한 방향 제어, 마우스 드래그로 시선 제어, Shift로 이동속도 가속)
- 랜덤 화재 발생 시, 사선 레이저 캐스팅을 활용하여 지면이나 건물 옥상뿐만 아니라 건물 벽면까지 포함한 정확한 화재 위치 산출
- 사용자가 충분히 가까운 거리에서 클릭했을 경우에만 화재 진화 처리
- 시간 경과에 따른 화재 3D 엔티티 크기 점진적 업데이트
- 카메라 이동 범위 제한 및 반대 방향 키 동시 클릭 시 발생하는 런타임 에러 수정
- 컴포넌트 언마운트 시 발생할 수 있는 리소스 누수 방어
---

## 주요 화면

<img width="1905" height="887" alt="상공에서 내려다본 지상" src="https://github.com/user-attachments/assets/9bbf293f-779d-473d-9307-a5b583e9b86b" />
<img width="1907" height="901" alt="건물 외벽에 화재가 발생한 모습" src="https://github.com/user-attachments/assets/e2510d5f-5bb2-41ca-8221-26a663ab0b0d" />
<img width="1892" height="883" alt="조작을 일시정지한 화면" src="https://github.com/user-attachments/assets/602b1ded-a645-4cd9-b862-d2ee684f7369" />

--- 
## 실행 방법
### 파이프라인 실행 방식
파이프라인을 구동하여 코드를 생성하거나 하네스 인터랙션을 테스트하는 단계입니다. 
루트(Root) 디렉토리에서 실행합니다.

```bash
# 1. 가상환경 활성화 (Windows 환경)
source venv/Scripts/activate

# 2. 필수 의존성 라이브러리 설치 (최초 1회)
pip install -r harness/requirements.txt

# 3. 하네스 파이프라인 메인 스크립트 구동
python harness/main.py
```

### 3D 시뮬레이터 앱 실행 방식
파이프라인을 통해 빌드업된 Cesium 기반 3D 웹 프로토타입을 로컬 환경에 띄우는 단계입니다.
```bash
# 1. 웹 애플리케이션 디렉토리로 이동
cd app

# 2. 패키지 의존성 설치 (최초 1회)
npm install

# 3. 로컬 개발 서버 구동
npm run dev

# 4. http://localhost:5173/로 접속
```
