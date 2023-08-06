# TODO
from cassandra.data.trasformations.trasformations import adstock_weibull, saturation, adstock
import nevergrad as ng
import numpy as np


def create_df_trasformations_nevergrad(trasf, df, df_transformations, medias, use_adstock = True, use_saturation = True, adstock_type = 'weibull'):

    #key_trasf = list(hyperparameters_dict.keys())
    #trasf = dict(zip(key_trasf, value_trasf))

    if use_saturation:
        if use_adstock:
            if adstock_type == 'weibull':
                for m in medias:
                    df_transformations[m] = saturation(adstock_weibull(df[m], trasf[m + '_scale'], trasf[m + '_shape']).replace([np.inf, -np.inf], 0), trasf[m + '_beta'])

            else:
                for m in medias:
                    df_transformations[m] = saturation(adstock(df[m], trasf[m + '_theta']), trasf[m + '_beta'])
        else:
            for m in medias:
                df_transformations[m] = saturation(df[m], trasf[m + '_beta'])

    else:
        if use_adstock:
            if adstock_type == 'weibull':
                for m in medias:
                    df_transformations[m] = saturation(
                        adstock_weibull(df[m], trasf[m + '_scale'], trasf[m + '_shape']).replace([np.inf, -np.inf],
                                                                                                 0),
                        trasf[m + '_beta'])

            else:
                for m in medias:
                    df_transformations[m] = saturation(adstock(df[m], trasf[m + '_theta']), trasf[m + '_beta'])

    return df_transformations


def instrum_variables_nevergrad(medias, organic, force_coeffs=False, use_intercept=True, use_adstock=True, use_saturation=True,
                                adstock_type='weibull'):
    result_dict = {}

    if force_coeffs:
        for x in medias:
            result_dict[x] = {'lower': 0, 'upper': None}
        for x in organic:
            result_dict[x] = {'lower': None, 'upper': None}
        if use_intercept:
            result_dict['intercept'] = {'lower': None, 'upper': None}

    if use_adstock:
        if adstock_type == 'weibull':
            for x in medias:
                result_dict[x + '_shape'] = {'lower': 0, 'upper': 2}
                result_dict[x + '_scale'] = {'lower': 0, 'upper': 0.1}

                if use_saturation:
                    result_dict[x + '_beta'] = {'lower': 0, 'upper': 1}
        else:
            for x in medias:
                result_dict[x + '_theta'] = {'lower': 0, 'upper': 0.3}

                if use_saturation:
                    result_dict[x + '_beta'] = {'lower': 0, 'upper': 1}

    return result_dict


def instrum_trasformations_nevergrad(hyperparameters_dict):
    result = {}
    for key, value in hyperparameters_dict.items():
        result[key] = ng.p.Scalar(lower=hyperparameters_dict[key]['lower'], upper=hyperparameters_dict[key]['upper'])

    return result

def choose_optimizer_algoritm(optimizer_algoritm, budget, instrum):
    if optimizer_algoritm == 'TwoPointsDE':
        optimizer = ng.optimizers.TwoPointsDE(parametrization=instrum, budget=budget)
    if optimizer_algoritm == 'NGOpt':
        optimizer = ng.optimizers.NGOpt(parametrization=instrum, budget=budget)

    return optimizer

def optimize_metric(return_metric, metrics_values):
    result = ''
    for key, value in metrics_values.items():
        if return_metric in key:
            result = value

    return result



