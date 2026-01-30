# Chapter 2: Repository Pattern - 핵심 원칙 정리

## 1. 의존성 역전 원칙 (Dependency Inversion Principle)

### 전통적인 방식 vs 역전된 방식

```
[전통적 계층 아키텍처]
UI → Business Logic → Database
     (모델이 ORM에 의존)

[역전된 아키텍처 - Onion/Hexagonal]
Entrypoints → Service Layer → Domain Model ← Adapters(ORM, Repository)
              (ORM이 모델에 의존)
```

### 현재 코드베이스에서의 구현

**orm.py** - ORM이 도메인 모델을 import

```python
import model  # ORM이 모델에 의존

def start_mappers():
    lines_mapper = mapper(model.OrderLine, order_lines)
    mapper(model.Batch, batches, ...)
```

**model.py** - 순수 Python 클래스, ORM/DB 의존성 없음

```python
@dataclass(unsafe_hash=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int

class Batch:
    # SQLAlchemy, 데이터베이스 관련 코드 전혀 없음
```

## 2. Classical Mapping vs Declarative Mapping

### Declarative (일반적인 방식 - 사용하지 않음)

```python
# 모델이 ORM에 의존 - BAD
class OrderLine(Base):
    id = Column(Integer, primary_key=True)
    sku = Column(String(250))
```

### Classical Mapping (현재 코드베이스 - 권장)

```python
# 테이블 정의와 모델 분리
order_lines = Table(
    "order_lines", metadata,
    Column("id", Integer, primary_key=True),
    Column("sku", String(255)),
    ...
)

# 명시적 매핑
def start_mappers():
    mapper(model.OrderLine, order_lines)
```

**장점**: 도메인 모델이 데이터베이스 기술에서 완전히 분리됨

## 3. Repository Pattern

### 핵심 개념

- 영속성 저장소에 대한 **추상화**
- 모든 데이터가 메모리에 있는 것처럼 가장
- 데이터 접근의 복잡성을 숨김

### 인터페이스 (Port)

```python
# repository.py
class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch: model.Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> model.Batch:
        raise NotImplementedError
```

### 구현체 (Adapter)

```python
class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, batch):
        self.session.add(batch)

    def get(self, reference):
        return self.session.query(model.Batch).filter_by(reference=reference).one()
```

## 4. Port와 Adapter

| 구분        | 설명                                       | 현재 코드베이스                          |
| ----------- | ------------------------------------------ | ---------------------------------------- |
| **Port**    | 애플리케이션과 외부 세계 사이의 인터페이스 | `AbstractRepository`                     |
| **Adapter** | 인터페이스의 구현체                        | `SqlAlchemyRepository`, `FakeRepository` |

## 5. 테스트 전략

### 테스트 피라미드

```
tests/
├── unit/           # 도메인 모델 테스트 (I/O 없음)
├── integration/    # Repository, ORM 테스트 (DB 사용)
└── e2e/            # API 테스트
```

### ORM 테스트 (test_orm.py)

- 매핑 설정이 올바른지 검증
- 초기 설정 시 유용, 이후 삭제 가능

```python
def test_orderline_mapper_can_load_lines(session):
    session.execute("INSERT INTO order_lines ...")
    assert session.query(model.OrderLine).all() == expected
```

### Repository 테스트 (test_repository.py)

- 장기적으로 유지할 가치 있는 테스트
- Raw SQL로 데이터 준비 → Repository로 조회 검증

```python
def test_repository_can_retrieve_a_batch_with_allocations(session):
    # Raw SQL로 테스트 데이터 준비
    orderline_id = insert_order_line(session)
    batch1_id = insert_batch(session, "batch1")
    insert_allocation(session, orderline_id, batch1_id)

    # Repository로 조회
    repo = repository.SqlAlchemyRepository(session)
    retrieved = repo.get("batch1")

    # 검증
    assert retrieved._allocations == {model.OrderLine("order1", "GENERIC-SOFA", 12)}
```

## 6. Fake Repository 패턴

```python
class FakeRepository(AbstractRepository):
    def __init__(self, batches):
        self._batches = set(batches)

    def add(self, batch):
        self._batches.add(batch)

    def get(self, reference):
        return next(b for b in self._batches if b.reference == reference)
```

**장점**:

- 단위 테스트에서 DB 없이 빠르게 테스트 가능
- 인프라 걱정 없이 비즈니스 로직에 집중

## 7. 설계 원칙 요약

### commit()은 Repository 외부에서

```python
repo.add(batch)
session.commit()  # 호출자의 책임 (Unit of Work 패턴과 연결)
```

### 단순한 인터페이스 유지

- `add()`: 새 객체 추가
- `get()`: 객체 조회
- `list()`: 전체 목록 (선택적)

### Trade-offs

| 장점                                          | 단점                             |
| --------------------------------------------- | -------------------------------- |
| 영속성과 도메인 모델 사이의 단순한 인터페이스 | ORM 매핑 수동 관리 필요          |
| 테스트용 Fake 구현이 쉬움                     | 추가 추상화 계층 = 유지보수 비용 |
| 저장소 변경이 용이                            | Python 개발자에게 낯선 패턴      |
| 비즈니스 문제에 먼저 집중 가능                |                                  |

## 8. 파일 구조

```
.
├── model.py           # 도메인 모델 (순수 Python)
├── orm.py             # SQLAlchemy 테이블 정의 + 매퍼
├── repository.py      # Repository 추상화 + 구현
├── conftest.py        # pytest fixtures (in_memory_db, session)
├── test_batches.py    # 단위 테스트 (Batch 동작)
├── test_allocate.py   # 단위 테스트 (allocate 함수)
├── test_orm.py        # 통합 테스트 (ORM 매핑)
└── test_repository.py # 통합 테스트 (Repository)
```

## 9. 핵심 교훈

> "추상화를 Fake로 만들기 어렵다면, 그 추상화는 아마도 너무 복잡한 것이다."

> "앱이 단순한 CRUD 래퍼라면 도메인 모델이나 Repository가 필요 없다.
> 하지만 도메인이 복잡해질수록 인프라 관심사에서 자유로워지는 투자가
> 변경 용이성 측면에서 보상받게 된다."
