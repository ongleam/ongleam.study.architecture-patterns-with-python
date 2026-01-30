# Chapter 1: Domain Modeling - 핵심 원칙 정리

## Domain Model이란?

- **Domain**: 해결하려는 비즈니스 문제 영역
- **Model**: 현상의 유용한 속성을 포착한 지도(map)
- **Domain Model**: 비즈니스 전문가들의 멘탈 모델을 코드로 표현한 것

> "소프트웨어에서 가장 중요한 것은 문제에 대한 유용한 모델을 제공하는 것이다." - DDD

## 핵심 패턴

### 1. Value Object (값 객체)

**정의**: 데이터로만 식별되는 객체. 속성이 바뀌면 다른 객체가 됨.

**특징**:

- 불변(immutable)
- 값 동등성(value equality): 모든 속성이 같으면 같은 객체
- `dataclass(frozen=True)` 또는 `NamedTuple` 사용

```python
@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int
```

**예시**: 돈(Money), 이름(Name), 주문라인(OrderLine)

- 10파운드 지폐 두 장은 같은 가치 = 동등함

### 2. Entity (엔티티)

**정의**: 고유한 식별자를 가진 객체. 속성이 변해도 동일한 객체.

**특징**:

- 식별자 동등성(identity equality)
- 시간이 지나도 동일성 유지
- `__eq__`와 `__hash__` 구현 필요

```python
class Batch:
    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)
```

**예시**: 사람(Person), 배치(Batch)

- 해리가 이름을 배리로 바꿔도 같은 사람

### 3. Domain Service (도메인 서비스)

**정의**: Entity나 Value Object에 자연스럽게 속하지 않는 비즈니스 로직.

> "때로는 그냥 '것(thing)'이 아니다." - Eric Evans

**특징**:

- Python은 다중 패러다임 → 함수로 구현 가능
- `FooManager`, `BarBuilder` 대신 `manage_foo()`, `build_bar()`

```python
def allocate(line: OrderLine, batches: List[Batch]) -> str:
    batch = next(b for b in sorted(batches) if b.can_allocate(line))
    batch.allocate(line)
    return batch.reference
```

### 4. Domain Exception (도메인 예외)

**정의**: 도메인 개념을 예외로 표현.

```python
class OutOfStock(Exception):
    pass

# 사용
raise OutOfStock(f"Out of stock for sku {line.sku}")
```

**원칙**: Ubiquitous Language로 명명

## Python Magic Methods 활용

도메인 모델을 Pythonic하게 만들기:

| Magic Method | 용도               | 예시                |
| ------------ | ------------------ | ------------------- |
| `__eq__`     | 동등성 비교 (`==`) | Entity 식별자 비교  |
| `__hash__`   | Set/Dict 키 사용   | Entity를 Set에 저장 |
| `__gt__`     | 정렬 (`sorted()`)  | Batch를 ETA 순 정렬 |
| `__repr__`   | 디버깅 출력        | `<Batch batch-001>` |

```python
def __gt__(self, other):
    if self.eta is None:
        return False  # 창고 재고 우선
    if other.eta is None:
        return True
    return self.eta > other.eta
```

## Ubiquitous Language (보편 언어)

- 비즈니스 전문가와 개발자가 **같은 용어** 사용
- 코드에서 비즈니스 용어 그대로 사용: `Batch`, `OrderLine`, `allocate`, `OutOfStock`
- 테스트도 비즈니스 언어로 작성 → 비개발자도 읽을 수 있음

```python
def test_prefers_current_stock_batches_to_shipments():
    # 비즈니스 전문가도 이해할 수 있는 테스트
    ...
```

## 설계 원칙 요약

| 원칙                            | 설명                                        |
| ------------------------------- | ------------------------------------------- |
| **Domain Model은 순수해야 함**  | 프레임워크 의존성 없이 순수 Python          |
| **Entity vs Value Object 구분** | 식별자가 있으면 Entity, 없으면 Value Object |
| **함수도 OK**                   | 모든 것이 객체일 필요 없음                  |
| **도메인 언어 사용**            | 코드가 비즈니스를 반영                      |
| **불변성 선호**                 | Value Object는 frozen으로                   |

## 이 챕터의 도메인 모델

```
┌─────────────────────────────────────────────────┐
│                  allocate()                     │
│              (Domain Service)                   │
└─────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│                   Batch                         │
│                 (Entity)                        │
│  - reference (식별자)                           │
│  - sku                                          │
│  - eta                                          │
│  - _purchased_quantity                          │
│  - _allocations: Set[OrderLine]                 │
└─────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│                 OrderLine                       │
│              (Value Object)                     │
│  - orderid                                      │
│  - sku                                          │
│  - qty                                          │
└─────────────────────────────────────────────────┘
```

## 다음 챕터 예고

> "도메인 서비스를 첫 번째 유스케이스에 사용할 수 있다. 하지만 먼저 데이터베이스가 필요하다..."

→ Chapter 2: Repository Pattern
