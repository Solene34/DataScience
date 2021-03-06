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

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from whitenoise import WhiteNoise

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = 'DataScience-Thématiques'

server = app.server
server.wsgi_app = WhiteNoise(server.wsgi_app, root='static/')

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
    "background-color": "#17a2b8",
    "color": "white"
}

# Style du contenu
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

footer = html.Footer(id="footer", children=[
    html.Hr(),
    html.H6('Laura Biasibetti'),
    html.H6('Solène Issartel'),
    html.H6('Luc Raymond')
], style=FOOTER_STYLE)

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
                dbc.NavLink("Introduction", href="/", active="exact", style={"color": "white", 'font-weight': 'bold'}),
                dbc.NavLink("1- Formatage des données", href="/formatage", active="exact", style={"color": "white", 'font-weight': 'bold'}),
                dbc.NavLink("2- Thématiques : MapReduce", href="/mapReduce", active="exact", style={"color": "white", 'font-weight': 'bold'}),
                dbc.NavLink("3- Thématiques : Extraction", href="/extractThematiques", active="exact",
                            style={"color": "white", 'font-weight': 'bold'}),
                dbc.NavLink("4- Patterns Fréquents", href="/patternsFrequents", active="exact", style={"color": "white", 'font-weight': 'bold'}),
                dbc.NavLink("5- ACP", href="/acp", active="exact", style={"color": "white", 'font-weight': 'bold'}),
                dbc.NavLink("6- Amélioration : correction de nos analyses", href="/ameliorationCorrection", active="exact", style={"color": "white", 'font-weight': 'bold'})
            ],
            vertical=True,
            pills=True,
        ),
        footer
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

# Toute notre application
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

# Presentation dans la rubrique Home
cardPresentationUs = dbc.Card(
    dbc.CardBody([
        html.H6('A propos', className='card-title'),
        html.P('Dans le cadre de notre projet Data Science à l\'école d\'ingénieur Polytech Montpellier, nous avons '
               'réalisé ce site interactif afin de présenter les étapes de notre travail et nos résultats. ',
               className='card-text'),
        html.P('Ce projet s\'inscrit dans l\'apprentissage des matières de Data Mining et de Statistiques que nous '
               'abordons lors de notre 4ème Année du cycle ingénieur.',
               className='card-text')
    ])
)
cardPresentationProject = dbc.Card(
    dbc.CardBody([
        html.H6('Description du projet', className='card-title'),
        html.P("Le sujet de notre projet porte sur l'analyse des mails afin d'en extraire "
               "des thématiques (présentes dans les sujets des mails) "
               "et des personnes qui intéragissent avec ces thématiques (les expéditeurs)",
               className='card-text'
               ),
        html.P("Ainsi, nous allons chercher à mettre en évidence "
               "des liens entre ces thématiques, et également des liens"
               " entre les expéditeurs et les thématiques qu'ils utilisent dans leurs mails.",
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
        html.P('- Interprétation')
    ])
)
presentation = dbc.CardDeck(
    [dbc.Card(cardPresentationUs, color="info", outline=False),
     dbc.Card(cardPresentationProject, color="info", outline=False),
     dbc.Card(cardPresentationPbm, color="info", outline=False)],
)
logos = html.Div([
    dbc.Row(
            [
                dbc.Col(html.Img(src='polytech.png', style={'width': '80%'})),
                dbc.Col(html.Img(src='enron.png', style={'width': '40%'})),
                dbc.Col(html.Img(src='ig.png', style={'width': '30%'}))
            ]
    )
], style={'textAlign':'center'})


# La page avec les thématiques
def extractThemsCount(csvName):
    with open(csvName, newline='') as f:  # Ouverture du fichier CSV
        read = csv.reader(f)  # chargement des lignes du fichier csv
        columns_name = ["Thématiques", "Nombre de mots"]
        themes = []
        length = []
        i = 0
        dic = {}
        for line in read:
            # La première ligne correspond aux titres
            if (i == 0):
                i = 1
            else:
                dic[line[1]] = len((line[2]).split(","))
                themes.append(line[1])
                length.append(len((line[2]).split(",")))
        sorted_dic = sorted(dic.items(), key=lambda item: item[1], reverse=True)
        final_dic = {k: v for k, v in sorted_dic}
    return [columns_name, final_dic]


def extractTabThemsCount(number,csvName):
    datas = extractThemsCount(csvName)
    dic = dict(itertools.islice(datas[1].items(), number))
    return [datas[0], dic.keys(), dic.values()]


# On utilise les méthodes afin de les envoyer au dashboard
data = extractTabThemsCount(10,'data/clean_thematiques.csv')

df = pd.DataFrame({
    data[0][0]: data[1],
    data[0][1]: data[2]
})

figThematique = px.bar(df, x=data[0][0], y=data[0][1])

thematiquesCount = html.Div(children=[
    html.H5(children='Les premières thématiques avec le nombre de mots les composant'),
    dcc.Graph(
        figure=figThematique
    )])

# La page de formatage des données
donnees_formatees = pd.read_csv("data/formatted_data.csv")
formatage_page = html.Div(children=[
    html.H2('1- Formatage des Données'),
    html.H3('1) Suppression des mails n\'étant pas sous un bon format'),
    html.Ul(children=[
        html.Li("On garde seulement les colonnes 'id', 'From', 'To', 'Subject' et 'Content', "
                "les autres ne nous seront pas utiles par la suite,"),
        html.Li("Formatage des noms des expéditeurs sous la forme début_mail(@mail.com), "
                "par exemple, “phillip.allen@enron.com” devient phillip.allen,"),
        html.Li("Suppression des mails qui ne sont pas au bon format de données (décalages, lignes vides etc.),"),
        html.Li("Suppression des mails qui ne comportent ni contenu, ni sujet à la fois.")
    ]),
    html.Hr(),
    html.P("Nous nous retrouvons avec 99 770 mails, au lieu de 100 000 mails."),
    html.P("Les données semblaient assez \"propres\", car nous avons retiré que très peu de mails."),
    html.H3('2) Aperçu de nos données formatées'),
    dt.DataTable(
        id='tabDataFormated',
        style_cell={
            'whiteSpace': 'normal',
            'height': 'auto',
            'textOverflow': 'ellipsis',
            'maxWidth': 0,
            'textAlign': 'left'
        },
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        columns=[{"name": i, "id": i} for i in donnees_formatees.iloc[:, 1:6]],
        data=donnees_formatees.head().to_dict('records'),
        sort_action="native"
    ),
    html.Hr(),
])

# La page présentant le map reduce
map_reduce_data = pd.read_csv("data/map_reduced_subject.csv")
map_reduce_page = html.Div(children=[
    html.H2('2- Création de thématiques avec MapReduce :'),
    html.H3('1) Les différentes étapes de notre MapReduce'),
    html.Ul(children=[
        html.Li("1 Récupération du sujet de tous les mails,"),
        html.Li("2 Suppression des lignes vides (Sans sujet),"),
        html.Li("3 Passage des sujets en minuscules, puis split de chaque mot (Nous nous retrouvons avec "
                "une grande liste de tous les mots rencontrés dans les sujets des mails),"),
        html.Li("4 Enlever les mots inutiles (stop-words),"),
        html.Li("5 Associer un 1 à chaque mot,"),
        html.Li("6 Réduire les mots identiques et additionner le compteur,"),
        html.Li("7 Garder uniquement les mots apparaissant au moins 200 fois.")
    ]),
    html.Hr(),
    html.P("Nous nous retrouvons avec %d mots différents." % (len(map_reduce_data))),
    html.H3('2) Aperçu des mots ressortant les plus dans les mails'),
    dt.DataTable(
        id='tabDataMapReduce',
        style_cell={
            'whiteSpace': 'normal',
            'height': 'auto',
            'textOverflow': 'ellipsis',
            'maxWidth': 0,
            'textAlign': 'left'
        },
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        columns=[{"name": i, "id": i} for i in map_reduce_data.columns],
        data=map_reduce_data[:20].to_dict('records'),
        sort_action="native"
    ),
    html.Hr(),
    html.H3('3) Critiques de notre MapReduce'),
    html.Ul(children=[
        html.Li("Toujours des mots ayant peu d'intérêt ('fwd' par exemple), mais ils sont peu nombreux,"),
        html.Li("Utilisation seulement du sujet des mails, et non pas du contenu => Pertinence des mots récupérés ?")
    ]),
    html.Hr(),
])

# La page présentant les thématiques clean
clean_thematiques_data = pd.read_csv("data/clean_thematiques.csv")
extract_thematiques_page = html.Div(children=[
    html.H2('3- Extraction des thématiques : clustering'),
    html.H3('1) Les différentes étapes de regroupement des mots'),
    html.Ul(children=[
        html.Li("1 On passe nos mots au singulier, pour éviter les doublons,"),
        html.Li("2 Mot proche d'un des autres mots, ou de ses synonymes ? (Librairie WordNet pour avoir la similarité"
                " entre 2 mots, et les synonymes d'un mot),"),
        html.Li("- Oui, alors on les regroupe ensemble, "),
        html.Li("- Non, alors on crée une nouvelle thématique comprenant ce mot,"),
        html.Li("3 Le mot du cluster ressortant le plus donnera son nom à la thématique.")
    ]),
    html.Hr(),
    html.P("Nous nous retrouvons avec %d thématiques différentes." % (len(clean_thematiques_data))),
    html.H3('2) Aperçu des premières thématiques extraites'),
    dt.DataTable(
        id='tabDataThematiques',
        style_cell={
            'whiteSpace': 'normal',
            'height': 'auto',
            'textOverflow': 'ellipsis',
            'maxWidth': 0,
            'textAlign': 'left'
        },
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        columns=[{"name": i, "id": i} for i in clean_thematiques_data.iloc[:, 1:3]],
        data=clean_thematiques_data[:10].to_dict('records'),
        sort_action="native"
    ),
    html.Hr(),
    html.H3('3) Critiques de notre extraction de thématiques'),
    html.Ul(children=[
        html.Li("Mots proches si similaires au moins à 65% (assez faible) => des mots regroupés ensembles"
                " qui ne devraient pas vraiment l'être (trop de mots dans une même thématique),"),
        html.Li("Beaucoup de thématiques composées d'un seul mot.")
    ]),
    html.Hr(),
    thematiquesCount,
    html.Hr(),
])

# La page pour les patterns fréquents
itemsets = pd.read_csv("data/itemsetsFrequents.csv", low_memory=False, header=0)
mails_thematiques = pd.read_csv("data/mails_thematiques.csv")
patternsFrequents = html.Div(children=[
    html.H2('4- Patterns fréquents'),
    html.H3('1) Les différentes étapes pour déterminer les patterns fréquents'),
    html.Ul(children=[
        html.Li("1 Associer les mails aux thématiques (Pour chaque mail, on regarde s'il contient, "
                "pour chaque thématique, un des mots la composant. "
                "Chaque mail se voit donc associé à une liste de thématiques),"),
        html.Li("2 Faire ressortir les itemsets fréquents à l'aide de la librairie fp_growth,"),
        html.Li("3 Garder les itemsets ressortant au moins 100 fois.")
    ]),
    html.Hr(),
    html.P("Nous nous retrouvons avec %d mails comportant des thématiques." % (len(mails_thematiques))),
    html.H3(children='2) Les différentes thématiques associées ensembles'),
    dt.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in itemsets.iloc[:, 1:3]],
        data=itemsets.to_dict('records'),
        sort_action="native",
        style_cell={'textAlign': 'left'},
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        }
    ),
    html.Hr(),
    html.H3(children='3) Critiques de notre fp-growth'),
    html.Ul(children=[
        html.Li("On a seulement gardé les mails comportant au moins une thématique => 70% des mails en moins,"),
        html.Li("Algorithme pour associer les thématiques au mail glouton => 8min40s,"),
        html.Li("Qualité douteuse de certaines thématiques => 'meeting', biaise un peu nos résultats."),
    ]),
    html.Hr()
])


data_exp = pd.read_csv("data/exp_mails.csv")
data_exp = data_exp[["From","Nombre d'emails envoyés"]].sort_values(by=['Nombre d\'emails envoyés'],ascending=False)

figExp = px.bar(data_exp, x="From", y="Nombre d'emails envoyés")

count_mail_exp = html.Div(children=[
    html.H5(children='Le nombre d\'emails envoyé pour chaque expéditeur'),
    dcc.Graph(
        figure=figExp
    )])

data_exp_thematiques_acp = pd.read_csv("data/extracted_data.csv")
tab_exp_thematiques_acp = html.Div(children=[
    dt.DataTable(
        id='tab',
        columns=[{"name": i, "id": i} for i in data_exp_thematiques_acp.iloc[:, 0:5]],
        data=data_exp_thematiques_acp.head().to_dict('records'),
        sort_action="native",
        style_cell={'textAlign': 'left'},
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        }
    )
])

def valeurs_propres(df):
    X = df
    del X['Unnamed: 0']
    # instanciation
    sc = StandardScaler()
    # transformation – centrage
    Z = sc.fit_transform(X)
    acp = PCA(svd_solver='full')
    coord = acp.fit_transform(Z)
    eigenvalues = acp.explained_variance_ratio_[:10]
    return eigenvalues

dfVP = valeurs_propres(data_exp_thematiques_acp)
figVP = px.bar(dfVP, labels={"index": "Dimension", "value": "Part d'inertie"})
count_val_propres = html.Div(children=[
    html.H5(children='Les parts d\'inertie des premières valeurs propres'),
    dcc.Graph(
        figure=figVP
    )])

layoutNuageInd = html.Div([
    html.H3("Nuage des individus"),
    html.Img(src='nuageIndiv.png', style={'width': '60%', 'textAlign': 'center'})
])

layoutNuageVar = html.Div([
    html.H3("Nuage des variables"),
    html.Img(src='nuageVar.png', style={'width': '60%', 'textAlign': 'center'})
])

acp_layout = html.Div(children=[
    html.H2('5- ACP'),
    html.H3('1) Préparation de l\'ACP'),
    html.P("Nous avons choisi de faire une ACP afin de :"),
    html.Ul(children=[
        html.Li("Représenter les 73 individus sur 2 dimensions,"),
        html.Li("Représenter les 66 thématiques sur 2 dimensions,"),
        html.Li("Voir si on peut mettre en lien les individus et les thématiques,"),
        html.Li("Identifier des individus atypiques ou des comportements moyens.")
    ]),
    html.Hr(),
    html.H3('2) Tableau de données des individus, et du nombre de fois qu\'ils traitent chaque thématique'),
    tab_exp_thematiques_acp,
    html.Hr(),
    count_mail_exp,
    html.H3('3) Les valeurs propres'),
    count_val_propres,
    html.Hr(),
    html.H3('4) Résultats de l\'ACP'),
    layoutNuageInd,
    html.Hr(),
    layoutNuageVar,
    html.Hr(),
    html.H3('5) Critiques'),
    html.Ul(children=[
        html.Li("60% de perte de données,"),
        html.Li("Nous n'avons pu analyser que peu d’individus => 8 individus sur 73,"),
        html.Li("Thématiques => majorité sur l'axe 1,"),
        html.Li("Individus => majorité au centre du graphe."),
    ]),
    html.H6('Important : toutes les interprétations faites ne sont pas vraiment fiables.'),
    html.Hr(),
])


# On utilise les méthodes afin de les envoyer au dashboard
data2 = extractTabThemsCount(10,'data/clean_thematiques2.csv')

df2 = pd.DataFrame({
    data2[0][0]: data2[1],
    data2[0][1]: data2[2]
})

figExp2 = px.bar(df2, x=data2[0][0], y=data2[0][1])

thematiquesCount2 = html.Div(children=[
    html.H5(children='Les premières thématiques avec le nombre de mots les composant'),
    dcc.Graph(
        figure=figExp2
    )])

data_exp_thematiques_acp2 = pd.read_csv("data/extracted_data2.csv")
tab_exp_thematiques_acp2 = html.Div(children=[
    dt.DataTable(
        id='tab',
        columns=[{"name": i, "id": i} for i in data_exp_thematiques_acp2.iloc[:, 0:5]],
        data=data_exp_thematiques_acp2.head().to_dict('records'),
        sort_action="native",
        style_cell={'textAlign': 'left'},
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        }
    )
])

layoutNuageInd2 = html.Div([
    html.H3("Nuage des individus"),
    html.Img(src='nuageIndiv2.png', style={'width': '60%', 'textAlign': 'center'})
])

layoutNuageVar2 = html.Div([
    html.H3("Nuage des variables"),
    html.Img(src='nuageVar2.png', style={'width': '60%', 'textAlign': 'center'})
])

itemsets2 = pd.read_csv("data/itemsetsFrequents2.csv")
amelioration_page = html.Div(children=[
    html.H2('6- Amélioration : correction de nos analyses'),
    html.H3('1) Meilleure façon d\'associer les mails aux thématiques'),
    html.P("Nous nous sommes rendus compte au dernier moment que notre association de thématiques aux mails "
           "était complètement naïve (Se met avec le premier mot proche, sans regarder les autres)"),
    thematiquesCount2,
    html.Hr(),
    html.H3('2) Nouveau tableau de données des individus, et du nombre de fois qu\'ils traitent chaque thématique'),
    tab_exp_thematiques_acp2,
    html.Hr(),
    html.H3(children='3) Les thématiques associées ensembles'),
    dt.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in itemsets2.iloc[:, 1:3]],
        data=itemsets2.to_dict('records'),
        sort_action="native",
        style_cell={'textAlign': 'left'},
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        }
    ),
    html.Hr(),
    html.H3('4) Nouveaux résultats de l\'ACP'),
    layoutNuageInd2,
    html.Hr(),
    layoutNuageVar2,
    html.Hr(),
])

# Permet de mettre à jour la page selon le lien
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.Div(children=[
            header,
            html.H4('Présentation'),
            presentation,
            logos
        ])
    elif pathname == "/formatage":
        return html.Div(children=[
            header,
            formatage_page
        ])
    elif pathname == "/mapReduce":
        return html.Div(children=[
            header,
            map_reduce_page
        ])
    elif pathname == "/extractThematiques":
        return html.Div(children=[
            header,
            extract_thematiques_page
        ])
    elif pathname == "/patternsFrequents":
        return html.Div(children=[
            header,
            patternsFrequents
        ])
    elif pathname == "/acp":
        return html.Div(children=[
            header,
            acp_layout
        ])
    elif pathname == "/ameliorationCorrection":
        return html.Div(children=[
            header,
            amelioration_page
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
