> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Checkpointing

> Claude의 편집을 자동으로 추적하고 원하지 않는 변경 사항에서 빠르게 복구하기 위해 되감기합니다.

Claude Code는 작업하면서 Claude의 파일 편집을 자동으로 추적하므로, 문제가 발생하면 변경 사항을 빠르게 실행 취소하고 이전 상태로 되돌릴 수 있습니다.

## Checkpointing의 작동 방식

Claude와 함께 작업할 때, checkpointing은 각 편집 전에 코드의 상태를 자동으로 캡처합니다. 이 안전망을 통해 항상 이전 코드 상태로 돌아갈 수 있다는 것을 알면서 야심 찬 대규모 작업을 수행할 수 있습니다.

### 자동 추적

Claude Code는 파일 편집 도구로 수행된 모든 변경 사항을 추적합니다:

* 모든 사용자 프롬프트는 새로운 checkpoint를 생성합니다
* Checkpoint는 세션 전체에 걸쳐 유지되므로 재개된 대화에서 액세스할 수 있습니다
* 30일 후 세션과 함께 자동으로 정리됩니다(구성 가능)

### 변경 사항 되감기

`Esc` 두 번(`Esc` + `Esc`)을 누르거나 `/rewind` 명령을 사용하여 rewind 메뉴를 엽니다. 다음을 복구하도록 선택할 수 있습니다:

* **대화만**: 코드 변경 사항을 유지하면서 사용자 메시지로 되감기
* **코드만**: 대화를 유지하면서 파일 변경 사항 되돌리기
* **코드와 대화 모두**: 세션의 이전 지점으로 둘 다 복구

## 일반적인 사용 사례

Checkpoint는 다음과 같은 경우에 특히 유용합니다:

* **대안 탐색**: 시작점을 잃지 않으면서 다양한 구현 방식을 시도합니다
* **실수에서 복구**: 버그를 도입하거나 기능을 손상시킨 변경 사항을 빠르게 실행 취소합니다
* **기능 반복**: 작동하는 상태로 되돌릴 수 있다는 것을 알면서 변형을 실험합니다

## 제한 사항

### Bash 명령 변경 사항이 추적되지 않음

Checkpointing은 bash 명령으로 수정된 파일을 추적하지 않습니다. 예를 들어, Claude Code가 다음을 실행하는 경우:

```bash  theme={null}
rm file.txt
mv old.txt new.txt
cp source.txt dest.txt
```

이러한 파일 수정 사항은 rewind를 통해 실행 취소할 수 없습니다. Claude의 파일 편집 도구를 통해 직접 수행된 파일 편집만 추적됩니다.

### 외부 변경 사항이 추적되지 않음

Checkpointing은 현재 세션 내에서 편집된 파일만 추적합니다. Claude Code 외부에서 수동으로 수행한 파일 변경 사항과 다른 동시 세션의 편집은 일반적으로 캡처되지 않습니다. 단, 현재 세션과 동일한 파일을 수정하는 경우는 예외입니다.

### 버전 관리의 대체가 아님

Checkpoint는 빠른 세션 수준의 복구를 위해 설계되었습니다. 영구적인 버전 기록 및 협업을 위해:

* 커밋, 분기 및 장기 기록을 위해 버전 관리(예: Git)를 계속 사용합니다
* Checkpoint는 적절한 버전 관리를 보완하지만 대체하지 않습니다
* Checkpoint를 "로컬 실행 취소"로, Git을 "영구 기록"으로 생각합니다

## 참고 항목

* [Interactive mode](/ko/interactive-mode) - 키보드 단축키 및 세션 제어
* [Built-in commands](/ko/interactive-mode#built-in-commands) - `/rewind`를 사용하여 checkpoint에 액세스
* [CLI reference](/ko/cli-reference) - 명령줄 옵션
