import pandas as pd
import tiktoken
import os
import time
import openai
import pymysql
import re

os.environ["OPENAI_API_KEY"] = "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"

class Subclass():
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

        ## 사용할 model 정하기
        self.model = "gpt-3.5-turbo"
        ## 사용할 model에 따른 토크나이저 객체 생성 - 토큰 확인용
        self.tokenizer = tiktoken.get_encoding("r50k_base")
    
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
   
## gpt api에 사용하기 전 preprocessing해주는 class     
class Preprocessing():
    def __init__(self):
        # MySQL 서버 연결 설정
        db_config = {"host": "localhost",
                    "user": "root",
                    "password": "123456",
                    "database": "destiny2_db"
                    }
        # 연결 생성
        conn = pymysql.connect(**db_config)

        # 커서 생성
        self.cursor = conn.cursor()
    
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
    
    def find_data(self, character_name):
        query = f"""SELECT * FROM fin_output
            """
            
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        
        summary_text = results[0][2]
        translate_text = results[0][0]
        
        return character_name, summary_text, translate_text
        
        