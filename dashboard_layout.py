import datetime as dt

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from states.helper import state_code_dict
from districts.helper import districts


def get_dropdown_for_row(dropdown_text, dropdown_id, dropdown_options, default_value):
    """
    dropdown data in bootstrap row
    :param dropdown_text: name of dropdown
    :param dropdown_id: id of dropdown
    :param dropdown_options: options in dropdown menu
    :param default_value: default selected value of dropdown
    :return: list of two bootstrap columns containing dropdown name and menu
    """
    return [
        dbc.Col(html.Div(dropdown_text), md=1),
        dbc.Col(
            dcc.Dropdown(id=dropdown_id,
                         options=dropdown_options,
                         value=default_value
                         ),
            md=3),
    ]


def get_date_input_for_row(date_id, n_past_days=40):
    """
    date data in bootstrap row
    :param date_id: id of date picker
    :param n_past_days: default value in datepicker, go back that many days from today
    :return: list of two bootstrap columns containing name for datepicker input and the datepicker
    """
    return [
        dbc.Col(html.Div("Start Date:"), md=1),
        dbc.Col(
            dcc.Input(
                id=date_id,
                type='Date',
                value=dt.date.today() - dt.timedelta(days=n_past_days)
            ),
            md=3),
    ]


def get_graphs_for_row(levitt_graph_id, daily_new_graph_id, daily_active_graph_id):
    """
    three graphs (levitt's measure graph, daily new cases graph, daily active cases graph) for bootstrap row
    :param levitt_graph_id: id of levitt's measure graph used for prediction
    :param daily_new_graph_id: id of daily new cases graph
    :param daily_active_graph_id: id of daily active cases graph
    :return: list of three bootstrap columns that will contain the three graphs
    """
    return [
        dbc.Col(dbc.Card(html.Div(id=levitt_graph_id)), md=4),
        dbc.Col(dbc.Card(html.Div(id=daily_new_graph_id)), md=4),
        dbc.Col(dbc.Card(html.Div(id=daily_active_graph_id)), md=4),
    ]


dashboard_layout = dbc.Container(
    [
        html.H1("Analyzing COVID-19 trends in India via Levitt's Measure"),
        html.P(children=["Levitt's measure H(t) for day t for COVID-19 is a very simple measure, it is defined as H("
                         "t)=X(t)/X(t-1), where X(t) is the cumulative number of COVID-19 cases on day t. When the "
                         "value of H(t) approximately equals 1 (we have taken 1.0001) then the situation will be "
                         "better and the number of new cases per day will become considerably low.", html.Br(),
                         "More information about Levitt's measure is given here: ",
                         html.A("Conceptual basis of the Levitt's measure",
                                href="https://drive.google.com/file/d/1bnZ1tLP1hOJJ2GeQFEMTK5cPjEdHvyf2/view?usp"
                                     "=sharing"),
                         ]
               ),
        html.P(children=["Three graphs are plotted for each:", html.Br(),
                         html.B("1) H(t) for India as t varies,"), html.Br(),
                         html.B("2) H(t) for States/Union Territories of India as t varies,"), html.Br(),
                         html.B("3) H(t) for Districts of India as t varies."), html.Br(),
                         "For each of the above, the first graph shows daily H(t). The regression line is fitted on "
                         "last 40 days daily H(t). However, user can specify the start date explicitly to manually "
                         "adjust how many past days H(t) to be used for fitting, the line is then extrapolated till "
                         "H(t) reaches 1.0001. R-squared value is shown which measures the goodness of the fit. "
                         "R-squared normally takes a value between 0 and 1, generally higher the value, better is the "
                         "fit. The line is not extrapolated if it's slope is positive or r-squared value is less than "
                         "0.1, as it will be meaningless. Choice of states/union territories, and of districts can be "
                         "made using the corresponding drop-down menu. The second and third graphs show the daily new "
                         "cases, and the daily active cases, respectively. "
                         ]
               ),
        html.P(children=[html.B("Disclaimer: "), "It must be understood that the prediction shown here is based on a "
                                                 "certain trend in the current data, therefore, if certain "
                                                 "circumstances arise in future that alter the current trend, "
                                                 "then the prediction will not hold. "
                         ]
               ),
        html.Hr(),
        # for India
        dbc.Row(get_date_input_for_row("in-start-date"), align="center"),
        html.P(html.B("Plots for India"), style={'text-align': 'center'}),
        dbc.Row(get_graphs_for_row("in-levitt", "in-daily-new", "in-daily-active"), align="center"),
        html.Hr(),
        # for states
        dbc.Row(get_dropdown_for_row("Choose State:", "state-dropdown",
                                     [{'label': state, 'value': state_code} for state, state_code in
                                      state_code_dict.items()], "mh") + get_date_input_for_row("state-start-date"),
                align="center"),
        html.P(html.B("Plots for a State"), style={'text-align': 'center'}),
        dbc.Row(get_graphs_for_row("state-levitt", "state-daily-new", "state-daily-active"), align="center"),
        html.Hr(),
        # for districts
        dbc.Row(get_dropdown_for_row("Choose District:", "district-dropdown",
                                     [{'label': district, 'value': district} for district in districts],
                                     "Mumbai") + get_date_input_for_row("district-start-date"), align="center"),
        html.P(html.B("Plots for a District"), style={'text-align': 'center'}),
        dbc.Row(get_graphs_for_row("district-levitt", "district-daily-new", "district-daily-active"), align="center"),
        html.Hr(),
        # footer
        html.Footer(children=
        [
            html.P(children=[
                "Data Source: ",
                html.A("Covid19 India", href="https://github.com/covid19india/api"),
            ]
            ),
        ]
        ),
    ],
    fluid=True,
)
