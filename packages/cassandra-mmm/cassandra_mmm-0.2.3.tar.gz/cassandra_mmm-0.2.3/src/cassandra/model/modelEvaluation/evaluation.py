import pandas as pd
import numpy as np
from cassandra.data.trasformations.trasformations import saturation
from scipy.stats import dweibull
import matplotlib.pyplot as plt
import plotly.express as px

# def saturation_to_dataset(df, df_adstock_saturation):
#     df_saturation = df.copy()
#
#     for index, row in df.iterrows():
#         for m in list(df_adstock_saturation['canale']):
#             df_saturation.at[index, m] = saturation(df_saturation.at[index, m], df_adstock_saturation.loc[
#                 df_adstock_saturation['canale'] == m, 'saturation'].iloc[0])
#
#     return df_saturation


def response_regression_to_dataset(df, name_date_column, name_target_colum, name_prediction_column, coef_dict,
                                   features):
    columns = features
    coef_array = list(coef_dict.values())
    new_dict = {}

    for x in range(len(coef_array) - 1):
        new_dict[columns[x]] = df[columns[x]] * coef_array[x]

    new_dict['intercept'] = coef_array[-1]
    response_df = df[[name_date_column, name_target_colum, name_prediction_column]].join(pd.DataFrame(new_dict))
    return response_df


def decomposition_to_dataset(df, coef_dict, features, medias, name_date_column, name_target_colum,
                             name_prediction_column):
    columns = features
    coef_array = list(coef_dict.values())
    result = df[columns].copy()

    spend_df = spend_to_dataset(df, medias)

    result['intercept'] = coef_array[-1]

    coef_dict = {}

    for x in range(len(coef_array) - 1):
        coef_dict[columns[x]] = coef_array[x]

    coef_dict['intercept'] = coef_array[-1]

    df_all_decomp = response_regression_to_dataset(df, name_date_column, name_target_colum, name_prediction_column,
                                                   coef_dict, features)

    coef_df = pd.DataFrame(list(coef_dict.items()))
    coef_df.rename(columns={coef_df.columns[0]: 'canale', coef_df.columns[1]: 'coef'}, inplace=True)

    decomp_df = pd.DataFrame(df_all_decomp[result.keys()].sum(axis=0))
    decomp_df.reset_index(inplace=True)
    decomp_df.rename(columns={decomp_df.columns[0]: 'canale', decomp_df.columns[1]: 'xDecompAgg'},
                     inplace=True)

    response_decomp_df = pd.merge(left=decomp_df, right=coef_df, left_on='canale', right_on='canale')

    response_decomp_df['xDecompPerc'] = response_decomp_df['xDecompAgg'] / response_decomp_df['xDecompAgg'].sum()

    df_aggregated = pd.merge(how='left', left=response_decomp_df, right=spend_df, left_on='canale',
                             right_on='canale')

    xDecompPercSum = 0

    for index, row in df_aggregated.iterrows():
        if row['canale'] in medias:
            xDecompPercSum = xDecompPercSum + row['xDecompPerc']

    for index, row in df_aggregated.iterrows():
        if row['canale'] in medias:
            df_aggregated.at[index, 'effect_share'] = df_aggregated.at[index, 'xDecompPerc'] / xDecompPercSum
            df_aggregated.at[index, 'roi'] = df_aggregated.at[index, 'xDecompAgg'] / df_aggregated.at[
                index, 'spesa_totale']

    return df_aggregated, df_all_decomp


def adstock_saturation_to_dataset(nevergrad_dict, adstock_type, weibull_type='pdf', max_y=1, max_x=100, graph=True):
    if adstock_type == 'weibull':
        result_df = pd.DataFrame()
        adstock_columns = [col.replace('_shape', '') for col in nevergrad_dict.keys() if 'shape' in col]

        for m in adstock_columns:
            shape_name = m + '_shape'
            scale_name = m + '_scale'
            shape = nevergrad_dict[shape_name]
            scale = nevergrad_dict[scale_name]

            x_array = np.array([1])
            x = np.repeat(x_array, 100, axis=0)  # see to del
            range_x = [x / 100 for x in range(1, 101)]

            if weibull_type == 'pdf':
                y = dweibull.pdf(range_x, shape, scale=scale)
            else:
                y = dweibull.cdf(range_x, shape, scale=scale)

            data = plt.plot(range(1, 101), y)[0].get_data()

            df_media = pd.DataFrame(data).T

            df_media.rename(columns={df_media.columns[0]: 'x', df_media.columns[1]: 'y'},
                            inplace=True)

            for index, row in df_media.iterrows():
                df_media.at[index, 'y'] = ((df_media.at[index, 'y'] - df_media['y'].min()) / (
                        df_media['y'].max() - df_media['y'].min())) * (max_y - 0) + 0
                df_media.at[index, 'x'] = ((df_media.at[index, 'x'] - df_media['x'].min()) / (
                        df_media['x'].max() - df_media['x'].min())) * (max_x - 0) + 0
            if graph == True:
                title_graph = 'Adstock weibull ' + m
                fig2 = px.line(x=df_media['x'], y=df_media['y'], title=title_graph)
                fig2.show()

            df_media['canale'] = m
            result_df = pd.concat([result_df, df_media])

        shapes = [col for col in nevergrad_dict.keys() if 'shape' in col]
        adstocked_shapes = {key: nevergrad_dict[key] for key in shapes}
        scales = [col for col in nevergrad_dict.keys() if 'scale' in col]
        adstocked_scales = {key: nevergrad_dict[key] for key in scales}
        betas = [col for col in nevergrad_dict.keys() if 'beta' in col]
        saturationed = {key: nevergrad_dict[key] for key in betas}

        adstock_shapes_df = pd.DataFrame(list(adstocked_shapes.items()))
        adstock_shapes_df.rename(
            columns={adstock_shapes_df.columns[0]: 'canale', adstock_shapes_df.columns[1]: 'adstock_shape'},
            inplace=True)
        adstock_shapes_df['canale'] = adstock_shapes_df.canale.str.replace('_shape', '')

        adstock_scales_df = pd.DataFrame(list(adstocked_scales.items()))
        adstock_scales_df.rename(
            columns={adstock_scales_df.columns[0]: 'canale', adstock_scales_df.columns[1]: 'adstock_scale'},
            inplace=True)
        adstock_scales_df['canale'] = adstock_scales_df.canale.str.replace('_scale', '')

        adstock_df = pd.merge(left=adstock_shapes_df, right=adstock_scales_df, left_on='canale',
                              right_on='canale')

        saturation_df = pd.DataFrame(list(saturationed.items()))
        saturation_df.rename(columns={saturation_df.columns[0]: 'canale', saturation_df.columns[1]: 'saturation'},
                             inplace=True)
        saturation_df['canale'] = saturation_df.canale.str.replace('_beta', '')

        df_adstock_saturation = pd.merge(left=adstock_df, right=saturation_df, left_on='canale',
                                         right_on='canale')

    else:

        thetas = [col for col in nevergrad_dict.keys() if 'theta' in col]
        adstocked = {key: nevergrad_dict[key] for key in thetas}
        betas = [col for col in nevergrad_dict.keys() if 'beta' in col]
        saturationed = {key: nevergrad_dict[key] for key in betas}

        adstock_df = pd.DataFrame(list(adstocked.items()))
        adstock_df.rename(columns={adstock_df.columns[0]: 'canale', adstock_df.columns[1]: 'adstock'}, inplace=True)
        adstock_df['canale'] = adstock_df.canale.str.replace('_theta', '')

        saturation_df = pd.DataFrame(list(saturationed.items()))
        saturation_df.rename(columns={saturation_df.columns[0]: 'canale', saturation_df.columns[1]: 'saturation'},
                             inplace=True)
        saturation_df['canale'] = saturation_df.canale.str.replace('_beta', '')

        df_adstock_saturation = pd.merge(left=adstock_df, right=saturation_df, left_on='canale',
                                         right_on='canale')
    if adstock_type == 'weibull':
        return df_adstock_saturation, result_df
    else:
        return df_adstock_saturation


def spend_to_dataset(df, medias):
    total_spend_dict = {key: df[key].sum() for key in medias}
    total_spend_df = pd.DataFrame(list(total_spend_dict.items()))
    total_spend_df['spesa_totale'] = sum(total_spend_dict.values())
    total_spend_df.rename(columns={total_spend_df.columns[0]: 'canale', total_spend_df.columns[1]: 'spesa'},
                          inplace=True)
    total_spend_df['spend_share'] = (total_spend_df['spesa'] * 100) / total_spend_df['spesa_totale']

    return total_spend_df

def saturation_to_dataset(df, df_adstock_saturation, coeffs, features):
    df_saturation = df.copy()

    for index, row in df_saturation.iterrows():
        for m in list(df_adstock_saturation['canale']):
            df_saturation.at[index, m] = saturation(df_saturation.at[index, m], df_adstock_saturation.loc[
                df_adstock_saturation['canale'] == m, 'saturation'].iloc[0])

    coef_array = coeffs.copy()
    new_dict = {}

    for x in range(len(coef_array) - 1):
        new_dict[features[x]] = df_saturation[features[x]] * coef_array[x]

    df_saturation_response = pd.DataFrame(new_dict)
    return df_saturation_response

# def decomposition_to_dataset(df, coef_dict, features, spend_df, medias, name_date_column, name_target_colum,
#                              name_prediction_column):
#     columns = features
#     coef_array = list(coef_dict.values())
#     result = df[columns].copy()
#
#     result['intercept'] = coef_array[-1]
#
#     coef_dict = {}
#
#     for x in range(len(coef_array) - 1):
#         coef_dict[columns[x]] = coef_array[x]
#
#     coef_dict['intercept'] = coef_array[-1]
#
#     df_all_decomp = response_regression_to_dataset(df, name_date_column, name_target_colum, name_prediction_column,
#                                                    coef_dict, features)
#
#     coef_df = pd.DataFrame(list(coef_dict.items()))
#     coef_df.rename(columns={coef_df.columns[0]: 'canale', coef_df.columns[1]: 'coef'}, inplace=True)
#
#     decomp_df = pd.DataFrame(df_all_decomp[result.keys()].sum(axis=0))
#     decomp_df.reset_index(inplace=True)
#     decomp_df.rename(columns={decomp_df.columns[0]: 'canale', decomp_df.columns[1]: 'xDecompAgg'},
#                      inplace=True)
#
#     response_decomp_df = pd.merge(left=decomp_df, right=coef_df, left_on='canale', right_on='canale')
#
#     response_decomp_df['xDecompPerc'] = response_decomp_df['xDecompAgg'] / response_decomp_df['xDecompAgg'].sum()
#
#     df_aggregated = pd.merge(how='left', left=response_decomp_df, right=spend_df, left_on='canale',
#                              right_on='canale')
#
#     xDecompPercSum = 0
#
#     for index, row in df_aggregated.iterrows():
#         if row['canale'] in medias:
#             xDecompPercSum = xDecompPercSum + row['xDecompPerc']
#
#     for index, row in df_aggregated.iterrows():
#         if row['canale'] in medias:
#             df_aggregated.at[index, 'effect_share'] = df_aggregated.at[index, 'xDecompPerc'] / xDecompPercSum
#             df_aggregated.at[index, 'roi'] = df_aggregated.at[index, 'xDecompAgg'] / df_aggregated.at[
#                 index, 'spesa_totale']
#
#     return df_aggregated, df_all_decomp
