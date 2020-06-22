# PTTyR-UROP


학부생 연구 프로그램(UROP)을 위한 repository입니다.

Tensor shape 분석 언어 명세와, 이를 위한 자료들을 업로드하겠습니다.



우선 다른 학부생분들은 아래와 같이 환경설정해주시면 감사하겠습니다. 기본적인 내용은 주 repository에서 가져왔습니다.

- 아나콘다 설치(파이썬 3)

- 아래 명령어로 가상환경 생성 후 requirements.txt 내용 설치

  ```bash
  conda create -n pttyr python==3.8
  conda activate pttyr
  conda install pytorch==1.4.0
  pip install -r requirements.txt
  ```

  - 우분투만 그런지 모르겠는데, pytorch는 requirement.txt 형식으로 바로 설치가 안 돼서 따로 빼두었습니다.
  - 주 repository에서 `pygit2`만 새로 추가된 것입니다.



### 라이브러리 크롤러

- 깃헙 레포지토리로부터 .py, .ipynb 파일으로부터 builtin, Module 상속 클래스들의 출현 위치와 빈도수를 계산하여 엑셀로 만듭니다.

- 본 프로젝트의 주요 요소가 아니므로 코드는 친절하진 않습니다.. (주석 없이 최대한 빠르게 완성하고자 했습니다.)

  - 간단하게 설명드리면, 주석부분을 제외한 부분으로부터 정규식 문자열 탐색을 통해 해당 함수들의 출현 위치를 데이터베이스화 시키는 것입니다.
- `database.csv` 파일은 오직 `torchvision, torchtext, torchaudio`만 크롤링 한 것이고,
  - `database_full.csv` 파일은 `requirement_full.csv` 파일 전체 레포지토리를 크롤링한 것입니다.
  - 우선 `database.csv`부터 구글독스를 사용하여 학부생들끼리 서로 겹치지 않게 표기하면서 명세화작업에 들어가도록 하겠습니다.
    - 구글독스 링크: https://drive.google.com/drive/folders/17KxY6jU8Jf9rOG54wS3cnZtwBx4Gjj2m?usp=sharing
  
- 사용 방법

  -  PROJECT_URLS` 리스트에 있는 주소의 코드들을 읽어와서 데이터베이스 테이블을 완성합니다.

    ```bash
    conda activate pttyr
    python3 src/crawler/table_maker.py
    ```

  - `repositories.txt` 파일 내용을 줄 단위로 읽어서 깃헙 사이트를 클론한 뒤, 데이터베이스 테이블에서 검색하여 추가합니다.
  - 라이브러리 내장 함수 혹은 모듈 클래스 중 어떤 것들이 자주 사용되는지 빈도수로 정렬하여 `.csv` 파일 형태로 저장합니다.



### 진행 예정 사항

- `pytorch` 사용 프로젝트 레포지토리를 최대한 찾은 뒤, 어떤 함수들이 쓰이는지 테이블 형태로 만들겠습니다.
- 빈도수 내림차순으로 정렬하므로 조금의 작업만으로도 더 많은 코드를 커버할 수 있을 것입니다.
- 이 테이블을 기반으로 바로 명세화 작업 들어가겠습니다.

