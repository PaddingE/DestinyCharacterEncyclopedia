from flask import Flask, render_template, request
import subclass as sc

app = Flask(__name__)

@app.route("/")
def homepage():
    return  render_template('index_with_sidebar_revision_or.html')

@app.route("/output", methods = ['GET'])
def view():
    
    input_text = request.args['input_text']
    
    pp = sc.Preprocessing()
    output = sc.Subclass()

    
    item_list_data, name, df_text = pp.search_character(input_text)
    character_name, summary_text, translate_text = pp.find_data(input_text)
    list_output_list = output.make_output(df_text, name)
    
    text_output = ''
    
    for text in list_output_list:
        text_output += text
        
    return render_template('lisbon.html', output_text = translate_text, character_text = character_name,summary_text = text_output,
                           table = item_list_data)

@app.route("/reference/<item>")
def click_reference(item):
    
    pp = sc.Preprocessing()
    
    title,description,season = pp.find_item(item)
    
    return render_template('item.html', item_title = title, item_description = description, item_season = season)

@app.route("/Humanity")
def humanity():
    return render_template('Humanity.html')
    
if __name__ == "__main__":
    app.run()





    # full_text = ' '

    # for i in range(len(df)):
    #     full_text += (' ' + df.)