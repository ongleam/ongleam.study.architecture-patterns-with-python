# Chapter 4: Flask API and Service Layer - 핵심 원칙

## Service Layer란?

**Orchestration Layer** 또는 **Use-Case Layer**라고도 불리며, 워크플로우를 조율하고 시스템의 유스케이스를 정의하는 계층이다.

```
Entrypoints (Flask API)
       ↓
Service Layer (Use Cases)  ← 오케스트레이션 로직
       ↓
Domain Model (Business Logic)
       ↑
Adapters (Repository)
```

## 핵심 원칙

### 1. 관심사의 분리 (Separation of Concerns)

| 계층                    | 책임                                           |
| ----------------------- | ---------------------------------------------- |
| **Entrypoints (Flask)** | HTTP 파싱, JSON 처리, 상태 코드 반환           |
| **Service Layer**       | 유스케이스 오케스트레이션, 검증, 트랜잭션 관리 |
| **Domain Model**        | 순수 비즈니스 로직                             |
| **Adapters**            | 외부 시스템(DB 등)과의 통신                    |

### 2. 전형적인 Service Layer 함수의 단계

```python
def allocate(line: OrderLine, repo: AbstractRepository, session) -> str:
    # 1. Repository에서 객체를 가져온다
    batches = repo.list()

    # 2. 현재 상태에 대한 검증/확인
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f'Invalid sku {line.sku}')

    # 3. Domain Service 호출
    batchref = model.allocate(line, batches)

    # 4. 상태 변경을 저장
    session.commit()

    return batchref
```

### 3. 추상화에 의존하라 (Depend on Abstractions)

```python
def allocate(line: OrderLine, repo: AbstractRepository, session) -> str:
    ...
```

- `AbstractRepository`에 의존함으로써 테스트와 프로덕션에서 다른 구현체 사용 가능
- 테스트: `FakeRepository`
- 프로덕션: `SqlAlchemyRepository`

### 4. FakeRepository를 활용한 빠른 테스트

```python
class FakeRepository(repository.AbstractRepository):
    def __init__(self, batches):
        self._batches = set(batches)

    def add(self, batch):
        self._batches.add(batch)

    def get(self, reference):
        return next(b for b in self._batches if b.reference == reference)

    def list(self):
        return list(self._batches)
```

**테스트 피라미드 최적화:**

- E2E 테스트: Happy path / Unhappy path 최소한으로
- Service Layer 테스트: FakeRepository로 빠른 단위 테스트
- Domain 테스트: 순수 비즈니스 로직 테스트

### 5. 얇은 Entrypoint (Thin Controllers)

```python
@app.route("/allocate", methods=['POST'])
def allocate_endpoint():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    line = model.OrderLine(
        request.json['orderid'],
        request.json['sku'],
        request.json['qty'],
    )

    try:
        batchref = services.allocate(line, repo, session)
    except (model.OutOfStock, services.InvalidSku) as e:
        return {"message": str(e)}, 400

    return {"batchref": batchref}, 201
```

Flask 앱의 책임:

- 세션 관리
- POST 파라미터 파싱
- HTTP 상태 코드 반환
- JSON 응답

## Service Layer의 Trade-offs

### 장점

- 모든 유스케이스를 한 곳에서 관리
- 도메인 로직을 API 뒤에 숨겨 리팩토링 자유도 확보
- "HTTP 처리"와 "비즈니스 로직"의 명확한 분리
- FakeRepository와 함께 사용하면 빠른 테스트 가능

### 단점

- 또 하나의 추상화 계층 추가
- 너무 많은 로직을 Service Layer에 넣으면 **Anemic Domain** 안티패턴 발생
- 순수 웹앱이라면 Controller가 유스케이스 관리 역할을 할 수도 있음

## 권장 디렉토리 구조

```
├── config.py
├── domain/
│   └── model.py           # Entity, Value Object, Domain Service
├── service_layer/
│   └── services.py        # Use Case 함수들
├── adapters/
│   ├── orm.py             # SQLAlchemy 매핑
│   └── repository.py      # Repository 구현
├── entrypoints/
│   └── flask_app.py       # API 엔드포인트
└── tests/
    ├── unit/              # 도메인 + 서비스 레이어 테스트
    ├── integration/       # ORM + Repository 테스트
    └── e2e/               # API 테스트
```

## 두 가지 "Service" 구분

| 종류                                    | 역할                                      | 예시                                |
| --------------------------------------- | ----------------------------------------- | ----------------------------------- |
| **Application Service** (Service Layer) | 외부 요청 처리, 오케스트레이션            | `services.allocate()`               |
| **Domain Service**                      | 도메인 로직이지만 Entity에 속하지 않는 것 | `model.allocate()`, `TaxCalculator` |

## 다음 단계

- Chapter 5: Service Layer를 도메인 객체에서 분리 (Primitive 타입 사용)
- Chapter 6: Unit of Work 패턴으로 session 의존성 제거
