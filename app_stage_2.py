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

rf_mod = pickle.load(open("C:\\Users\\pawel\\OneDrive\\Dokumenty\\ATLAS\\HackYeah2023HWB_ATLAS\\models\\stage_2\\model_knn.pkl", "rb"))

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

            html.Label("How many times have you been pregnant?"),
            html.Br(),
            dcc.Input(id="pregnant", value = "", max=20),
            html.Br(),

            html.Label("What is your blood pressure?"),
            html.Br(),
            dcc.Input(id="pressure", value = "", max=300),
            html.Br(),

            html.Label("What is your Body Mass Index (BMI)?"),
            html.Br(),
            dcc.Input(id="bmi", value = "", max=50),
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
        State(component_id = "pregnant", component_property = "value"),
        State(component_id = "pressure", component_property = "value"),
        State(component_id = "bmi", component_property = "value"),
        State(component_id = "age", component_property = "value"),

)
def pred_client(n_clicks, pregnant, pressure, bmi, age):
    if n_clicks >0:
        try:
            data1 = {
                    "Pregnancies": pregnant,
                    "BloodPressure": pressure,
                    "BMI": bmi,
                    "Age": age}
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