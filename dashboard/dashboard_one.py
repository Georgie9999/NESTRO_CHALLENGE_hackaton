import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import timedelta, datetime
from dateutil.relativedelta import *



data = pd.read_excel('../first_table/Приложение 1.xlsx')
data.columns = data.iloc[0]
data = data.drop(0, axis=0)

dollar_course = data['Курс $'][data['Курс $'].notna()]
dollar_data = data.iloc[:, 13][data.iloc[:, 13].notna()]

brent_price = data['Цена Brent,\n$/барр.'][data['Цена Brent,\n$/барр.'].notna()]

spread_price = data['Spread (Корректировка),\n$/барр.'][data['Spread (Корректировка),\n$/барр.'].notna()]
freight_price = data['Freight (Корректировка),\n$/барр.'][data['Freight (Корректировка),\n$/барр.'].notna()]


customers = pd.read_csv("../first_table/customers.csv").drop('Unnamed: 0', axis = 1)
# print(customers)
customers_values = customers['Покупатель']
profit_course = customers['Прибыль за счёт изменения курса (руб)']
cash_course = customers['Поступление (руб)']

urals = pd.read_csv("../first_table/urals.csv")['Urals']

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Dashboard for 3 case"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="NESTRO_CHALLENGE_hackaton", className="header-title"
                ),


            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    "x": dollar_data,
                                    "y": dollar_course,
                                    "type": "lines",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Курс доллара, руб.",
                                    "x": 0.45,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": True},
                                "yaxis": {
                                    "fixedrange": True,
                                },
                                "colorway": ["#17B897"],
                            },
                        },
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    "x": [datetime(2022, 2, 1)+ relativedelta(months=+i) for i in range(11)],
                                    "y": urals,
                                    "type": "lines",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Цена нефти Юралс по месяцам(2022), $/барр.",
                                    "x": 0.45,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": True},
                                "yaxis": {
                                    "fixedrange": True,
                                },
                                "colorway": ["#F12D39"],
                            },
                        },
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="volume-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    "x": dollar_data,
                                    "y": brent_price,
                                    "type": "lines",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Цена на нефть марки Brent, $",
                                    "x": 0.45,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": True},
                                "yaxis": {"fixedrange": True},
                                "colorway": ["#2d7be1"],
                            },
                        },
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="volume-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    "x": dollar_data,
                                    "y": brent_price,
                                    "type": "bar",
                                    "name": "Brent price, $/барр."
                                },
                                {
                                    "x": dollar_data,
                                    "y": spread_price,
                                    "type": "bar",
                                    "name": "Spread, $/барр.",
                                },
                                {
                                    "x": dollar_data,
                                    "y": freight_price,
                                    "type": "bar",
                                    "name": "Freiqht, $/барр.",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Гистограмма изменения котировок, $/ барр.",
                                    "x": 0.45,
                                    "xanchor": "left",
                                },
                            },
                        },
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="volume-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    "x": customers_values,
                                    "y": profit_course,
                                    "type": "bar",
                                    "name": "Прибыль за счёт изменения курса (руб)"
                                },
                                {
                                    "x": customers_values,
                                    "y": cash_course,
                                    "type": "bar",
                                    "name": "Поступление (руб)",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Гистограмма поступления денежных средств с учетом курса, руб.",
                                    "x": 0.40,
                                    "xanchor": "left",
                                },
                            },
                        },
                    ),
                    className="card",
                ),

            ],
            className="wrapper",
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
