# OS Ecosystem

OS Ecosystem은 독립 시스템과 공통 Capability를 하나의 일관된 제품 경험으로 연결하는 통합 운영 계층입니다.

**Current version:** v0.7.0
**Release type:** Stable Product Integration
**Status:** Release Candidate
**OS Systems:** OS Ecosystem Core, AI Hub, Living OS, Universal Learning Engine
**Capabilities:** Safety, Enhancement, Automation, Collaboration & Connectivity, Personal Secretary
**Production:** https://8javbq85jtappi6tkdhkt7g.streamlit.app/

## 제품 계약

- 컨셉아트 자체를 탐색 UI로 사용하며 우주·세계수·열매·씨앗·성장의 의미를 실제 Navigation과 연결합니다.
- 한국어 우선 UI와 공통 Header, Navigation, Breadcrumb를 사용합니다.
- 세계수는 현재 OS Ecosystem Core를 나타내는 Landmark이고, 열매와 씨앗 Action Card는 이동 위치와 동작을 명시합니다.
- 클릭 가능한 요소는 전체 카드, 명확한 동작 문구, Focus 상태로 3초 안에 구분할 수 있게 합니다.
- 사이드바나 일반 대시보드 없이 홈과 내부 AI Hub가 같은 제품 셸을 사용합니다.
- Living OS와 Universal Learning Engine은 독립 프로젝트로 유지되며 실제 공개 HTTPS 주소를 새 탭에서 직접 엽니다.
- AI Hub는 이 Repository 내부 공식 구성요소이며 OS Ecosystem과 함께 버전 관리·배포합니다.
- 모든 System과 Capability 설명은 [6W Metadata Contract](./docs/architecture/METADATA_CONTRACT.md)를 따릅니다.
- DB, Runtime, Credential 등 운영 내부는 사용자 화면에 노출하지 않습니다.
- Ultra Brain 전용 Governance와 OS Ecosystem의 운영 책임을 혼합하지 않습니다.

## 로컬 실행

    pip install -r requirements.txt
    streamlit run app.py

외부 프로젝트 주소는 `LIVING_OS_URL`, `ULE_URL` Secret 또는 환경 변수로 교체할 수 있습니다. 유효한 HTTP(S) 주소만 링크가 되며 AI Hub는 `?project=ai-hub` 내부 경로를 사용합니다.

## 문서

모든 공식 설계와 수명주기 문서는 [docs](./docs/README.md)에서 관리합니다.

- [Architecture](./docs/architecture/ARCHITECTURE.md)
- [Common UI System](./docs/architecture/UI_SYSTEM.md)
- [Governance 책임 경계](./docs/governance/RESPONSIBILITY_BOUNDARY.md)
- [Registry](./docs/registry/PROJECT_REGISTRY.md)
- [Contract Registry](./docs/registry/CONTRACT_REGISTRY.md)
- [Release](./docs/release/VERSION_HISTORY.md)
- [Capabilities](./docs/capabilities/README.md)
- [VERSION](./VERSION)

## Repository 구조

- `app.py`: 공통 제품 셸, World Explorer와 Streamlit 진입점
- `AI-Hub/`: 내부 AI 운영 구성요소
- `*-Capability/`: 독립 Capability 패키지
- `docs/`: 공식 Architecture, Governance, Registry, Release, Capability 문서
- `tests/`: 제품·문서·회귀 계약 검증
- `Living-OS/`, `Universal-Learning-Engine/`: 독립 연결 프로젝트 작업공간

상세 구조는 [Structure](./docs/architecture/STRUCTURE.md)를 따릅니다.