from datetime import datetime, timedelta


def getBudget(df, name_date_column, name_target_column, medias, date_get_budget='', number_tail=15):
    if date_get_budget:
        new_df = df.copy()
        new_df.drop(new_df[new_df[name_date_column] > date_get_budget].index, inplace=True)
        full_row = new_df.tail(number_tail).mean()
    else:
        full_row = df.tail(number_tail).mean()

    spends = []

    for m in medias:
        spends.append(full_row[m])

    response = full_row[name_target_column]
    return spends, response


def getVals(df, name_date_column, all_features, date_get_budget='', number_tail=15):
    if date_get_budget:
        new_df = df.copy()
        new_df.drop(new_df[new_df[name_date_column] > date_get_budget].index, inplace=True)
        full_row = new_df.tail(number_tail).mean()
    else:
        full_row = df.tail(number_tail).mean()

    row = full_row[all_features].copy()

    return row
