import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_mantine_components as dmc
from datetime import timedelta, datetime

from dash import Output, Input, callback, dash_table
from dateutil.relativedelta import relativedelta

data = pd.read_excel('../first_table/Приложение 1.xlsx')
data.columns = data.iloc[0]
data = data.drop(0, axis=0)

dollar_course = data['Курс $'][data['Курс $'].notna()]
dollar_course.iloc[0] = 94.11
dollar_data = data.iloc[:, 13][data.iloc[:, 13].notna()]
dollar = pd.DataFrame({"Дата": dollar_data, "Курс доллара, руб.": dollar_course})

brent_price = data['Цена Brent,\n$/барр.'][data['Цена Brent,\n$/барр.'].notna()]
spread_price = data['Spread (Корректировка),\n$/барр.'][data['Spread (Корректировка),\n$/барр.'].notna()]
freight_price = data['Freight (Корректировка),\n$/барр.'][data['Freight (Корректировка),\n$/барр.'].notna()]

price = pd.DataFrame({"Дата": dollar_data, "Цена Brent, $/барр.": brent_price,
                      "Spread (Корректировка), $/барр.": spread_price,
                      "Freight (Корректировка), $/барр.": freight_price})

customers = pd.read_csv("../first_table/customers.csv").drop('Unnamed: 0', axis=1)

customers_values = customers['Покупатель']
profit_course = customers['Прибыль за счёт изменения курса (руб)']
cash_course = customers['Поступление (руб)']
customers = pd.DataFrame({"Покупатель": customers_values,
                          "Прибыль за счёт изменения курса (руб)": profit_course,
                          "Поступление (руб)": cash_course})

urals = pd.read_csv("../first_table/urals.csv")['Urals']

oil_price_urals = pd.DataFrame(
    {"Дата_urals": [datetime(2022, 2, 1) + relativedelta(months=+i) for i in range(11)],
     "Цена Юралс, $/барр.": urals})

oil_price_brent = pd.DataFrame(
    {"Дата_brent": dollar_data,
     "Цена Brent, $/барр.": brent_price})

app = dash.Dash(__name__)
app.title = "Dashboard for 3 case"

app.layout = html.Div([
    html.Div(children=[html.H1(children='NESTRO_CHALLENGE_hackaton', style={'textAlign': 'center'}),
                       html.H2(children='АО «Зарубежнефть»', style={'textAlign': 'center'})]),

    html.Div(children=[html.H2(children='Курс доллара, руб.'),
                       dash_table.DataTable(data=dollar.to_dict('records'), page_size=6),
                       dcc.Graph(figure=px.line(dollar, x='Дата', y='Курс доллара, руб.', markers=True,
                                                color_discrete_sequence=["orange"]))]),

    dmc.Grid([
        dmc.Col([html.H2(children='Цена нефти Юралс по месяцам(2022), $/барр.'),
                 dcc.Graph(figure=px.line(oil_price_urals,
                                          x="Дата_urals", y="Цена Юралс, $/барр.", markers=True,
                                          color_discrete_sequence=["green"]))
                 ], span=6),
        dmc.Col([html.H2(children='Цена на нефть марки Brent, $'),
                 dcc.Graph(figure=px.line(oil_price_brent, x="Дата_brent",
                                          y="Цена Brent, $/барр.", markers=True))
                 ], span=6),
    ]),

    dmc.Grid([
        dmc.Col([html.H2(children='Гистограмма поступления денежных средств с учетом курса, руб.'),
                 dash_table.DataTable(data=customers.to_dict('records'), page_size=11,
                                      style_table={'overflowX': 'auto'})
                 ], span=6),
        dmc.Col([
            dcc.Graph(figure=px.histogram(customers, x='Покупатель',
                                          y=['Прибыль за счёт изменения курса (руб)',
                                             "Поступление (руб)"],barmode='group'))
        ], span=6),
    ]),

    html.Div(children=[html.H2(children='Гистограмма изменения котировок, $/ барр.'),
                       dash_table.DataTable(data=price.to_dict('records'), page_size=11,
                                            style_table={'overflowX': 'auto'}),
                       dcc.Graph(figure=px.histogram(price, x='Дата',
                                                     y=['Цена Brent, $/барр.',
                                                        "Spread (Корректировка), $/барр.",
                                                        "Freight (Корректировка), $/барр."], nbins=20,barmode='group'))])
])

if __name__ == '__main__':
    app.run(debug=True)

