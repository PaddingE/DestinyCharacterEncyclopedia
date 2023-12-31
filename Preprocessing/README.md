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
|0	|Guardian|	Classes|	Guardians	|\n"Legends are carved into history by the brav...|
|1|	Guardian|	Classes	|Class: Hunter	|\n"Our old worlds have grown feral—rabid beast...|
|2	|Guardian	|Classes	|Ghost Fragment: Hunter|	She leaves the Sparrow and climbs a long way a...|
|3|	Guardian|	Classes|	Class: Titan	|\n"Stand. Not only to fight, but to strive. Fo...|
|4|	Guardian|	Classes|	Ghost Fragment: Titan	|/ Tighten that strap.\n/ Eh?\n/ The gardbrace ...|
|...|	...|	...|	...|	...|
|834|	Activities|	Other_Activities	|Festival of the Lost: Underwatch|	"Eri-i-i-is. Oh, Eri-i-i-is."\n"Do you have my...|
|835|	Activities|	Other_Activities|	The Dawning	|“Pass me those lanterns, would you?” Eva said....|
|836|	Activities	|Other_Activities|	Dawning Fortunes|	Fortune telling at the start of a new year is ...|
|837|	Activities|	Other_Activities|	Haakon Precipice|"Hey! Who left this forklift in the middle of ...|
|838|	Activities	|Other_Activities|	Shining Sands|	"OK. I’ve been hearing a rumor that a racer we...|
* [crawling_destiny2_weblore.ipynb](https://github.com/PaddingE/DestinyCharacterEncyclopedia/blob/main/Preprocessing/WEB_crawling/crawling_destiny1_grimoire.ipynb) 참고
