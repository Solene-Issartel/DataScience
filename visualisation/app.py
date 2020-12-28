import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import csv

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__)

def extraireTableau(number):
    with open('../data/clean_thematiques.csv', newline='') as f:  # Ouverture du fichier CSV
        read = csv.reader(f)  # chargement des lines du fichier csv
        columnsName = ["theme", "number of words"]
        print(columnsName)
        themes = []
        lengthes = []
        i = 0
        for line in read:
            if i != 0:
                if i == number+1:
                    break
                for elm in line:
                    themes.append(line[1])
                    lengthes.append(len((line[2]).split(",")))
                print(line[1])
                print(len((line[2]).split(",")))
            i+=1
    return [columnsName, themes, lengthes]

datas = extraireTableau(10)

df = pd.DataFrame({
    datas[0][0]: datas[1],
    datas[0][1]: datas[2]
})

fig = px.bar(df, x=datas[0][0], y=datas[0][1])

app.layout = html.Div(children=[
    html.H1(children='DATA SCIENCE par Luc Raymond, Solène Issartel, Laura Biasibetti'),

    html.H3(children='Analyse des thématiques abordées ensemble dans les mails'),

    dcc.Graph(

        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)