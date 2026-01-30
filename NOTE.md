# Chapter 9. Going to Town on the Message Bus

## 핵심 개념: 메시지 버스 중심 아키텍처

이 장에서는 이벤트를 **선택적 부수효과**에서 **시스템의 핵심 구조**로 전환한다.
애플리케이션 전체가 **메시지 프로세서(Message Processor)**로 변환된다.

```
[Before] 메시지 버스는 선택적 부가 기능
API → Service Layer → Domain Model
                  ↓
            Message Bus (optional side effect)

[After] 메시지 버스가 서비스 레이어의 메인 진입점
API → Message Bus → Event Handlers → Domain Model
```

---

## 1. 아키텍처 변화: 모든 것이 이벤트 핸들러

### 기존 방식: 서비스 함수 + 내부 이벤트 핸들러

```python
# 두 가지 흐름이 존재
# 1. API → 서비스 레이어 함수
# 2. 내부 이벤트 → 핸들러
```

### 새로운 방식: 통합된 이벤트 핸들러

```python
# 모든 흐름이 이벤트로 통합
# API 호출도 이벤트 → 핸들러
# 내부 이벤트도 이벤트 → 핸들러
```

---

## 2. 이벤트 정의: 시스템 입력의 구조화

### 현재 구현된 이벤트 (`src/allocation/domain/events.py`)

```python
class Event:
    pass

@dataclass
class BatchCreated(Event):          # API 입력 → add_batch
    ref: str
    sku: str
    qty: int
    eta: Optional[date] = None

@dataclass
class AllocationRequired(Event):     # API 입력 → allocate
    orderid: str
    sku: str
    qty: int

@dataclass
class BatchQuantityChanged(Event):   # 외부 입력 → change_batch_quantity
    ref: str
    qty: int

@dataclass
class OutOfStock(Event):             # 내부 발생 → send_out_of_stock_notification
    sku: str
```

### 핵심 원칙

- **외부 입력(API)**도 이벤트로 모델링
- **내부 발생 이벤트**와 **외부 입력 이벤트**를 동일하게 처리
- 이벤트는 **도메인 언어**를 반영하는 간단한 dataclass

---

## 3. 핸들러: 서비스 함수의 새로운 모습

### 현재 구현 (`src/allocation/service_layer/handlers.py`)

모든 핸들러가 동일한 시그니처: `(event, uow) -> result`

```python
def add_batch(event: events.BatchCreated, uow: AbstractUnitOfWork):
    with uow:
        product = uow.products.get(sku=event.sku)
        if product is None:
            product = model.Product(sku=event.sku, batches=[])
            uow.products.add(product)
        product.batches.append(model.Batch(event.ref, event.sku, event.qty, event.eta))
        uow.commit()

def allocate(event: events.AllocationRequired, uow: AbstractUnitOfWork) -> str:
    line = OrderLine(event.orderid, event.sku, event.qty)
    with uow:
        product = uow.products.get(sku=line.sku)
        if product is None:
            raise InvalidSku(f"Invalid sku {line.sku}")
        batchref = product.allocate(line)
        uow.commit()
        return batchref

def change_batch_quantity(event: events.BatchQuantityChanged, uow: AbstractUnitOfWork):
    with uow:
        product = uow.products.get_by_batchref(batchref=event.ref)
        product.change_batch_quantity(ref=event.ref, qty=event.qty)
        uow.commit()

def send_out_of_stock_notification(event: events.OutOfStock, uow: AbstractUnitOfWork):
    email.send_mail("stock@made.com", f"Out of stock for {event.sku}")
```

### 핵심 변화

```diff
# Before: 원시 타입 파라미터
- def add_batch(ref: str, sku: str, qty: int, eta: Optional[date], uow):

# After: 이벤트 객체 파라미터
+ def add_batch(event: events.BatchCreated, uow):
```

---

## 4. 메시지 버스: 이벤트 큐 관리

### 현재 구현 (`src/allocation/service_layer/messagebus.py`)

```python
def handle(event: events.Event, uow: AbstractUnitOfWork) -> List:
    results = []
    queue = [event]
    while queue:
        event = queue.pop(0)
        for handler in HANDLERS[type(event)]:
            results.append(handler(event, uow=uow))
            queue.extend(uow.collect_new_events())  # 새 이벤트 수집
    return results

HANDLERS = {
    events.BatchCreated: [handlers.add_batch],
    events.BatchQuantityChanged: [handlers.change_batch_quantity],
    events.AllocationRequired: [handlers.allocate],
    events.OutOfStock: [handlers.send_out_of_stock_notification],
}
```

### 핵심 메커니즘

1. **큐 기반 처리**: 이벤트를 큐에 넣고 순차 처리
2. **UoW에서 이벤트 수집**: 핸들러 실행 후 새로 발생한 이벤트 수집
3. **연쇄 처리**: 새 이벤트는 다시 큐에 추가되어 처리

---

## 5. Unit of Work: 이벤트 수집 책임

### 현재 구현 (`src/allocation/service_layer/unit_of_work.py`)

```python
class AbstractUnitOfWork(abc.ABC):
    products: repository.AbstractRepository

    def collect_new_events(self):
        """Repository가 추적한 모든 Product에서 이벤트 수집"""
        for product in self.products.seen:
            while product.events:
                yield product.events.pop(0)
```

### 핵심 변화

```diff
# Before: UoW가 직접 메시지 버스에 이벤트 발행
- def publish_events(self):
-     for product in self.products.seen:
-         while product.events:
-             messagebus.handle(product.events.pop(0))

# After: UoW는 이벤트를 수집만 하고, 메시지 버스가 가져감
+ def collect_new_events(self):
+     for product in self.products.seen:
+         while product.events:
+             yield product.events.pop(0)
```

**변경 이유**: UoW와 메시지 버스 간의 **순환 의존성 제거**

---

## 6. Repository: seen 추적 패턴

### 현재 구현 (`src/allocation/adapters/repository.py`)

```python
class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen = set()  # 조회/추가된 모든 Aggregate 추적

    def add(self, product: model.Product):
        self._add(product)
        self.seen.add(product)

    def get(self, sku) -> model.Product:
        product = self._get(sku)
        if product:
            self.seen.add(product)
        return product

    def get_by_batchref(self, batchref) -> model.Product:
        product = self._get_by_batchref(batchref)
        if product:
            self.seen.add(product)
        return product
```

### 핵심 원칙

- Repository가 **조회한 모든 Aggregate를 추적**
- UoW가 `seen` 세트를 통해 **이벤트 수집 대상 파악**
- 새로운 쿼리 메서드도 반드시 `seen`에 추가

---

## 7. 도메인 모델: 이벤트 발행

### 현재 구현 (`src/allocation/domain/model.py`)

```python
class Product:
    def __init__(self, sku: str, batches: List[Batch], version_number: int = 0):
        self.events = []  # 이벤트 버퍼

    def allocate(self, line: OrderLine) -> str:
        try:
            batch = next(b for b in sorted(self.batches) if b.can_allocate(line))
            batch.allocate(line)
            return batch.reference
        except StopIteration:
            self.events.append(events.OutOfStock(line.sku))  # 이벤트 발행
            return None

    def change_batch_quantity(self, ref: str, qty: int):
        batch = next(b for b in self.batches if b.reference == ref)
        batch._purchased_quantity = qty
        while batch.available_quantity < 0:
            line = batch.deallocate_one()
            # 재할당 필요 이벤트 발행
            self.events.append(events.AllocationRequired(line.orderid, line.sku, line.qty))
```

### 핵심 원칙

- Aggregate가 **비즈니스 로직 수행 중 이벤트 발행**
- 이벤트는 `events` 리스트에 버퍼링
- 메시지 버스가 나중에 수집하여 처리

---

## 8. API 엔트리포인트: 이벤트 기반 호출

### 현재 구현 (`src/allocation/entrypoints/flask_app.py`)

```python
@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    try:
        # 1. 요청을 이벤트로 변환
        event = events.AllocationRequired(
            request.json["orderid"],
            request.json["sku"],
            request.json["qty"],
        )
        # 2. 메시지 버스에 전달
        results = messagebus.handle(event, unit_of_work.SqlAlchemyUnitOfWork())
        # 3. 결과 반환 (임시 해킹)
        batchref = results.pop(0)
    except handlers.InvalidSku as e:
        return {"message": str(e)}, 400
    return {"batchref": batchref}, 201
```

### 핵심 패턴

1. HTTP 요청 → **이벤트 객체 생성**
2. 이벤트 → **메시지 버스에 전달**
3. 핸들러 결과 → **HTTP 응답으로 변환**

---

## 9. 테스트: 이벤트 기반 테스트

### 현재 구현 (`tests/unit/test_handlers.py`)

```python
def test_allocate_returns_allocation():
    uow = FakeUnitOfWork()
    # 이벤트를 통해 테스트 데이터 설정
    messagebus.handle(events.BatchCreated("batch1", "COMPLICATED-LAMP", 100, None), uow)
    # 이벤트를 통해 기능 테스트
    results = messagebus.handle(
        events.AllocationRequired("o1", "COMPLICATED-LAMP", 10), uow
    )
    assert results[0] == "batch1"

def test_reallocates_if_necessary():
    uow = FakeUnitOfWork()
    # 이벤트 히스토리로 시나리오 구성
    event_history = [
        events.BatchCreated("batch1", "INDIFFERENT-TABLE", 50, None),
        events.BatchCreated("batch2", "INDIFFERENT-TABLE", 50, None),
        events.AllocationRequired("order1", "INDIFFERENT-TABLE", 20),
        events.AllocationRequired("order2", "INDIFFERENT-TABLE", 20),
    ]
    for e in event_history:
        messagebus.handle(e, uow)

    # 이벤트 연쇄 테스트: BatchQuantityChanged → AllocationRequired
    messagebus.handle(events.BatchQuantityChanged("batch1", 25), uow)

    [batch1, batch2] = uow.products.get(sku="INDIFFERENT-TABLE").batches
    assert batch1.available_quantity == 5
    assert batch2.available_quantity == 30
```

### 핵심 변화

```diff
# Before: 서비스 함수 직접 호출
- services.add_batch("b1", "CRUNCHY-ARMCHAIR", 100, None, uow)

# After: 이벤트 + 메시지 버스
+ messagebus.handle(events.BatchCreated("b1", "CRUNCHY-ARMCHAIR", 100, None), uow)
```

---

## 10. 이벤트 연쇄 처리 플로우

### BatchQuantityChanged 시나리오

```
1. API/외부 시스템 → BatchQuantityChanged 이벤트 발생

2. Message Bus가 이벤트 수신
   └→ change_batch_quantity 핸들러 호출

3. change_batch_quantity 핸들러
   └→ product.change_batch_quantity() 호출
   └→ 배치 수량 변경
   └→ 할당량 초과 시 deallocate_one() 실행
   └→ AllocationRequired 이벤트 발행 (product.events에 추가)

4. 핸들러 종료 후 Message Bus가 uow.collect_new_events() 호출
   └→ AllocationRequired 이벤트 수집
   └→ 큐에 추가

5. Message Bus가 AllocationRequired 처리
   └→ allocate 핸들러 호출
   └→ 재할당 수행
```

---

## 핵심 원칙 요약

| 원칙                      | 설명                                             |
| ------------------------- | ------------------------------------------------ |
| **Single Entry Point**    | 모든 요청(외부/내부)이 메시지 버스를 통해 진입   |
| **Event as Interface**    | 원시 타입 대신 이벤트 객체로 시스템 입력 정의    |
| **Handler Unification**   | 서비스 함수와 이벤트 핸들러를 동일한 형태로 통합 |
| **Event Chaining**        | 핸들러가 새 이벤트를 발행하여 연쇄 처리 가능     |
| **UoW Event Collection**  | UoW가 이벤트 수집 책임, 메시지 버스가 처리 책임  |
| **Single Responsibility** | 각 핸들러는 하나의 이벤트만 처리                 |

---

## Trade-offs

### 장점

- 핸들러와 서비스가 동일 → 개념 단순화
- 입력이 구조화된 이벤트 객체 → 명확한 API
- 새로운 요구사항을 새 이벤트 + 핸들러로 해결 → 확장성
- 이벤트 연쇄로 복잡한 워크플로우 처리 → 유연성

### 단점

- 메시지 버스 기반 처리 → 언제 끝나는지 예측 어려움
- 모델 객체와 이벤트 간 필드 중복 → 유지보수 비용
- 결과 반환 해킹 필요 → 읽기/쓰기 책임 혼합 (Chapter 12에서 해결)

---

## 의존성 흐름

```
flask_app.py (Entrypoint)
    │
    ├── events.py (Domain Events)
    ├── messagebus.py (Service Layer)
    │       │
    │       └── handlers.py (Service Layer)
    │               │
    │               ├── model.py (Domain)
    │               └── unit_of_work.py (Service Layer)
    │                       │
    │                       └── repository.py (Adapter)
    │
    └── unit_of_work.py
```

**핵심**: 메시지 버스가 서비스 레이어의 **단일 진입점**이 됨
