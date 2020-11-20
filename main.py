import math
import datetime as dt
import warnings
import pandas as pd
import numpy as np

from sklearn.metrics import r2_score

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output

from states.helper import get_state_df, reverse_state_code_dict
from districts.helper import get_district_df
from india.helper import get_in_df

from dashboard_layout import dashboard_layout

warnings.filterwarnings("ignore")

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Levitt's Measure"
server = app.server


def get_graph(graph_id, x_values, y_values, title, label_x, label_y):
    """
    creates a dash core component graph with the passed parameters
    :param graph_id: id of the graph
    :param x_values: x axis values
    :param y_values: y axis values
    :param title: title of the graph
    :param label_x: x axis label
    :param label_y: y axis label
    :return: dash core component graph created with the passed parameters
    """
    return dcc.Graph(id=graph_id,
                     figure={
                         'data': [
                             {'x': x_values, 'y': y_values, 'mode': 'lines+markers'},
                         ],
                         'layout': {
                             'title': title,
                             'xaxis': {
                                 'title': label_x
                             },
                             'yaxis': {
                                 'title': label_y
                             }
                         }
                     }),


def get_graph_with_regression_line(graph_id, x1_values, y1_values, x2_values, y2_values, r_squared, title):
    """
    creates two plots on the same graph (Regression line plot and scatter plot of daily Levitt's Measure H(t)) with the
    passed parameters
    :param graph_id: id of the graph
    :param x1_values: x axis values for the first plot (scatter plot of daily H(t))
    :param y1_values: y axis values for the first plot
    :param x2_values: x axis values for the second plot (regression line plot)
    :param y2_values: y axis values for the second plot
    :param r_squared: r-squared value of regression line
    :param title: title of the graph
    :return: dash core component graph with two plots (Regression line plot and scatter plot of daily H(t))
    """
    return dcc.Graph(id=graph_id,
                     figure={
                         'data': [
                             {'x': x1_values, 'y': y1_values, 'mode': 'markers', 'name': 'H(t)'},
                             {'x': x2_values, 'y': y2_values, 'mode': 'line',
                              'name': "Regression Line<br> R² = " + str(r_squared)},
                         ],
                         'layout': {
                             'title': title,
                             'xaxis': {
                                 'title': "Date",
                             },
                             'yaxis': {
                                 'title': "Levitt's Measure H(t)"
                             }
                         }
                     })


def get_data_for_graph_with_regression_line(df_levitt, start_date):
    """
    relevant data to plot regression line
    :param df_levitt: dataframe of India/States/Districts
    :param start_date: date from which data is to be considered
    :return: dataframe containing Levitt Measure H(t) for each day, dates corresponding to each H(t) and predicted
    H(t), regression model, regression line, r squared value of regression line
    """
    df_levitt = df_levitt[df_levitt['date'] > start_date]
    df_levitt = df_levitt.reset_index(drop=True)
    df_levitt['LevittMeasure'] = np.NaN
    # Levitt Measure Calculation
    for i in reversed(range(1, len(df_levitt))):
        numerator = df_levitt.iloc[i]['cum_confirmed']
        denominator = df_levitt.iloc[i - 1]['cum_confirmed']
        if denominator > 0:
            df_levitt.at[i, 'LevittMeasure'] = numerator / denominator
    # line fit code
    days = range(0, len(df_levitt))
    df_levitt = df_levitt.assign(day_count=pd.Series(days).values)
    X_train, y_train = df_levitt['day_count'], df_levitt['LevittMeasure']
    idx = np.isfinite(X_train) & np.isfinite(y_train)
    X_train, y_train = X_train[idx], y_train[idx]
    model = np.poly1d(np.polyfit(X_train, y_train, 1))
    # day till which fitted regression line needs to be extrapolated
    required_day = (1.0001 - model.coeffs[1]) / model.coeffs[0]
    # get dates corresponding to day number
    dates = []
    # if slope is positive or r-squared value is less than equal to 0.1 then do not extrapolate
    if required_day < 0 or r2_score(y_train, model(X_train)) <= 0.1:
        line = np.linspace(0, len(X_train), len(X_train))
    else:
        # required day can have decimal, use ceil to get integer
        line = np.linspace(0, math.ceil(required_day), math.ceil(required_day))
        # find more dates needed for plotting
        more_dates = math.ceil(required_day) - len(days)
        last_date = df_levitt.iloc[-1]['date']
        for i in range(more_dates):
            dates.append(last_date + dt.timedelta(i + 1))
    return df_levitt, dates, model, line, round(r2_score(y_train, model(X_train)), 2)


# get india dataframe containing required parameters
df_in_daily = get_in_df()

# set app layout to dashboard layout
app.layout = dashboard_layout


@app.callback(
    [Output('in-levitt', 'children'), Output('in-daily-new', 'children'), Output('in-daily-active', 'children')],
    [Input(component_id='in-start-date', component_property='value')]
)
def update_graph(in_start_date):
    """
    creates three graphs using India data: daily Levitt's measure graph with fitted regression line, daily new cases
    graph, daily active cases graph to be placed in a bootstrap row
    :param in_start_date: date from which data is to be considered
    :return: list of three dash core component graphs
    """
    if dt.datetime.strptime(in_start_date, "%Y-%m-%d") > pd.to_datetime("2020-03-01"):
        start_date = dt.datetime.strptime(in_start_date, "%Y-%m-%d")
        daily_new_graph = get_graph("in-daily-new-graph", df_in_daily['date'], df_in_daily['dailyconfirmed'],
                                    "Daily New Cases India", "Date", "New Cases")
        daily_active_graph = get_graph("in-daily-active-graph", df_in_daily['date'], df_in_daily['active'],
                                       "Daily Active Cases India", "Date", "Active Cases")
        df_in_levitt, dates, model, line, r_squared = get_data_for_graph_with_regression_line(df_in_daily, start_date)
        regression_graph = get_graph_with_regression_line("in-levitt-graph", df_in_levitt['date'],
                                                          df_in_levitt['LevittMeasure'],
                                                          list(df_in_levitt['date']) + dates, model(line), r_squared,
                                                          "Daily Levitt's Measure H(t) India")
        return [regression_graph, daily_new_graph, daily_active_graph]


@app.callback(
    [Output('state-levitt', 'children'), Output('state-daily-new', 'children'),
     Output('state-daily-active', 'children')],
    [Input(component_id='state-dropdown', component_property='value'),
     Input(component_id='state-start-date', component_property='value')]
)
def update_graph(state_dropdown_code, state_start_date):
    """
    creates three graphs using Indian states data: daily Levitt's measure graph with fitted regression line, daily new
    cases graph, daily active cases graph to be placed in a bootstrap row
    :param state_dropdown_code: state code of selected state from the dropdown menu of Indian states
    :param state_start_date: date from which data is to be considered
    :return: list of three dash core component graphs
    """
    if dt.datetime.strptime(state_start_date, "%Y-%m-%d") > pd.to_datetime("2020-03-01"):
        start_date = dt.datetime.strptime(state_start_date, "%Y-%m-%d")
        df_state_daily = get_state_df(state_dropdown_code)
        daily_new_graph = get_graph("state-daily-new-graph", df_state_daily['date'], df_state_daily['confirmed'],
                                    "Daily New Cases " + reverse_state_code_dict[state_dropdown_code],
                                    "Date", "New Cases")
        daily_active_graph = get_graph("state-daily-active-graph", df_state_daily['date'], df_state_daily['active'],
                                       "Daily Active Cases " + reverse_state_code_dict[state_dropdown_code], "Date",
                                       "Active Cases")
        df_state_levitt, dates, model, line, r_squared = get_data_for_graph_with_regression_line(df_state_daily,
                                                                                                 start_date)
        regression_graph = get_graph_with_regression_line("state-levitt-graph", df_state_levitt['date'],
                                                          df_state_levitt['LevittMeasure'],
                                                          list(df_state_levitt['date']) + dates, model(line), r_squared,
                                                          "Daily Levitt's Measure H(t) " + reverse_state_code_dict[
                                                              state_dropdown_code])
        return [regression_graph, daily_new_graph, daily_active_graph]


@app.callback(
    [Output('district-levitt', 'children'), Output('district-daily-new', 'children'),
     Output('district-daily-active', 'children')],
    [Input(component_id='district-dropdown', component_property='value'),
     Input(component_id='district-start-date', component_property='value')]
)
def update_graph(district_dropdown, district_start_date):
    """
    creates three graphs using Indian districts data: daily Levitt's measure graph with fitted regression line, daily
    new cases graph, daily active cases graph to be placed in a bootstrap row
    :param district_dropdown: selected district name from dropdown menu of Indian districts
    :param district_start_date: date from which data is to be considered
    :return: list of three dash core component graphs
    """
    if dt.datetime.strptime(district_start_date, "%Y-%m-%d") > pd.to_datetime("2020-03-01"):
        start_date = dt.datetime.strptime(district_start_date, "%Y-%m-%d")
        df_district_daily = get_district_df(district_dropdown)
        df_district_daily.rename({'Date': 'date'}, axis=1, inplace=True)
        df_district_daily.rename({'Confirmed': 'cum_confirmed'}, axis=1, inplace=True)
        daily_new_graph = get_graph("district-daily-new-graph", df_district_daily['date'], df_district_daily['New'],
                                    "Daily New Cases " + district_dropdown, "Date", "New Cases")
        daily_active_graph = get_graph("district-daily-active-graph", df_district_daily['date'],
                                       df_district_daily['Active'], "Daily Active Cases " + district_dropdown, "Date",
                                       "Active Cases")
        df_district_levitt, dates, model, line, r_squared = get_data_for_graph_with_regression_line(df_district_daily,
                                                                                                    start_date)
        regression_graph = get_graph_with_regression_line("district-levitt-graph", df_district_levitt['date'],
                                                          df_district_levitt['LevittMeasure'],
                                                          list(df_district_levitt['date']) + dates, model(line),
                                                          r_squared, "Daily Levitt's Measure H(t) " + district_dropdown)
        return [regression_graph, daily_new_graph, daily_active_graph]


if __name__ == "__main__":
    app.run_server(debug=False)
