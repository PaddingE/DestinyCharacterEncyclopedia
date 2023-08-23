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
