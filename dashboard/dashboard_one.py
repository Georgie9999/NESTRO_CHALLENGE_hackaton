import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pathlib
import os
import sys


data = pd.read_excel('../first_table/Приложение 1.xlsx')
data.columns = data.iloc[0]
data = data.drop(0, axis=0)

dollar_course = data['Курс $'][data['Курс $'].notna()]
dollar_data = data.iloc[:, 13][data.iloc[:, 13].notna()]

brent_price = data['Цена Brent,\n$/барр.'][data['Цена Brent,\n$/барр.'].notna()]

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Avocado Analytics: Understand Your Avocados!"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="NESTRO_CHALLENGE_hackaton", className="header-title"
                ),
                html.P(
                    children="Курс доллара, цена на нефть марки Brent и не только",
                    className="header-description",
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
                                    "x": 0.05,
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
                                    "x": 0.05,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": True},
                                "yaxis": {"fixedrange": True},
                                "colorway": ["#E12D39"],
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