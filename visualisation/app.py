import csv
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_table as dt
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import itertools

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title='DataScience-Thématiques'

# Style du footer
FOOTER_STYLE = {
    "position": "fixed",
    "bottom": 0,
    "padding": "1rem 1rem"
}
# Style de la side bar bootstrap
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#17a2b8"
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
                dbc.NavLink("X- Thématiques", href="/thematiquesCount", active="exact"),
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
# Le titre de notre page
titleDash = html.Title(id="title", children=[html.Title(children="DataScience")])
# Notre header présent sur toutes les pages
header = html.Header(id="header", children=[
    html.H1(children='Projet DATA SCIENCE'),
    html.Hr()
])
# Notre footer présent sur toutes les pages
footer = html.Footer(id="footer", children=[
    html.Hr(),
    html.H6(children='par Luc Raymond, Solène Issartel, Laura Biasibetti')],
    style=FOOTER_STYLE)


# Toute notre application
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


# Presentation dans la rubrique Home
cardPresentationUs = dbc.Card(
    dbc.CardBody([
        html.H6('A propos', className='card-title'),
        html.P('Bonjour, nous sommes trois élèves de Polytech Montpellier en Informatique et Gestion.',
            className='card-text')
    ])
)
cardPresentationProject = dbc.Card(
    dbc.CardBody([
        html.H6('Description du projet', className='card-title'),
        html.P("Nous analysons des mails afin d'extraire "
               "des thématiques (contenus dans les sujets) "
               "et des personnes (destinataire, expéditeur) "
               "Ainsi nous pouvons établir des corrélations "
               "entre ces différents éléments.",
               className='card-text'
               )
    ])
)
cardPresentationPbm = dbc.Card(
    dbc.CardBody([
        html.H6('Déroulement', className='card-title'),
        html.P('- Formatage des données '),
        html.P('- Extraire les données (thématiques et personnes) '),
        html.P("- Exécuter des méthodes d'analyse "),
        html.P('- Interpréation')
    ])
)
presentation = dbc.CardDeck(
    [dbc.Card(cardPresentationUs, color="info", outline=False),
     dbc.Card(cardPresentationProject, color="info", outline=False),
     dbc.Card(cardPresentationPbm, color="info", outline=False)],
)

# La page avec les thématiques
def extractThemsCount():
    with open('data/clean_thematiques.csv', newline='') as f:  # Ouverture du fichier CSV
        read = csv.reader(f)  # chargement des lignes du fichier csv
        columns_name = ["Thématiques", "Nombre de mots"]
        print(columns_name)
        themes = []
        length = []
        i = 0
        dic = {}
        for line in read:
            # La première ligne correspond aux titres
            if (i == 0) :
                i = 1
            else:
                dic[line[1]] = len((line[2]).split(","))
                themes.append(line[1])
                length.append(len((line[2]).split(",")))
        sorted_dic = sorted(dic.items(), key=lambda item: item[1], reverse=True)
        final_dic = {k: v for k, v in sorted_dic}
        print(final_dic)
    return [columns_name, final_dic]
def extractTabThemsCount(number):
    datas = extractThemsCount()
    dic = dict(itertools.islice(datas[1].items(), number))
    return [datas[0], dic.keys(), dic.values()]
# On utilise les méthodes afin de les envoyer au dashboard
data = extractTabThemsCount(10)

df = pd.DataFrame({
    data[0][0]: data[1],
    data[0][1]: data[2]
})

figThematique = px.bar(df, x=data[0][0], y=data[0][1])

thematiquesCount = html.Div(children=[
    html.H5(children='Analyse des thématiques abordées ensemble dans les mails'),
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
            html.H4('Présentation'),
            presentation,
            footer
        ])
    elif pathname == "/formatage":
        return html.Div(children=[
            header,
            footer
        ])
    elif pathname == "/thematiquesCount":
        return html.Div(children=[
            header,
            thematiquesCount,
            footer
        ])
    elif pathname == "/patternsFrequents":
        return html.Div(children=[
            header,
            patternsFrequents,
            footer
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
