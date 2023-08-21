import subclass as sc
import pandas as pd

pp = sc.Preprocessing('./Database/cut_data.json')
output = sc.Subclass()

character = 'Lisbon-13'

df, name = pp.search_character(character)

list_output = output.make_output(df,name)

print(list_output)

full_text = ''

for text in list_output:
    full_text += text

df_summary = pd.DataFrame({'character': [character] * len(list_output),
                           'summary': list_output})


df_summary.to_json('./Databaase/lisbon_gpt_summary.json', orient='records')

