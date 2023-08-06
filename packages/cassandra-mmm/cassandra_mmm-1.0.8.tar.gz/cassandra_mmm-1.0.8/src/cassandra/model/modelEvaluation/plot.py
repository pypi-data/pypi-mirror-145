import pandas as pd
import numpy as np
import plotly.express as px
from cassandra.model.modelEvaluation.evaluation import saturation_to_dataset
from sklearn import metrics
import plotly.graph_objects as go


def show_nrmse(y_train, y_trainPred, verbose=False):
    value = np.sqrt(np.mean((y_train - y_trainPred) ** 2)) / (max(y_train) - min(y_train))
    passed = "✔️" if value < 0.15 else "❌"
    if verbose:
        return value, passed
    else:
        return value


def show_mape(y_test, y_testPred, verbose=False):
    # mean absolute percentage error
    x = np.abs((y_test - y_testPred) / y_test)
    value = np.mean(x[~np.isinf(x)])
    passed = "✔️" if value < 0.15 else "❌"
    if verbose:
        return value, passed
    else:
        return value


def show_rsquared(y_actual, y_pred, verbose=False):
    # r squared
    value = round(metrics.r2_score(y_actual, y_pred), 3)
    passed = "✔️" if value > 0.8 else "❌"
    if verbose:
        return value, passed
    else:
        return value


def show_nrmse_old(y_actual, y_pred, verbose=False):
    # normalized root mean square error
    value = round(np.sqrt(metrics.mean_squared_error(y_actual, y_pred)) / np.mean(y_actual), 3)
    passed = "✔️" if value < 0.15 else "❌"
    if verbose:
        return value, passed
    else:
        return value


def show_mape_old(y_actual, y_pred, verbose=False):
    # mean absolute percentage error
    value = round(metrics.mean_absolute_error(y_actual, y_pred) / np.mean(y_actual), 3)
    passed = "✔️" if value < 0.15 else "❌"
    if verbose:
        return value, passed
    else:
        return value


def show_coefficients(features, model, name_model, graph=True):
    # Given model = LinearRegression() model already executed

    # Create an array of the variables you want to check coeffs
    # features = ['g_display_cost', 'g_shopping_cost', 'g_video_cost', 'g_search_brand_cost', 'g_search_no_brand_cost',
    #             'fb_cost', 'pinterest_cost', 'b_audience_cost', 'b_search_cost', 'avg_price',
    #             'solostove_organic_traffic', 'solostove_paid_traffic', 'trend_smokeless_fire_pit']

    coeffs = model.coef_.copy()
    new_features = features.copy()

    if model.intercept_:
        coeffs = np.append(coeffs, model.intercept_)
        new_features = np.append(new_features, 'intercept')

    roas = pd.DataFrame(data=coeffs, index=new_features, columns=['contribution'])
    title_graph = name_model + " Model Coefficients graph"
    if graph == True:

        fig = go.Figure(
            data=[go.Bar(x=roas.index, y=roas['contribution'])],
            layout=go.Layout(
                title=go.layout.Title(text=title_graph)
            )
        )

        fig.show()
        return coeffs
    else:
        return coeffs


def show_saturation_curves(df, df_adstock_saturation, coeffs, features, medias):
    df_saturation = saturation_to_dataset(df, df_adstock_saturation, coeffs, features)

    for m in medias:
        s_df = pd.merge(df[m], df_saturation[m], left_index=True, right_index=True)

        # For each media remove all the 0 spend values as Log(0) can't be calculated
        s_df[m + '_x'] = s_df[m + '_x'][s_df[m + '_x'] != 0]
        s_df[m + '_y'] = s_df[m + '_y'][s_df[m + '_y'] != 0]

        # Create a Scatter Plot
        fig = px.line(
            # Spends Media channel's name
            x=s_df[m + '_x'].sort_values(),
            # Response Media channel's name
            y=s_df[m + '_y'].sort_values()
            # Specify the type of trendline you want to show, use OLS if not sure
        )
        # Print Figure
        fig.show()

    return df_saturation


def show_effect_share_vs_spend_share(df_aggregated, show_cpo=True):
    df_spend_var = df_aggregated.copy().dropna()
    fig = go.Figure()

    fig.add_bar(x=df_spend_var['canale'], y=df_spend_var['spend_share'], name='spend_share',
                marker=dict(color="Purple"))
    fig.add_bar(x=df_spend_var['canale'], y=df_spend_var['effect_share'], name='effect_share',
                marker=dict(color="MediumPurple"))

    if show_cpo:
        fig.add_scatter(x=df_spend_var['canale'], y=(1 / (round(df_spend_var['roi'], 2))), mode="markers", name='cpo',
                        marker=dict(size=20, color="LightSeaGreen"))
    else:
        fig.add_scatter(x=df_spend_var['canale'], y=round(df_spend_var['roi'], 2), mode="markers", name='roi',
                        marker=dict(size=20, color="LightSeaGreen"))

    fig.show()
