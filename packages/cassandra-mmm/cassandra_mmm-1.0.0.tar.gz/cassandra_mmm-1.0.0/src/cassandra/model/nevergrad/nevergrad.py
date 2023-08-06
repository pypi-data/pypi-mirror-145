# TODO
import nevergrad as ng
from cassandra.model.nevergrad.utils import instrum_trasformations_nevergrad, create_df_trasformations_nevergrad, choose_optimizer_algoritm, optimize_metric
from cassandra.model.utils import choose_model


def nevergrad_model(df, hyperparameters_dict, medias, organic, target, use_intercept=True, use_adstock=True, use_saturation=True,
                                adstock_type='weibull', model_regression='linear', X_trasformations_columns=[],
                     model_regression_log_log='linear', ridge_number=0, metric=['rsq', 'nrmse', 'mape'],
                     return_metric=True, size=0.2, positive=False, random_state=42, metric_return='mape',
              force_coeffs=False, coeffs=[], intercept=0, optimizer_algoritm='TwoPointsDE', budget=1000):

    value_trasf = instrum_trasformations_nevergrad(hyperparameters_dict)
    instrum = ng.p.Instrumentation(**value_trasf)
    optimizer = choose_optimizer_algoritm(optimizer_algoritm, budget, instrum)

    metric_array = []
    df_transformations = df.copy()
    metrics_values = {}
    all_hyper = list(hyperparameters_dict.keys())

    def build_model(**all_hyper):
        df_transf = create_df_trasformations_nevergrad(all_hyper, df, df_transformations, medias, use_adstock, use_saturation, adstock_type)
        if return_metric:
            result, model, metrics_values = choose_model(df_transf, medias + organic, target, model_regression, X_trasformations_columns,
                     model_regression_log_log, ridge_number, metric,
                     return_metric, size, positive, random_state, force_coeffs, coeffs, intercept)
        else:
            result, model = choose_model(df_transf, medias + organic, target, model_regression, X_trasformations_columns,
                     model_regression_log_log, ridge_number, metric,
                     return_metric, size, positive, random_state, force_coeffs, coeffs, intercept)

        metric_to_optimize = optimize_metric(metric_return, metrics_values)
        metric_array.append(metric_to_optimize)

        return metric_to_optimize

    recommendation = optimizer.minimize(build_model)

    def build_model_result(**all_hyper):

        df_transf = create_df_trasformations_nevergrad(all_hyper, df, df_transformations, medias, use_adstock, use_saturation, adstock_type)

        if return_metric:
            result, model, metrics_values = choose_model(df_transf, medias + organic, target, model_regression, X_trasformations_columns,
                     model_regression_log_log, ridge_number, metric,
                     return_metric, size, positive, random_state, force_coeffs, coeffs, intercept)
        else:
            result, model = choose_model(df_transf, medias + organic, target, model_regression, X_trasformations_columns,
                     model_regression_log_log, ridge_number, metric,
                     return_metric, size, positive, random_state, force_coeffs, coeffs, intercept)

        metric_to_optimize = optimize_metric(metric_return, metrics_values)
        metric_array.append(metric_to_optimize)

        return metric_to_optimize, result, model

    metric, result, model = build_model_result(**recommendation.value[1])
    return metric, result, model, metric_array




