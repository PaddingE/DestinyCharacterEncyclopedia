# Project : DestinyCharacterEncyclopedia

## 프로젝트 최종 목표

 웹페이지에 Destiny2 스토리와 관련된 정보들을 보여주고 검색창에 특정 캐릭터 입력시 해당 캐릭터에 관한 내용을 하나의 문서로 요약해 보여주는 것을 목표로 시작

![홈페이지](/output_images/output_1.png)
![검색결과](/output_images/output_3.png)
![검색결과](/output_images/output_4.png)
![검색결과](/output_images/output_5.png)
![아이템정보](/output_images/output_6.png)

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

* 웹 크롤링에 필요한 **urlopen, BeautifulSoup** 모듈  Mysql로 관리할 database를 json 파일로 만들어 사용하기 위한 **pandas** import
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

* Weblore 웹 크롤링과 마찬가지로 **urlopen, BeautifulSoup, pandas** import

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re
```

* destiny pedia Grimoire 페이지 에 보이는 최상위구조 카테고리 가져오는 부분
* html 파일의 div태그의 class속성이 gallerytext인 값에 카테고리들이 들어있음

```python
url_grimoire_root = 'https://www.destinypedia.com/Grimoire'

html = urlopen(url_grimoire_root)
bs = BeautifulSoup(html, 'html.parser')

list_gallary_text = bs.findAll('div',{'class': 'gallerytext'})
```

* Weblore 보다 카테고리가 한겹 더 쌓여져 있어서 반복문을 한겹 더 사용

```python
list_section_df = []
list_title_df = []
list_subtitle_df = []
list_text_df = []

for i in range(len(list_gallary_title)):
    url_section = url_grimoire_root + ':' + list_gallary_title[i]
    section_html = urlopen(url_section)
    bs_section = BeautifulSoup(section_html, 'html.parser')
    
    list_title_text = bs_section.findAll('div',{'class': 'gallerytext'})
    
    list_title = []
    
    for title in list_title_text:
        title_text_re = re.sub(r'\n','', title.text)
        list_title.append(title_text_re)
        
    for j in range(len(list_title)):
        list_title[j] = re.sub("'",'%27',list_title[j])
        list_title[j] = re.sub("&",'%26',list_title[j])
        list_title[j] = re.sub(" ",'_',list_title[j])
        
        url_title = url_section + '/' + list_title[j]
        title_html = urlopen(url_title)
        bs_title = BeautifulSoup(title_html,'html.parser')
        
        select = bs_title.select_one('.mw-parser-output')

        flag = False
        
        text = ''

        for child in select:
            if child.name == 'h2':
            
                if flag == True:
                    list_text_df.append(text)
                    text = ''
            
                list_subtitle_df.append(child.text)
                list_title_df.append(list_title[j])
                list_section_df.append(list_gallary_title[i])
                flag = True
        
            elif flag == True and (child.name == 'p' or child.name == 'dl'):
                text += child.text
        
        list_text_df.append(text)
        
        list_title_df[j] = re.sub("%27","'",list_title_df[j])
        list_title_df[j] = re.sub("%26",'&',list_title_df[j])
        list_title_df[j] = re.sub("_",' ',list_title_df[j])
        
```

* 크롤링한 데이터를 json파일로 저장

```python
df_grimoire = pd.DataFrame({'section': list_section_df, 'title':list_title_df, 'sub_title':list_subtitle_df, 'text': list_text_df})
df_grimoire.to_json('./Database/raw_grimoire.json',orient='records')
```

### 수집한 데이터

|index|section|title|sub_title|text|
|---|---|---|---|---|
|0|Guardian|Classes|Guardians|\n"Legends are carved into history by the brav...|
|1|Guardian|Classes|Class: Hunter|\n"Our old worlds have grown feral—rabid beast...|
|2|Guardian|Classes|Ghost Fragment: Hunter|	She leaves the Sparrow and climbs a long way a...|
|3|Guardian|Classes|Class: Titan|\n"Stand. Not only to fight, but to strive. Fo...|
|4|Guardian|Classes|Ghost Fragment: Titan|/ Tighten that strap.\n/ Eh?\n/ The gardbrace ...|
|...|	...|	...|	...|	...|
|834|Activities|Other_Activities|Festival of the Lost: Underwatch|"Eri-i-i-is. Oh, Eri-i-i-is."\n"Do you have my...|
|835|Activities|Other_Activities|The Dawning|“Pass me those lanterns, would you?” Eva said....|
|836|Activities|Other_Activities|Dawning Fortunes|Fortune telling at the start of a new year is ...|
|837|Activities|Other_Activities|Haakon Precipice|"Hey! Who left this forklift in the middle of ...|
|838|Activities|Other_Activities|Shining Sands|"OK. I’ve been hearing a rumor that a racer we...|
* [crawling_destiny2_weblore.ipynb](https://github.com/PaddingE/DestinyCharacterEncyclopedia/blob/main/Preprocessing/WEB_crawling/crawling_destiny1_grimoire.ipynb) 참고
---

## 자연어 처리.GPT 3.5 Turbo
### GPT 3.5 Turbo API 기본 사용법

* OpenAi 챗봇 모델을 사용하기 위해 모듈 설치
```python
pip install openai
```

* OpenAi 챗봇 모델이 토큰 제한을 가지고 있어 미리 토큰을 세서 질문하기 위해 tiktoken 모듈 설치
```python
pip install tiktoken
```

* 사용할 모듈 import
```python
import os
import openai
from tiktoken import Tokenizer
```

* 본인의 Api Key 세팅
```python
openai.api_key = "USE_YOUR_API_KEY"
```

* GPT에 물어보기 위한 질문지 작성
```python
messages = [{"role":"user","content":"Please summarize the following text"},
            {"role":"user","content":"""A compact submersible of Eliksni design finishes its descent through the hazy depths of Titan\'s methane ocean. 
                                        The craft\'s seafloor landing kicks up a cloud of dark silt and microbial life shimmering like stars. 
                                        The submersible\'s dorsal airlock cracks open with a rush of bubbles, then slowly folds down into a ramp, 
                                        allowing a trio of figures armored in deep diving gear to emerge. 
                                        The submersible\'s single floodlight sweeps across the ocean floor, revealing the alien landscape of twisting coral. 
                                        \n\nFenchurch approaches one of the coral growths, running a gloved hand over its surface. \"These polyps…\" he mutters.
                                        \"Is this—\" He stops suddenly at the sound of a mechanical snap, and turns to see Chalco and Lisbon-13 plant a large, 
                                        mechanical spire in the ground. Internal lights flicker on as the spire whirrs to life, 
                                        creating a regulated field of water pressure around the submersible. \n\nFenchurch steps away from the coral, rubbing his fingers together. 
                                        He looks to the spire as its sides open like a flower and release several drones, each outfitted with floodlights. 
                                        The drones swim out ahead, revealing the disorienting flicker of what looks like the water\'s surface but at an impossibly vertical angle.
                                        \n\n\"This way,\" Chalco directs as she turns to follow the drones. 
                                        Fenchurch and Lisbon look at one another, steady themselves, and fall in line behind their fireteam leader. 
                                        \n\n\"Stop me if you\'ve heard this one before,\" Fenchurch says, anxiously checking the talisman clipped to his armor. 
                                        \"Two Hunters and a Warlock walk into the deep…\"
                                        """}
            ]
```

* 사용할 gpt모델에 질문지를 사용해서 채팅 보내서 답변 받기
```python
completion = openai.ChatCompletion.create(
    model = 'gpt-3.5-turbo',
    messages = messages
)
```

* 받은 답변 확인
```python
completion.choices
```
