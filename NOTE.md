# Chapter 5. TDD in High Gear and Low Gear

## 핵심 원칙

### 1. 테스트 피라미드 (Test Pyramid)

```
       /\        E2E 테스트 (2개) - API 레벨
      /  \
     /----\      통합 테스트 (8개) - ORM, Repository
    /      \
   /--------\    유닛 테스트 (15개) - 서비스 레이어 + 도메인 모델
```

**목표**: 유닛 테스트가 가장 많고, E2E 테스트는 최소화

### 2. High Gear vs Low Gear

| 상황                     | 기어      | 테스트 대상   | 특징                   |
| ------------------------ | --------- | ------------- | ---------------------- |
| 새 기능 추가, 버그 수정  | High Gear | 서비스 레이어 | 낮은 커플링, 빠른 개발 |
| 새 프로젝트, 복잡한 문제 | Low Gear  | 도메인 모델   | 높은 피드백, 설계 검증 |

**비유**: 자전거 기어

- Low Gear: 출발할 때, 언덕을 오를 때 (관성 극복)
- High Gear: 속도가 붙은 후 (효율적 이동)

### 3. 서비스 레이어 테스트의 장점

```python
# 도메인 모델에 직접 의존하지 않음
def test_allocate_returns_allocation():
    repo, session = FakeRepository([]), FakeSession()
    services.add_batch("batch1", "LAMP", 100, None, repo, session)
    result = services.allocate("o1", "LAMP", 10, repo, session)
    assert result == "batch1"
```

- 도메인 모델 리팩토링 시 테스트 수정 불필요
- "private" 메서드/속성에 의존하지 않음
- 테스트 = 접착제 → 저수준 테스트가 많을수록 변경이 어려움

### 4. 서비스 레이어 API를 프리미티브로 표현

```python
# Before: 도메인 객체 사용
def allocate(line: OrderLine, repo, session) -> str:

# After: 프리미티브 타입 사용
def allocate(orderid: str, sku: str, qty: int, repo, session) -> str:
```

### 5. 누락된 서비스 추가하기

도메인 레이어 직접 조작이 필요하면 → 서비스가 불완전한 신호

```python
# add_batch 서비스 추가로 테스트에서 도메인 객체 직접 생성 제거
def add_batch(ref: str, sku: str, qty: int, eta: Optional[date],
              repo: AbstractRepository, session) -> None:
    repo.add(model.Batch(ref, sku, qty, eta))
    session.commit()
```

### 6. E2E 테스트도 API만 사용

```python
# add_stock SQL fixture 대신 API 호출
def post_to_add_batch(ref, sku, qty, eta):
    r = requests.post(f'{url}/add_batch', json={...})
    assert r.status_code == 201
```

## 테스트 유형별 가이드라인

| 테스트 유형   | 목적                          | 수량        |
| ------------- | ----------------------------- | ----------- |
| E2E           | 기능 동작 확인, 통합 검증     | 기능당 1개  |
| 서비스 레이어 | 비즈니스 로직, 엣지 케이스    | 대부분      |
| 도메인 모델   | 핵심 도메인 로직, 설계 피드백 | 소규모 유지 |

## 현재 프로젝트 적용 현황

```
tests/
├── unit/
│   ├── test_batches.py    # 8개 - 도메인 모델 (Low Gear)
│   ├── test_allocate.py   # 4개 - 도메인 모델 (Low Gear)
│   └── test_services.py   # 4개 - 서비스 레이어 (High Gear) ✓
├── integration/
│   ├── test_orm.py        # ORM 매핑 검증
│   └── test_repository.py # Repository 동작 검증
└── e2e/
    └── test_api.py        # 2개 - API 레벨 ✓
```

**구현 완료 항목**:

- [x] 서비스 레이어가 프리미티브 타입 사용
- [x] `add_batch` 서비스 함수 추가
- [x] 서비스 레이어 테스트가 서비스 함수만 사용
- [x] E2E 테스트가 `post_to_add_batch` 헬퍼 사용
- [x] 도메인 모델 테스트 유지 (설계 피드백용)
