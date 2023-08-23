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

* [summarization_gpt_api.ipynb](https://github.com/PaddingE/DestinyCharacterEncyclopedia/blob/main/NLP/summerization/summarization_gpt_api.ipynb) 참고

---

### GPT 3.5 Turbo API 활용

#### GPT API와 Flask를 활용해서 웹으로 정보를 뿌려주기 위해서 GPT API를 객체화

* 사용할 모듈 import
```python
import pandas as pd
import tiktoken
import os
import time
import openai
import pymysql
import re
```

* API KEY 환경변수에 저장
```python
os.environ["OPENAI_API_KEY"] = "USE_YOUR_API_KEY"
```

#### sublass.py 모듈안 Preprocessing, Subclass 클래스

* Preprocessing 클래스 : GPT API에 보낼 데이터를 전처리 해주는 클래스
* Subclass 클래스 : GPT API에 보낼 메세지를 작성해 보내고 답변을 받아오는 클래스

* Preprocessing클래스 객체 선언문
* 사용할 Database가 있는 Mysql에 연결
```python
## gpt api에 사용하기 전 preprocessing해주는 class     
class Preprocessing():
    def __init__(self):
        ## MySQL 서버 연결 설정
        db_config = {"host": "localhost",
                    "user": "root",
                    "password": "123456",
                    "database": "destiny2_db"
                    }
        ## 연결 생성
        conn = pymysql.connect(**db_config)

        ## 커서 생성
        self.cursor = conn.cursor()
```

* Database all_date_timestamp Table description열 data에 검색하려는 캐릭터의 이름이 있는 데이터들을 가지고와 SubClass객체에 사용할 데이터로 전처리해주는 함수
```python
def search_character(self, chararcter_name):
        query = f"""SELECT * FROM all_date_timestamp
            WHERE description LIKE '%{chararcter_name}%' """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        
        title_list = []
        text_list_character = []
        time_stamp = []

        for row in results:
            title_list.append(row[4])
            text_list_character.append(row[3])
            time_stamp.append(row[1])
        
        ## 사용할 데이터 dataframe화
        df_character = pd.DataFrame({
        'title': title_list,
        'text' : text_list_character,
        'time' : time_stamp
        })

        ## None값 제거
        df_character.dropna(axis=0,inplace=True)
        
        df_character_sort = df_character.sort_values(by='time', ascending = True)
        df_character_sort.reset_index(inplace = True)
        df_character_sort.drop(labels='index', axis=1,inplace=True)
        
        item_list = df_character_sort.iloc[:,0]
        
        return item_list, chararcter_name, df_character_sort
```

* 최종 요약본에 사용된 아이템들의 데이터를 사용하기 위해 mysql에 있는 아이템 데이터를 검색해서 아이템 이름, 정보 를 가지고 오는함수
```python
def find_item(self, item_name):
        print(item_name)
        item_name = re.sub('%20',' ',item_name)
        item_name = re.sub("'",'\'',item_name)
        query = f"""SELECT * FROM all_date_timestamp
            WHERE title = "{item_name}" """
            
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        
        title = results[0][4]
        description = results[0][3]
        season = results[0][1]
        
        return title, description, season
```

* 검색한 캐릭터와 관련된 정보들을 토큰수가 넘지 않게 질문을 작성해서 답변을 받아오는 함수 결과값을 list형식으로 return한다.
```python
## use_gpt_api 함수를 사용해서 summary한 내용들을 만들어주는 함수
    def make_output(self,df_character_sort,character_name):
        list_output_content = []
        list_input_title = []
        input_text = ''
        
        ## summary에 걸린 시간 측정을 위한 부분
        start_time = time.time()
        print('시작')
        
        ## data가 처음 들어왔을 때 DataFrame으로 들어왔을때 사용되는 부분
        if type(df_character_sort) == pd.DataFrame:
            for i in range(len(df_character_sort)):
                list_input_title.append(df_character_sort.iloc[i,0])
                ## 요약할 text 데이터의 token갯수를 미리 확인하는 부분 (gpt 3.5 turbo모델의 token제한에 걸리지 않기 위해 미리 확인하고 질문)
                if len(self.tokenizer.encode(df_character_sort.iloc[i,1])) < 3000:
                    input_text += df_character_sort.iloc[i,1]
                    
                    ## 다음 text 데이터를 합한 token갯수 미리 확인해서 3000 token이 넘으면 질문을 보내고 안넘으면 다음 반복문으로 진행
                    if i + 1 < len(df_character_sort) and len(self.tokenizer.encode(input_text + df_character_sort.iloc[i + 1,1])) >= 3000:
                        list_output_content.append(self.use_gpt_api(input_text,character_name))
                        input_text = ''
                        
                    ## index error방지
                    elif i + 1 == len(df_character_sort):
                        list_output_content.append(self.use_gpt_api(input_text,character_name))
                        input_text = ''
            
                    else:
                        continue
                    
                ## 요약할 text 데이터의 token 갯수가 3000이 넘을때 그 text를 .으로 split한 데이터를 질문으로 작성하는 부분
                else:
                    list_split = df_character_sort.iloc[i,1].split('.')
        
                    for j in range(len(list_split)):
                        if len(self.tokenizer.encode(list_split[j])) < 3000:
                            input_text += list_split[j]
                            if j + 1 < len(list_split) and len(self.tokenizer.encode(input_text + list_split[j + 1])) >= 3000:
                                list_output_content.append(self.use_gpt_api(input_text,character_name))
                                input_text = ''
                
                            ## index error방지    
                            elif j + 1 == len(list_split):
                                list_output_content.append(self.use_gpt_api(input_text,character_name))
                                input_text = ''
                    
                            else:
                                continue
```

* 한번 질문을 하고나서 나온 결과값이 너무 길면 한번더 요약하기 위해 list형식으로 데이터가 들어왔을때 처리하는 부분
```python
## 한번 요약한 데이터가 너무 길면 한번더 요약하기위해 사용될 부분                 
        elif type(df_character_sort) == list:
            for i in range(len(df_character_sort)):
                if len(self.tokenizer.encode(df_character_sort[i])) < 3000:
                    input_text += df_character_sort[i]
                    if i + 1 < len(df_character_sort) and len(self.tokenizer.encode(input_text + df_character_sort[i + 1])) >= 3000:
                        list_output_content.append(self.use_gpt_api(input_text,character_name))
                        input_text = ''
            
                    ## index error방지
                    elif i + 1 == len(df_character_sort):
                        list_output_content.append(self.use_gpt_api(input_text,character_name))
                        input_text = ''
            
                    else:
                        continue
                else:
                    list_split = df_character_sort[i].split('.')
        
                    for j in range(len(list_split)):
                        if len(self.tokenizer.encode(list_split[j])) < 3000:
                            input_text += list_split[j]
                            if j + 1 < len(list_split) and len(self.tokenizer.encode(input_text + list_split[j + 1])) >= 3000:
                                list_output_content.append(self.use_gpt_api(input_text,character_name))
                                input_text = ''
                
                            ## index error방지    
                            elif j + 1 == len(list_split):
                                list_output_content.append(self.use_gpt_api(input_text,character_name))
                                input_text = ''
                    
                            else:
                                continue
                            
        else:
            print("input error : input is not Dataframe or List")      
        
        finish_time = time.time()
        total_time = finish_time - start_time
        
        print(f"종료, 총 걸린 시간: {total_time}")    
                      
        return list_output_content
```

* gpt에 질문할 질문지 작성해주는 함수
```python
## gpt-api 사용해서 summary 요청해주는 함수
    def use_gpt_api(self,input_text,character_name):
        list_input_content = []
    
        ## gpt에 요청할 기본 환경과 질문 작성 부분
        list_input_content.append({"role": "system", "content": "This is the beginning of your NEW conversation."})
        list_input_content.append({"role": "assistant", "content": "You are a helpful summarizer chatbot."})
        list_input_content.append({"role": "user", "content": f"please substantiated summary about {character_name} based on the following text : " 
                                   + input_text})
    
        ## 초기화 부분에서 설정한 gpt모델에 질문 보내기
        response = openai.ChatCompletion.create(model=self.model,messages=list_input_content)
        answer = response['choices'][0]['message']['content']
    
        ## 딜레이 없이 너무 빨리 보내면 에러가 발생해 0.7초 딜레이 걸어주기
        time.sleep(0.7)
    
        return answer
```

* [subclass.py](https://github.com/PaddingE/DestinyCharacterEncyclopedia/blob/main/FrontEnd/Flask/flask_gpt/subclass.py) 참고

---
