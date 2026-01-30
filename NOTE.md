# Chapter 8. Events and the Message Bus - 핵심 원칙

## 핵심 문제: 부수 효과(Side Effects)의 분리

비즈니스 요구사항 중 핵심 도메인과 무관한 "부가 기능"(예: 재고 부족 시 이메일 알림)을 어디에 배치할 것인가?

### 잘못된 접근 방식들

| 위치               | 문제점                                        |
| ------------------ | --------------------------------------------- |
| **Web Controller** | HTTP 레이어의 책임이 아님, 단위 테스트 어려움 |
| **Domain Model**   | 인프라 의존성 유입, 도메인 순수성 훼손        |
| **Service Layer**  | try/except 중첩, SRP 위반                     |

## 핵심 패턴

### 1. Domain Events (도메인 이벤트)

도메인에서 발생한 "사실(fact)"을 기록하는 순수 데이터 구조.

```python
# src/allocation/domain/events.py
@dataclass
class OutOfStock(Event):
    sku: str
```

**원칙:**

- 이벤트는 Value Object - 행위 없이 순수 데이터만 보유
- 도메인 언어로 이름 지정 (OutOfStock, Allocated 등)
- 예외 대신 이벤트 사용 - 제어 흐름에 예외 사용 지양

### 2. Message Bus (메시지 버스)

이벤트를 핸들러에 매핑하는 단순 Publish-Subscribe 시스템.

```python
# src/allocation/service_layer/messagebus.py
HANDLERS = {
    events.OutOfStock: [send_out_of_stock_notification],
}

def handle(event: events.Event):
    for handler in HANDLERS[type(event)]:
        handler(event)
```

**원칙:**

- 메시지 버스는 "dumb infrastructure" - 이벤트 의미를 모름
- 동기 실행 - 모든 핸들러 완료까지 대기
- 단일 책임 분리 - 각 핸들러는 하나의 부수 효과만 담당

## 구현 옵션 비교

### Option 1: Service Layer가 이벤트 발행

```python
# services.py
batchref = product.allocate(line)
uow.commit()
messagebus.handle(product.events)  # 명시적 발행
```

### Option 2: Service Layer가 직접 이벤트 생성

```python
# services.py
if batchref is None:
    messagebus.handle(events.OutOfStock(line.sku))  # 직접 생성
```

### Option 3: UoW가 이벤트 수집 및 발행 (권장)

**현재 구현된 방식:**

```python
# unit_of_work.py
def commit(self):
    self._commit()
    self.publish_events()  # 자동 발행

def publish_events(self):
    for product in self.products.seen:  # Repository가 추적
        while product.events:
            event = product.events.pop(0)
            messagebus.handle(event)
```

## 아키텍처 플로우

```
┌─────────────────────────────────────────────────────────────────┐
│                        Entrypoint (API)                         │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Service Layer                             │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  with uow:                                               │   │
│  │      product = uow.products.get(sku)  ──────────────────────▶ Repository.seen에 추가
│  │      product.allocate(line)  ─────────────────────────────────▶ events 리스트에 기록
│  │      uow.commit()  ─────────────────────────────────────────▶ publish_events() 호출
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Message Bus                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  OutOfStock → [send_out_of_stock_notification]          │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Event Handler (Adapter)                      │
│  email.send_mail("stock@made.com", ...)                        │
└─────────────────────────────────────────────────────────────────┘
```

## 현재 코드베이스 구조

| 파일                            | 역할                                           |
| ------------------------------- | ---------------------------------------------- |
| `domain/events.py`              | Event 기본 클래스, OutOfStock 이벤트 정의      |
| `domain/model.py`               | Product.events 리스트에 이벤트 기록            |
| `adapters/repository.py`        | `.seen` 속성으로 사용된 Aggregate 추적         |
| `service_layer/unit_of_work.py` | commit() 시 publish_events() 자동 호출         |
| `service_layer/messagebus.py`   | 이벤트-핸들러 매핑 및 dispatch                 |
| `service_layer/services.py`     | 깔끔한 유스케이스 코드 (이벤트 처리 코드 없음) |

## SRP (단일 책임 원칙) 적용

> "함수가 하는 일을 'then'이나 'and' 없이 설명할 수 없다면, SRP를 위반하고 있는 것이다."

**Before:**

- `allocate_and_send_mail_if_out_of_stock` ❌

**After:**

- `allocate` → 할당 로직만 담당
- `OutOfStock` 이벤트 → 재고 부족 사실 기록
- `send_out_of_stock_notification` 핸들러 → 이메일 발송만 담당 ✅

## Trade-offs

### 장점

- 책임 분리 - 요청에 대한 여러 액션을 분리
- 느슨한 결합 - 핸들러 구현을 쉽게 변경 가능
- 비즈니스 언어 반영 - 이벤트가 도메인 모델의 일부

### 단점

- 추가 복잡성 - commit() 시 이메일 발송되는 "마법" 존재
- 동기 실행 - 모든 핸들러 완료까지 대기 (성능 이슈 가능)
- 추적 어려움 - 이벤트 체인으로 인한 워크플로우 파악 난이도 증가
- 순환 의존성/무한 루프 위험

## 핵심 인사이트

1. **"When X, then Y"** 패턴 → 이벤트로 모델링
2. **도메인 모델의 역할**: 재고가 없다는 "사실"을 아는 것
3. **핸들러의 역할**: 그 사실에 대해 "행동"하는 것
4. **이벤트를 통한 Eventual Consistency**: 서로 다른 Aggregate 간 일관성 유지
