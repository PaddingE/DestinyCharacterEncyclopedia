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

* 웹 크롤링을 위해 필요한 **urlopen, BeautifulSoup** 모듈  Mysql로 관리할 database를 json 파일로 만들어 사용하기 위한 **pandas** import
```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re
```

* destinypedia의 Weblore페이지 구성이 season별로 나뉘어 있기때문에 웹 크롤링에 사용할 season명을 따로 크롤링해 **season_list_tag**에 저장
```python
url_weblore = 'https://www.destinypedia.com/Weblore'

html = urlopen(url_weblore)
bs = BeautifulSoup(html, 'html.parser')

season_list_tag = bs.findAll('span',{'class':'mw-headline'})
```

```python
url_weblore_root = 'https://www.destinypedia.com/Weblore'

for i in range(len(list_season)):
    ## 데이터 프레임을 만들기 위해 필요한 변수 선언
    list_expension = []
    list_title = []
    list_text = []
    text = ''
    title_flag = False
    
    ## url사용시 에러나는부분 고처쓰기위한 부분
    list_season[i] = re.sub("'",'%27',list_season[i])
    list_season[i] = re.sub(" ",'_',list_season[i])
    
    ## beautiful soup 객체 선언
    url_season = url_weblore_root + ':' + list_season[i]
    html = urlopen(url_season)
    bs = BeautifulSoup(html, 'html.parser')
    
    ## class명으로 태그 선택
    html_full = bs.select_one('.mw-parser-output')
    
    ## 태그 안에 들어가 제목과 내용 분류해서 list에 넣기
    for child in html_full:
        if child.name == 'h2':
            ## 다음 제목으로 넘어가게 되면 이전 내용을 list에 저장 후 내용 초기화
            if title_flag == True:
                list_text.append(text)
                text = ''
            ## 제목이 들어있는 태그 만나면 제목리스트에 저장
            list_title.append(child.text)
            title_flag = True
        ## html_full을 처음 선택하면 있는 p태그를 건너뛰고 다음 p태그부터 저장할 내용 연결
        elif title_flag == True and child.name == 'p':
            text += child.text
    
    ## 제목 리스트의 마지막에 references제거         
    list_title.remove('References')
    
    ## url사용하기 위해 고친 부분 다시 원상태로 만들기
    list_season[i] = re.sub("%27","'",list_season[i])
    list_season[i] = re.sub("_",' ',list_season[i])
    
    ## 확장팩 리스트 만들기
    for j in range(len(list_title)):
        list_expension.append(list_season[i])
    
    ## 확인용    
    print(list_expension)
    print(list_title)
    print(list_text)
       
    ## 만든 리스트로 데이터 프레임 만들어서 csv파일로 저장 
    df_data = pd.DataFrame({'expension_name': list_expension, 'title': list_title, 'text':list_text})
    df_data.to_csv('.\Database\df_' + list_season[i] + '.csv', index= False)
```

* 수집한 데이터 **json**파일로 저장
```python
df_concat.to_json('./Database/weblore.json',orient='records')
```

### 수집한 데이터

|index|expension_name|title|text|
|----|----|----|----|
|0|Forsaken|Letter from Cayde|[scrawled on a page torn out of The Lone Star ...|
|1|Joker's Wild|Gambit Prime|"What's this about?" Joxer asked.\nThe Titan s...|
|2|Joker's Wild|The Reckoning|Drifter scowled at a notch on his glaive as he...|
|3|Joker's Wild|Praxic Order|The more petals Lionel swept into his garbage ...|
|.|.|.|.|
|.|.|.|.|
|.|.|.|.|
|38|Warmind|Tyra|"Ghost, open a new file. Research Notes TK-487...|
|39|Warmind|Apocrypha|In the beginning, there were five.\nYul, the H...|
|40|Warmind|Cryptarch|From "Collapse and Post-Collapse Incidents on ...|
|41|Warmind|Zavala|Ikora has confirmed my fears. The ice on Mars ...|
|42|Warmind|Rasputin|218CBI800JRS101\nAI-COM/RSPN: ASSETS//POLARIS/...|

* [crawling_destiny2_weblore.ipynb](https://github.com/PaddingE/DestinyCharacterEncyclopedia/blob/main/Preprocessing/WEB_crawling/crawling_destiny2_weblore.ipynb) 참고
---

### Destiny Grimoire

