# Chapter 6: Unit of Work Pattern - 핵심 원칙

## 현재 디렉토리 구조

```
src/allocation/
├── domain/
│   └── model.py              # 순수 도메인 모델 (Entity, Value Object, Domain Service)
├── adapters/
│   ├── orm.py                # SQLAlchemy Classical Mapping
│   └── repository.py         # Repository 추상화 및 구현
├── service_layer/
│   ├── services.py           # 애플리케이션 서비스 (Use Cases)
│   └── unit_of_work.py       # Unit of Work 추상화 및 구현
├── entrypoints/
│   └── flask_app.py          # API 진입점
└── config.py                 # 환경 설정

tests/
├── unit/                     # 도메인 및 서비스 레이어 단위 테스트
├── integration/              # ORM, Repository, UoW 통합 테스트
└── e2e/                      # API 엔드투엔드 테스트
```

## 핵심 원칙

### 1. Unit of Work의 역할

**Unit of Work는 원자적 연산(Atomic Operations)에 대한 추상화이다.**

- Repository 패턴이 영속 저장소에 대한 추상화라면, UoW는 **트랜잭션 경계**에 대한 추상화
- 서비스 레이어를 데이터 레이어로부터 완전히 분리시키는 마지막 퍼즐 조각

```python
# Before UoW: API가 3개 레이어와 직접 통신
API → Database (session)
API → Repository
API → Service Layer

# After UoW: API는 UoW 초기화와 서비스 호출만 담당
API → UoW → (Repository + Database)
API → Service Layer
```

### 2. Context Manager를 통한 트랜잭션 관리

```python
class AbstractUnitOfWork(abc.ABC):
    batches: repository.AbstractRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()  # 기본 동작은 롤백 (안전한 기본값)

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError
```

**Python Context Manager의 장점:**

- `with` 블록으로 원자적 연산의 범위를 시각적으로 명확히 표현
- `__exit__`에서 자동 롤백으로 **안전한 기본 동작** 보장
- 예외 발생 시에도 리소스 정리 보장

### 3. 명시적 커밋 (Explicit Commit)

```python
def allocate(orderid: str, sku: str, qty: int, uow: AbstractUnitOfWork) -> str:
    line = OrderLine(orderid, sku, qty)
    with uow:
        batches = uow.batches.list()
        if not is_valid_sku(line.sku, batches):
            raise InvalidSku(f"Invalid sku {line.sku}")
        batchref = model.allocate(line, batches)
        uow.commit()  # 명시적 커밋
    return batchref
```

**명시적 커밋 vs 암묵적 커밋:**

| 방식        | 장점                                                    | 단점                         |
| ----------- | ------------------------------------------------------- | ---------------------------- |
| 명시적 커밋 | 변경이 일어나는 경로가 하나뿐 (전체 성공 + 명시적 커밋) | 코드 한 줄 추가              |
| 암묵적 커밋 | 코드가 더 짧음                                          | 예상치 못한 상태 변경 가능성 |

**"Safe by Default"**: 명시적 커밋을 선호하면 시스템이 기본적으로 안전

### 4. UoW와 Repository의 협업

```python
class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.batches = repository.SqlAlchemyRepository(self.session)  # Repository 생성
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()  # 세션 정리
```

**UoW가 Repository를 소유:**

- `uow.batches`로 Repository에 접근
- Session lifecycle은 UoW가 관리
- Repository는 Session을 주입받아 사용

### 5. Fake UoW를 통한 테스트

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


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.batches = FakeRepository([])
        self.committed = False  # 커밋 여부 추적

    def commit(self):
        self.committed = True

    def rollback(self):
        pass
```

**"Don't Mock What You Don't Own":**

- SQLAlchemy Session을 직접 Mocking하지 않음
- 대신 우리가 정의한 추상화(UoW, Repository)를 Fake로 구현
- 테스트가 더 간결하고 유지보수 용이

### 6. 서비스 레이어의 단순화

```python
# Before: Session과 Repository를 모두 받음
def allocate(orderid, sku, qty, repo: AbstractRepository, session) -> str:
    ...

# After: UoW 하나만 받음
def allocate(orderid, sku, qty, uow: AbstractUnitOfWork) -> str:
    ...
```

**서비스 함수의 의존성이 하나로 단순화:**

- Repository 접근: `uow.batches`
- 트랜잭션 관리: `uow.commit()`, `uow.rollback()`

### 7. 엔트리포인트의 책임

```python
@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    try:
        batchref = services.allocate(
            request.json["orderid"],
            request.json["sku"],
            request.json["qty"],
            unit_of_work.SqlAlchemyUnitOfWork(),  # 구체 구현 주입
        )
    except (model.OutOfStock, services.InvalidSku) as e:
        return {"message": str(e)}, 400
    return {"batchref": batchref}, 201
```

**Flask API의 책임:**

1. UoW 초기화 (구체 구현 선택)
2. 서비스 함수 호출
3. 예외를 HTTP 응답으로 변환

### 8. 의존성 역전 원칙 (DIP) 적용

```
┌─────────────────────────────────────────────────────────────┐
│                       Entrypoints                           │
│   (Flask API - 구체적인 UoW 주입)                            │
└─────────────────────────┬───────────────────────────────────┘
                          │ depends on
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                     Service Layer                            │
│   (AbstractUnitOfWork에 의존 - 추상화)                       │
└─────────────────────────┬───────────────────────────────────┘
                          │ depends on
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                      Domain Model                            │
│   (순수 비즈니스 로직 - 외부 의존성 없음)                     │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │ implements
┌─────────────────────────────────────────────────────────────┐
│                        Adapters                              │
│   (SqlAlchemyUnitOfWork, SqlAlchemyRepository)              │
└─────────────────────────────────────────────────────────────┘
```

## Trade-offs

### 장점

- 원자적 연산에 대한 명확한 추상화
- Context Manager로 트랜잭션 범위의 시각적 표현
- 트랜잭션 시작/종료에 대한 명시적 제어
- 부분 커밋 걱정 없음 (안전한 기본 동작)
- Repository 접근을 위한 편리한 진입점
- 테스트에서 Fake 구현으로 쉽게 대체 가능

### 단점

- ORM이 이미 비슷한 추상화 제공 (SQLAlchemy Session)
- Rollback, 멀티스레딩, 중첩 트랜잭션 등 복잡한 케이스 고려 필요
- 단순한 애플리케이션에는 과도한 추상화일 수 있음

## 핵심 요약

> **Unit of Work 패턴은 데이터 무결성에 대한 추상화이다.**
>
> - Repository + Service Layer 패턴과 함께 사용하여 원자적 업데이트를 표현
> - 각 서비스 레이어 유스케이스는 단일 Unit of Work 내에서 성공하거나 실패
> - Context Manager는 Python에서 범위를 정의하는 관용적 방법
> - 기본적으로 롤백하여 시스템을 안전하게 유지
> - SQLAlchemy Session 위에 더 단순한 추상화를 도입하여 ORM과의 결합도를 낮춤
