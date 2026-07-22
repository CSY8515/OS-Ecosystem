# OS Ecosystem Structure

Version: v0.7.0

## Repository layout

- `.github/workflows`: CI 검증
- `.streamlit`: Theme과 배포 설정 예시
- `app.py`: 통합 제품 셸, World Explorer와 Streamlit 진입점
- `VERSION`: OS Ecosystem Release identity
- `AI-Hub/`: Repository 내부 AI 운영 구성요소
- `Safety-Capability/`, `Enhancement-Capability/`, `Automation-Capability/`, `Collaboration-Connectivity-Capability/`, `Personal-Secretary-Capability/`: 독립 Capability 패키지
- `Living-OS/`, `Universal-Learning-Engine/`: 독립 연결 System 작업공간
- `tests/`: 제품, 문서, 회귀 Contract 검증
- `docs/`: 모든 공식 문서

## Documentation layout

- `docs/architecture`: Architecture, Master Design, Structure, Roadmap, Common UI System, Metadata·Navigation Contract
- `docs/governance`: Constitution, Rules, Principles, Standards, Policies, Decisions, Conventions, 책임 경계
- `docs/registry`: Project, Capability, Version, Release, Contract, Route Registry
- `docs/release`: Release Note, Version History, Migration Note, Release Review
- `docs/capabilities`: 공통 Capability 문서 규칙과 Capability별 계약

## 공통 UI 배치

- `app.py`는 공통 Header, Navigation, Breadcrumb, World Explorer, Action Card, State Panel의 Runtime 구현을 소유합니다.
- `docs/architecture/UI_SYSTEM.md`는 우주·세계수·가지·열매·씨앗·성장의 의미와 재사용 가능한 컴포넌트 계약을 소유합니다.
- Living OS, Universal Learning Engine, Ultra Brain은 이 디자인 언어를 재사용할 수 있지만 Repository·Runtime·Governance 소유권은 이전되지 않습니다.

## 배치 원칙

Repository root는 실행 진입점, 패키지 경계, 테스트와 Navigation만 둡니다. 공식 설계와 수명주기 문서는 `docs/`에 둡니다. Package README는 운영 진입점이며 공식 문서를 대체하지 않습니다.

AI Hub는 이 Repository가 소유하고 같은 Release와 배포를 따릅니다. Living OS와 Universal Learning Engine은 독립 소유권, 데이터, 테스트, Release, 배포를 유지합니다.