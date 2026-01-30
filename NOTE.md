# Chapter 3: On Coupling and Abstractions - 핵심 원칙

## 1. 결합(Coupling)과 응집(Cohesion)

**지역적 결합은 좋다** - 코드가 함께 동작하며 서로를 지원하는 신호 (높은 응집)

**전역적 결합은 나쁘다** - 변경 비용과 위험이 superlinearly하게 증가 (Ball of Mud 패턴)

> 추상화를 삽입하여 결합도를 낮출 수 있다.
> 단순한 추상화는 복잡한 세부사항을 숨기고 변경으로부터 보호한다.

## 2. 추상화가 테스트 용이성을 높인다

**문제**: 도메인 로직이 I/O 코드와 강하게 결합되면 테스트가 어려워진다.

```python
# Before: 파일시스템에 의존하는 테스트 (느리고 복잡함)
def test_sync():
    source = tempfile.mkdtemp()
    dest = tempfile.mkdtemp()
    # ... 실제 파일 생성, 동기화, 검증, 정리 ...
```

**해결**: 상태를 단순한 데이터 구조로 추상화

```python
# After: 딕셔너리로 파일시스템 상태 추상화
source_files = {'hash1': 'path1', 'hash2': 'path2'}
dest_files = {'hash1': 'path1', 'hash2': 'pathX'}
```

## 3. "무엇을"과 "어떻게"의 분리

액션을 튜플 리스트로 추상화:

```python
("COPY", "sourcepath", "destpath")
("MOVE", "old", "new")
("DELETE", "path")
```

> "Given this actual filesystem, check what actions have happened"
> → "Given this **abstraction** of a filesystem, what **abstraction** of filesystem actions will happen?"

## 4. Functional Core, Imperative Shell (FCIS)

Gary Bernhardt의 접근법:

```python
def sync(source, dest):
    # 1. Imperative Shell: 입력 수집
    source_hashes = read_paths_and_hashes(source)
    dest_hashes = read_paths_and_hashes(dest)

    # 2. Functional Core: 순수 비즈니스 로직
    actions = determine_actions(source_hashes, dest_hashes, source, dest)

    # 3. Imperative Shell: 출력 적용
    for action, *paths in actions:
        if action == "COPY":
            shutil.copyfile(*paths)
        # ...
```

- **Functional Core**: 외부 상태에 의존하지 않는 순수 함수
- **Imperative Shell**: I/O를 담당하는 얇은 계층
- **테스트**: Functional Core에 집중

## 5. Edge-to-Edge 테스트와 의존성 주입

### Fake 객체 사용

```python
class FakeFileSystem(list):
    def copy(self, src, dest):
        self.append(('COPY', src, dest))
    def move(self, src, dest):
        self.append(('MOVE', src, dest))
    def delete(self, dest):
        self.append(('DELETE', dest))
```

### 명시적 의존성 주입

```python
def sync(reader, filesystem, source_root, dest_root):
    source_hashes = reader(source_root)
    dest_hashes = reader(dest_root)
    # ...
    filesystem.copy(destpath, sourcepath)
```

## 6. Mock vs Fake

| Mock                                    | Fake                           |
| --------------------------------------- | ------------------------------ |
| **행위 검증** (assert_called_once_with) | **상태 검증** (end state 확인) |
| London-school TDD                       | Classic-style TDD              |
| 구현 세부사항에 결합됨                  | 더 유연하고 리팩토링에 강함    |

### mock.patch를 피하는 이유

1. **설계 개선 없음**: 테스트만 가능해지고 --dry-run이나 FTP 서버 지원 불가
2. **구현에 결합**: `shutil.copy`가 올바른 인자로 호출되었는지 검증 → 취약한 테스트
3. **복잡한 테스트**: 과도한 setup 코드가 스토리를 가림

> **Designing for testability really means designing for extensibility.**

## 7. 적절한 추상화를 찾는 휴리스틱

1. 복잡한 시스템 상태를 표현할 수 있는 **친숙한 Python 데이터 구조**가 있는가?
2. 시스템 간 **경계(seam)**를 어디에 그을 수 있는가?
3. **책임**을 어떻게 분리할 것인가?
4. **암묵적 개념**을 명시적으로 만들 수 있는가?
5. **의존성**은 무엇이고 **핵심 비즈니스 로직**은 무엇인가?

## 핵심 요약

```
┌─────────────────────────────────────────────┐
│              Imperative Shell               │
│  (I/O: 파일 읽기/쓰기, 네트워크, DB 등)      │
└─────────────────────┬───────────────────────┘
                      │
              ┌───────▼───────┐
              │  Abstraction  │
              │ (Dict, Tuple) │
              └───────┬───────┘
                      │
┌─────────────────────▼───────────────────────┐
│             Functional Core                 │
│  (순수 함수: determine_actions 등)          │
│  - 테스트하기 쉬움                          │
│  - 확장하기 쉬움                            │
│  - 이해하기 쉬움                            │
└─────────────────────────────────────────────┘
```
