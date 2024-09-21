# 카카오톡 메시지 분석기

카카오톡 대화 내용을 분석하여 특정 사용자의 메시지를 요약하고 분석하는 GUI 프로그램입니다. OpenAI의 GPT-4 모델을 사용하여 메시지를 심도 있게 분석합니다.

## 주요 기능

- CSV 파일로부터 카카오톡 대화 내용을 읽어옵니다.
- 특정 사용자를 선택하여 해당 사용자의 메시지를 중심으로 대화를 분석합니다.
- 분석 결과를 GUI를 통해 단계별로 실시간 표시합니다.

## 목차

- [요구 사항](#요구-사항)
- [설치](#설치)
- [OpenAI API 키 설정](#openai-api-키-설정)
  - [macOS 및 Linux](#macos-및-linux)
  - [Windows](#windows)
  - [`.env` 파일 사용 (선택 사항)](#env-파일-사용-선택-사항)
- [사용 방법](#사용-방법)
- [주의 사항](#주의-사항)
- [라이선스](#라이선스)

## 요구 사항

- Python 3.7 이상
- `openai` 라이브러리
- `python-dotenv` 라이브러리 (선택 사항, `.env` 파일 사용 시)

## 설치

1. **리포지토리 클론 또는 다운로드**

   ```bash
   git clone https://github.com/yourusername/kakao-analyzer.git
   cd kakao-analyzer
   ```

2. **필요한 패키지 설치**

   ```bash
   pip install openai
   ```

   `.env` 파일을 사용할 예정이라면:

   ```bash
   pip install python-dotenv
   ```

## OpenAI API 키 설정

이 프로그램은 OpenAI의 GPT-4 모델을 사용하므로, OpenAI API 키가 필요합니다. API 키는 [OpenAI 계정](https://platform.openai.com/account/api-keys)에서 발급받을 수 있습니다.

### macOS 및 Linux

#### 터미널에서 일시적으로 설정하기

터미널에서 다음 명령어를 입력하여 현재 세션에만 환경 변수를 설정합니다:

```bash
export OPENAI_API_KEY='your-api-key-here'
```

`your-api-key-here` 부분을 실제 API 키로 대체하세요.

#### 터미널에서 영구적으로 설정하기

- **bash를 사용하는 경우 (`.bashrc` 수정)**

  ```bash
  echo "export OPENAI_API_KEY='your-api-key-here'" >> ~/.bashrc
  source ~/.bashrc
  ```

- **zsh를 사용하는 경우 (`.zshrc` 수정)**

  ```bash
  echo "export OPENAI_API_KEY='your-api-key-here'" >> ~/.zshrc
  source ~/.zshrc
  ```

### Windows

#### 명령 프롬프트에서 일시적으로 설정하기

명령 프롬프트에서 다음을 입력합니다:

```cmd
set OPENAI_API_KEY=your-api-key-here
```

#### 시스템 환경 변수로 영구적으로 설정하기

1. **환경 변수 설정 창 열기:**

   - 작업 표시줄 검색에서 "환경 변수"를 입력하고 **"시스템 환경 변수 편집"** 을 선택합니다.
   - 또는 **Win + R** 키를 누르고 `sysdm.cpl` 을 입력한 후 **확인**을 클릭하고, **고급** 탭에서 **환경 변수** 버튼을 클릭합니다.

2. **환경 변수 추가:**

   - **사용자 변수** 또는 **시스템 변수**에서 **새로 만들기**를 클릭합니다.
   - **변수 이름**에 `OPENAI_API_KEY` 를 입력합니다.
   - **변수 값**에 API 키를 입력합니다.
   - **확인**을 클릭하여 모든 창을 닫습니다.

### `.env` 파일 사용 (선택 사항)

`.env` 파일을 사용하면 환경 변수를 관리하기 더 편리합니다.

1. **`python-dotenv` 설치**

   ```bash
   pip install python-dotenv
   ```

2. **프로젝트 디렉토리에 `.env` 파일 생성**

   `.env` 파일에 다음 내용을 추가합니다:

   ```
   OPENAI_API_KEY=your-api-key-here
   ```

3. **코드에서 환경 변수 로드하기**

   파이썬 코드 상단에 다음을 추가합니다:

   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

## 사용 방법

1. **프로그램 실행**

   ```bash
   python your_script.py
   ```

2. **CSV 파일 선택**

   - "찾아보기" 버튼을 클릭하여 분석할 카카오톡 대화 CSV 파일을 선택합니다.

3. **사용자 선택**

   - "사용자 검색" 필드에 분석할 사용자의 이름을 입력하여 선택합니다.

4. **분석 시작**

   - "분석 시작" 버튼을 클릭하면 분석이 시작되고, 결과가 실시간으로 표시됩니다.

## 주의 사항

- **API 키 보안**

  - API 키는 절대 공개 저장소나 코드에 직접 포함하지 마세요.
  - 키가 노출되면 악의적인 사용으로 인해 요금이 발생할 수 있습니다.

- **OpenAI 요금**

  - OpenAI API를 사용하면 요금이 발생할 수 있으므로, 사용량을 모니터링하세요.

- **CSV 파일 형식**

  - CSV 파일은 다음과 같은 형식이어야 합니다:

    ```
    날짜,사용자,내용
    ```

  - 날짜 형식은 다음 중 하나여야 합니다:

    - `%Y-%m-%d %H:%M:%S`
    - `%Y.%m.%d %H:%M`
    - `%Y-%m-%d %H:%M`

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

---

프로젝트와 관련하여 문의 사항이나 개선 사항이 있다면 이슈를 생성하거나 풀 리퀘스트를 보내주세요!

# 추가 정보

- **OpenAI 계정 생성 및 API 키 발급:** [OpenAI 계정 대시보드](https://platform.openai.com/account/api-keys)
- **OpenAI API 문서:** [OpenAI API Documentation](https://platform.openai.com/docs/introduction)

# 개발자 참고 사항

- **GUI 업데이트 관련 주의사항**

  - Tkinter는 스레드 안전하지 않으므로, 백그라운드 스레드에서 직접 GUI를 업데이트하면 문제가 발생할 수 있습니다.
  - 이 프로젝트에서는 `queue.Queue`를 사용하여 스레드 간 안전하게 데이터를 전달하고, `after` 메서드를 사용하여 메인 스레드에서 주기적으로 큐를 확인하여 GUI를 업데이트합니다.

- **환경 변수 설정 확인**

  - 프로그램 실행 전에 환경 변수가 제대로 설정되었는지 확인하세요:

    ```bash
    echo $OPENAI_API_KEY  # macOS/Linux
    ```

    ```cmd
    echo %OPENAI_API_KEY%  # Windows
    ```

- **라이브러리 설치 문제**

  - 필요한 라이브러리가 설치되지 않은 경우 다음 명령어로 설치하세요:

    ```bash
    pip install -r requirements.txt
    ```

    `requirements.txt` 파일이 없는 경우:

    ```bash
    pip install openai python-dotenv
    ```

- **모델 이름 및 OpenAI API 변경 사항**

  - 코드에서 사용된 모델(`gpt-4-1106-preview`)은 예시이며, 실제로 사용 가능한 모델 이름으로 변경해야 할 수 있습니다.
  - OpenAI API의 변경 사항이나 모델 업데이트에 따라 코드 수정을 고려하세요.

# 코드 예시

```python
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    print("OpenAI API 키가 설정되지 않았습니다.")
    exit()

# 나머지 코드...
```

---

**중요:** 이 README 파일은 프로그램 사용에 필요한 정보를 제공하기 위한 것이며, 실제 코드 및 파일 구조에 따라 내용을 수정해야 할 수 있습니다.
