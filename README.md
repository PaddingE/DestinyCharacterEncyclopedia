# Project : DestinyCharacterEncyclopedia

## 프로젝트 최종 목표

 웹페이지에 Destiny2 스토리와 관련된 정보들을 보여주고 검색창에 특정 캐릭터 입력시 해당 캐릭터에 관한 내용을 하나의 문서로 요약해 보여주는 것을 목표로 시작

## 프로젝트 진행 방향

### 데이터 수집
* [웹 크롤링](https://github.com/PaddingE/DestinyCharacterEncyclopedia/tree/main/Preprocessing/WEB_crawling)

### 데이터 전처리
* [Time Stamp Preprocessing](https://github.com/PaddingE/DestinyCharacterEncyclopedia/tree/main/Preprocessing/Time_stamp)

### 자연어 처리
* [GPT-3.5-turbo API](https://github.com/PaddingE/DestinyCharacterEncyclopedia/tree/main/NLP/summerization)

### 프론트엔드
* [Flask](https://github.com/PaddingE/DestinyCharacterEncyclopedia/tree/main/FrontEnd/Flask/flask_gpt)

## 데이터 수집.웹 크롤링
### Destiny2 Weblore

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re
```

 
