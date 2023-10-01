from dash import Dash, dcc, html
from dash import dash_table
from dash import callback_context, callback
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
import dash_daq as daq
import pickle
import os
import xgboost as xgb
import pandas as pd

# current_dir = os.getcwd()
# model_file = os.path.join(current_dir, 'models', 'stage_1', 'model_xgb.pkl')
# xgb_mod = pickle.load(open(model_file, "rb"))

rf_mod = pickle.load(open("C:\\Users\\pawel\\OneDrive\\Dokumenty\\ATLAS\\HackYeah2023HWB_ATLAS\\models\\stage_1\\model_rf.pkl", "rb"))

app = Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])
app.title='Diabeater'

app.layout=html.Div([
    #html.H1('Diabeater'),
    dbc.NavbarSimple(
        brand="Diabeater",
        color="primary", ### TUTAJ KOLOR NA SAMEJ GÓRZE DO WYBORU
        dark=True,
        className="mb-2",
),
html.H5('Answer questions below'),

            html.Label("Have you experienced excessive urination?"),
            dcc.RadioItems(options = [{'label': 'Yes', 'value': 1},
                            {'label': 'No', 'value': 0}],
                            id = 'polyuria'),
            html.Br(),

            html.Label("Have you experienced excessive thirst/excess drinking?"),
            dcc.RadioItems(options = [{'label': 'Yes', 'value': 1},
                            {'label': 'No', 'value': 0}],
                            id = 'polydipsia'),
            html.Br(),

            html.Label("Have you experienced an episode of sudden weight loss?"),
            dcc.RadioItems(options = [{'label': 'Yes', 'value': 1},
                            {'label': 'No', 'value': 0}],
                            id = 'weight-loss'),
            html.Br(),

            html.Label("Have you experienced an episode of feeling weak?"),
            dcc.RadioItems(options = [{'label': 'Yes', 'value': 1},
                            {'label': 'No', 'value': 0}],
                            id = 'weakness'),
            html.Br(),

            html.Label("Have you experienced an episode of excessive/extreme hunger?"),
            dcc.RadioItems(options = [{'label': 'Yes', 'value': 1},
                            {'label': 'No', 'value': 0}],
                            id = 'polyphagia'),
            html.Br(),

            html.Label("Have you experienced a yeast infection?"),
            dcc.RadioItems(options = [{'label': 'Yes', 'value': 1},
                            {'label': 'No', 'value': 0}],
                            id = 'genital-thrush'),
            html.Br(),

            html.Label("Have you experienced an episode of blurred vision?"),
            dcc.RadioItems(options = [{'label': 'Yes', 'value': 1},
                            {'label': 'No', 'value': 0}],
                            id = 'visual-blurring'),
            html.Br(),

            html.Label("Have you experienced an episode of itch?"),
            dcc.RadioItems(options = [{'label': 'Yes', 'value': 1},
                            {'label': 'No', 'value': 0}],
                            id = 'itching'),
            html.Br(),

            html.Label("Have you experienced an episode of irritability?"),
            dcc.RadioItems(options = [{'label': 'Yes', 'value': 1},
                            {'label': 'No', 'value': 0}],
                            id = 'irritability'),
            html.Br(),

            html.Label("Have you noticed delayed healing when wounded?"),
            dcc.RadioItems(options = [{'label': 'Yes', 'value': 1},
                            {'label': 'No', 'value': 0}],
                            id = 'delayed-healing'),
            html.Br(),

            html.Label("Have you experienced an episode of weakening of a muscle/group of muscles?"),
            dcc.RadioItems(options = [{'label': 'Yes', 'value': 1},
                            {'label': 'No', 'value': 0}],
                            id = 'partial-paresis'),
            html.Br(),

            html.Label("Have you experienced an episode of muscle stiffness?"),
            dcc.RadioItems(options = [{'label': 'Yes', 'value': 1},
                            {'label': 'No', 'value': 0}],
                            id = 'muscle-stiffness'),
            html.Br(),

            html.Label("Have you experienced an episode of alopecia?"),
            dcc.RadioItems(options = [{'label': 'Yes', 'value': 1},
                            {'label': 'No', 'value': 0}],
                            id = 'alopecia'),
            html.Br(),

            html.Label("According to your Body Mass Index, are you obese?"),
            dcc.RadioItems(options = [{'label': 'Yes', 'value': 1},
                            {'label': 'No', 'value': 0}],
                            id = 'obesity'),
            html.Br(),

            html.Label("What is your gender?"),
            dcc.RadioItems(options = [{'label': 'Male', 'value': 1},
                            {'label': 'Female', 'value': 0}],
                            id = 'gender'),
            html.Br(),

            html.Label("How old are you?"),
            html.Br(),
            dcc.Input(id="age", value = "", max=130),
            html.Br(),
            html.Br(),

            html.Div([
                html.Button('Submit', id='submit-val', n_clicks=0), 
                html.Div(id='container-button-basic')]),

            html.Br()




]
)

@app.callback(
        Output(component_id = "container-button-basic", component_property = "children"),
        Input('submit-val', 'n_clicks'),
        State(component_id = "polyuria", component_property = "value"),
        State(component_id = "polydipsia", component_property = "value"),
        State(component_id = "weight-loss", component_property = "value"),
        State(component_id = "weakness", component_property = "value"),
        State(component_id = "polyphagia", component_property = "value"),
        State(component_id = "genital-thrush", component_property = "value"),
        State(component_id = "visual-blurring", component_property = "value"),
        State(component_id = "itching", component_property = "value"),
        State(component_id = "irritability", component_property = "value"),
        State(component_id = "delayed-healing", component_property = "value"),
        State(component_id = "partial-paresis", component_property = "value"),
        State(component_id = "muscle-stiffness", component_property = "value"),
        State(component_id = "alopecia", component_property = "value"),
        State(component_id = "obesity", component_property = "value"),
        State(component_id = "gender", component_property = "value"),
        State(component_id = "age", component_property = "value")

)
def pred_client(n_clicks, polyuria, polydipsia, weight_loss, weakness, polyphagia, genital_thrush, visual_blurring, itching, irritability, delayed_healing, partial_paresis, muscle_stiffness, alopecia, obesity, gender, age):
    if n_clicks >0:
        try:
            if gender==1:
                gender_Male = 1
                gender_Female = 0
            else:
                gender_Male = 0
                gender_Female = 1
            data1 = {"age": age,
                    "polyuria": polyuria,
                    "polydipsia": polydipsia,
                    "sudden_weight_loss": weight_loss,
                    "weakness": weakness,
                    "polyphagia": polyphagia,
                    "genital_thrush": genital_thrush,
                    "visual_blurring": visual_blurring,
                    "itching": itching,
                    "irritability": irritability,
                    "delayed_healing": delayed_healing,
                    "partial_paresis": partial_paresis,
                    "muscle_stiffness": muscle_stiffness,
                    "alopecia": alopecia,
                    "obesity": obesity,
                    "gender_Female": gender_Female,
                    "gender_Male": gender_Male}
            df_test = pd.DataFrame([data1])
            probability = rf_mod.predict_proba(df_test)[:,1]#[0][1]
            probability = int(probability * 100)
            binary = rf_mod.predict(df_test)
            if binary==1:
                binary = "You might suffer from diabetes"
            else:
                binary = "You probably don't suffer from diabetes"
            if probability > 99:
                probability = 99
            elif probability < 1:
                probability = 1
            return f'{binary}. Chance of you suffering from diabetes is {probability}%.'
        except ValueError:
            return 'Something went wrong. Make sure you filled the form correctly.'


if __name__ == '__main__':
    app.run_server(port=8090, debug=True)