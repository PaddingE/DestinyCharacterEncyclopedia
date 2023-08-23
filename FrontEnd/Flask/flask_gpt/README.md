## 프론트엔드.Flask

* 사용할 Flask, subclass모듈 import
```python
from flask import Flask, render_template, request
import subclass as sc
```

* Flask구동시 홈페이지 열어주는 함수
```python
app = Flask(__name__)

@app.route("/")
def homepage():
    return  render_template('Home.html')
```

* [Home.html](https://github.com/PaddingE/DestinyCharacterEncyclopedia/blob/main/FrontEnd/Flask/flask_gpt/templates/Home.html) 참고

* 홈페이지에서 검색창에 캐릭터 이름을 입력하고 검색하면 그 캐릭터에 대한 내용을 gpt에게 요약해달라고 하고, papago에 번역해서 answer.html에 보내서 뿌려주는 부분
```python
@app.route("/output", methods = ['GET'])
def view():
    
    input_text = request.args['input_text']
    
    pp = sc.Preprocessing()
    output = sc.Subclass()

    
    item_list_data, name, df_text = pp.search_character(input_text)
    character_name, _, translate_text = pp.find_data(input_text)
    list_output_list = output.make_output(df_text, name)
    
    text_output = ''
    
    for text in list_output_list:
        text_output += text
        
    return render_template('answer.html', character_text = character_name, summary_text = text_output, output_text = translate_text,
                           table = item_list_data)
```

* [Answer.html](https://github.com/PaddingE/DestinyCharacterEncyclopedia/blob/main/FrontEnd/Flask/flask_gpt/templates/Answer.html) 참고

* 검색 결과 페이지 아래에 요약에 사용된 아이템 referece를 클릭했을 때 그 아이템에 대한 내용을 item.html로 보내서 뿌려주는 부분
```python
@app.route("/reference/<item>")
def click_reference(item):
    
    pp = sc.Preprocessing()
    
    title,description,season = pp.find_item(item)
    
    return render_template('item.html', item_title = title, item_description = description, item_season = season)
```

* [item.html](https://github.com/PaddingE/DestinyCharacterEncyclopedia/blob/main/FrontEnd/Flask/flask_gpt/templates/item.html) 참고

* [app.py](https://github.com/PaddingE/DestinyCharacterEncyclopedia/blob/main/FrontEnd/Flask/flask_gpt/app.py) 참고
