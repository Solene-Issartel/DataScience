import csv
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_table as dt
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Style de la side bar bootstrap
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa"
}

# Style du contenu
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# Notre menu de navigation à gauche
sidebar = html.Div(
    [
        html.H2("Sommaire", className="display-6"),
        html.Hr(),
        html.P(
            "Cliquer sur les liens pour accéder aux menus correspondants", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("1- Formatage des données", href="/formatage", active="exact"),
                dbc.NavLink("X- Thématiques count", href="/thematiquesCount", active="exact"),
                dbc.NavLink("N- Patterns Fréquents", href="patternsFrequents", active="exact")
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

# Permet de mettre le style du contenu pour chaque page
content = html.Div(id="page-content", style=CONTENT_STYLE)

# Notre header présent sur toutes les pages
header = html.Header(id="header", children=[
    html.H1(children='Projet DATA SCIENCE par Luc Raymond, Solène Issartel, Laura Biasibetti'),
    html.Hr()])

# Toute notre application
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

# La page avec les thématiques
def extraireTableau(number):
    with open('data/clean_thematiques.csv', newline='') as f:  # Ouverture du fichier CSV
        read = csv.reader(f)  # chargement des lignes du fichier csv
        columns_name = ["Thématiques", "Nombre de mots"]
        print(columns_name)
        themes = []
        length = []
        i = 0
        for line in read:
            if i != 0:
                if i == number + 1:
                    break
                for elm in line:
                    themes.append(line[1])
                    length.append(len((line[2]).split(",")))
                print(line[1])
                print(len((line[2]).split(",")))
            i += 1
    return [columns_name, themes, length]


data = extraireTableau(10)

df = pd.DataFrame({
    data[0][0]: data[1],
    data[0][1]: data[2]
})

figThematique = px.bar(df, x=data[0][0], y=data[0][1])

thematiquesCount = html.Div(children=[
    html.H3(children='Analyse des thématiques abordées ensemble dans les mails'),
    dcc.Graph(
        figure=figThematique
    )])

# La page pour les patterns fréquents
itemsets = pd.read_csv("data/itemsetsFrequents.csv", low_memory=False, header=0)
patternsFrequents = html.Div(children=[
                html.H3(children='Les différentes thématiques associées ensembles'),
                dt.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in itemsets.iloc[:, 1:3]],
                    data=itemsets.to_dict('records'),
                    sort_action="native",
                )
            ])


# Permet de mettre à jour la page selon le lien
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.Div(children=[
            header,
        ])
    elif pathname == "/formatage":
        return html.Div(children=[
            header,
        ])
    elif pathname == "/thematiquesCount":
        return html.Div(children=[
            header,
            thematiquesCount
        ])
    elif pathname == "/patternsFrequents":
        return html.Div(children=[
            header,
            patternsFrequents
        ])
    # Si l'utilisateur veut rejoindre une page non existante
    return dbc.Jumbotron(
        [
            html.H1("404: Non trouvée", className="text-danger"),
            html.Hr(),
            html.P(f"La page {pathname} n'existe pas ..."),
        ]
    )


if __name__ == "__main__":
    app.run_server(debug=True)
