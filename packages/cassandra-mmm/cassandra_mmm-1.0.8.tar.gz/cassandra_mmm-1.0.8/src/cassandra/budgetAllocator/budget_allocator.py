import pandas as pd
import numpy as np
from cassandra.data.trasformations.trasformations import saturation
from cassandra.budgetAllocator.utils import get_opt_algoritm


def budget_allocator_c(df, name_date_column, medias, all_features, date_get_budget, model, spends, response_get_budget,
                       lower_bounds, upper_bounds, maxeval, df_aggregated, algoritm='LD_MMA', number_tail=15):

    def getVals(df, name_date_column, all_features, date_get_budget='', number_tail=number_tail):
        if date_get_budget:
            get_vals_df = df.copy()
            get_vals_df.drop(get_vals_df[get_vals_df[name_date_column] > date_get_budget].index)
            full_row = pd.DataFrame(get_vals_df.tail(number_tail).mean()).T
        else:
            full_row = df.tail(number_tail).mean()

        row = full_row[all_features].copy()

        return row

    def myFunc(x, grad=[]):

        data = {}

        for m in medias:
            data[m] = [saturation(x[medias.index(m)], df_aggregated.loc[
                df_aggregated['canale'] == m, 'saturation'].iloc[0])]

        dic = pd.DataFrame.from_dict(data)

        new_df = getVals(df, name_date_column, all_features, date_get_budget, number_tail).copy()

        for column in dic:
            new_df[column] = dic[column].iloc[0]

        return model.predict(new_df)[0]

    opt = get_opt_algoritm(algoritm, medias, lower_bounds, upper_bounds, spends, maxeval, myFunc)

    budget_spends = opt.optimize(spends)

    budget_allocator_df = pd.DataFrame()
    budget_allocator_df['canale'] = medias
    for index, row in budget_allocator_df.iterrows():
        budget_allocator_df.at[index, 'actual_spend'] = spends[index]
        budget_allocator_df.at[index, 'optimal_spend'] = budget_spends[index]
        budget_allocator_df.at[index, 'actual_response'] = df_aggregated.loc[index, 'xDecompAgg']
        budget_allocator_df.at[index, 'optimal_response'] = budget_spends[index] * df_aggregated.loc[index, 'coef']
        budget_allocator_df.at[index, 'actual_total_spend'] = np.sum(spends)
        budget_allocator_df.at[index, 'optimal_total_spend'] = np.sum(budget_spends)
        budget_allocator_df.at[index, 'actual_total_response'] = response_get_budget
        budget_allocator_df.at[index, 'optimal_total_response'] = opt.last_optimum_value()

    return budget_allocator_df

    # def getVals(df, name_date_column, all_features, date_get_budget):

    # full_row = df.loc[df[name_date_column] == date_get_budget]
    # print(full_row)
    # row = full_row[all_features].copy()
    # print(row)

    # return row
