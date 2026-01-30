# Chapter 7: Aggregates and Consistency Boundaries

## 핵심 개념

### Aggregate란?

**Aggregate**는 관련된 객체들의 클러스터로, 데이터 변경을 위한 하나의 단위로 취급된다.

> "An AGGREGATE is a cluster of associated objects that we treat as a unit for the purpose of data changes."
> — Eric Evans, Domain-Driven Design

### 왜 Aggregate가 필요한가?

1. **불변식(Invariants) 보장**: 비즈니스 규칙을 항상 만족시키기 위함
2. **동시성 제어**: 전체 테이블 잠금 없이 성능 최적화
3. **일관성 경계**: 트랜잭션의 범위를 명확히 정의

---

## 현재 코드베이스 구현

### 1. Product Aggregate (Aggregate Root)

```python
# src/allocation/domain/model.py
class Product:
    def __init__(self, sku: str, batches: List[Batch], version_number: int = 0):
        self.sku = sku
        self.batches = batches
        self.version_number = version_number

    def allocate(self, line: OrderLine) -> str:
        try:
            batch = next(b for b in sorted(self.batches) if b.can_allocate(line))
            batch.allocate(line)
            self.version_number += 1
            return batch.reference
        except StopIteration:
            raise OutOfStock(f"Out of stock for sku {line.sku}")
```

**주요 특징**:

- `sku`가 Product의 식별자
- `batches` 컬렉션을 내부에 포함
- `allocate()` 도메인 서비스가 Aggregate 메서드로 이동
- `version_number`로 낙관적 동시성 제어

### 2. One Aggregate = One Repository

```python
# src/allocation/adapters/repository.py
class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, product: model.Product):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, sku) -> model.Product:
        raise NotImplementedError
```

**원칙**: Repository는 오직 Aggregate만 반환해야 한다.

- `BatchRepository` → `ProductRepository`로 변경
- 외부에서 Batch에 직접 접근 불가

### 3. 낙관적 동시성 제어 (Optimistic Concurrency)

```python
# src/allocation/service_layer/unit_of_work.py
DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        config.get_postgres_uri(),
        isolation_level="REPEATABLE READ",
    )
)
```

**동작 방식**:

1. 두 트랜잭션이 동시에 같은 Product를 읽음 (version=3)
2. 둘 다 `allocate()` 호출하여 version을 4로 증가
3. DB 격리 수준으로 인해 하나만 커밋 성공, 다른 하나는 실패
4. 실패한 트랜잭션은 재시도

### 4. ORM 매핑

```python
# src/allocation/adapters/orm.py
products = Table(
    "products",
    metadata,
    Column("sku", String(255), primary_key=True),
    Column("version_number", Integer, nullable=False, server_default="0"),
)

# Product → Batch 관계
mapper(
    model.Product, products, properties={"batches": relationship(batches_mapper)}
)
```

---

## 핵심 원칙 정리

### 1. Aggregate는 일관성 경계이다

```
┌─────────────────────────────────────┐
│            Product (Aggregate)       │
│  ┌─────────┐  ┌─────────┐           │
│  │ Batch 1 │  │ Batch 2 │  ...      │
│  └─────────┘  └─────────┘           │
│                                      │
│  불변식: 주문라인은 하나의 배치에만    │
│         할당될 수 있다                │
└─────────────────────────────────────┘
```

- 같은 SKU의 Batch들은 함께 일관성을 유지해야 함
- 다른 SKU끼리는 동시 수정 가능 (DEADLY-SPOON ↔ FLIMSY-DESK)

### 2. Aggregate의 크기는 작게

- 성능을 위해 가능한 작은 단위로 설계
- 우리 선택: SKU 단위 (Product)
- 대안들: Shipment, Warehouse (너무 큼)

### 3. 접근 규칙

| 규칙       | 설명                               |
| ---------- | ---------------------------------- |
| 외부 접근  | Aggregate Root(Product)를 통해서만 |
| 내부 수정  | Aggregate 메서드를 통해서만        |
| Repository | Aggregate만 반환                   |
| 트랜잭션   | 하나의 Aggregate만 수정            |

### 4. Version Number 전략

**세 가지 구현 옵션**:

1. ✅ **도메인에서 관리** (현재 구현) - 가장 명시적
2. 서비스 레이어에서 관리 - 책임 혼재
3. 인프라에서 자동 관리 - 불필요한 증가 발생 가능

---

## Service Layer 변경점

```python
# Before: 도메인 서비스 직접 호출
batches = uow.batches.list()
batchref = allocate(line, batches)

# After: Aggregate를 통한 호출
product = uow.products.get(sku=line.sku)
batchref = product.allocate(line)
```

---

## Trade-offs

### 장점

| 장점      | 설명                                   |
| --------- | -------------------------------------- |
| 캡슐화    | 도메인 모델의 public/private 구분 명확 |
| 성능      | ORM 성능 문제 방지                     |
| 추론 용이 | 상태 변경 책임이 명확                  |

### 단점

| 단점        | 설명                                             |
| ----------- | ------------------------------------------------ |
| 학습 곡선   | Entity, Value Object에 더해 새로운 개념          |
| 사고 전환   | "한 번에 하나의 Aggregate만 수정" 원칙 적응 필요 |
| 최종 일관성 | Aggregate 간 일관성 처리가 복잡                  |

---

## Bounded Context와의 관계

```
┌─────────────────────────────┐  ┌─────────────────────────────┐
│     Allocation Service       │  │      E-commerce Service     │
├─────────────────────────────┤  ├─────────────────────────────┤
│ Product(sku, batches)        │  │ Product(sku, description,   │
│                              │  │         price, image_url,   │
│ - 할당에 필요한 것만         │  │         dimensions...)      │
└─────────────────────────────┘  └─────────────────────────────┘
```

> 도메인 모델은 계산에 필요한 데이터만 포함해야 한다.

---

## 핵심 정리

1. **Aggregate = 도메인 모델의 진입점**
   - 변경 방법을 제한하여 시스템 추론을 쉽게 만듦

2. **Aggregate = 일관성 경계**
   - 비즈니스 규칙과 불변식을 그룹 내에서 보장

3. **Aggregate와 동시성은 함께 간다**
   - 올바른 Aggregate 선택은 성능과 개념적 구조 모두에 영향
