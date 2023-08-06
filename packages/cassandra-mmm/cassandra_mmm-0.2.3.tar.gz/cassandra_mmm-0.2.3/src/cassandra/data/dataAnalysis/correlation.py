from IPython.display import Markdown, display
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


def show_trendline_curves(medias_column, df, name_target_column):
    saturation_df = df

    for media in medias_column:
        # For each media remove all the 0 spend values as Log(0) can't be calculated
        saturation_df[media] = saturation_df[media][saturation_df[media] != 0]
        # saturation_df = saturation_df[(saturation_df[[media]] != 0).all(axis=1)]

        # Create a Scatter Plot
        fig = px.scatter(
            # Our temporary DF with no 0 values
            saturation_df,
            # Media channel's name
            x=media,
            # Our output variable (Sales or Conversion)
            y=name_target_column,
            # Specify the type of trendline you want to show, use OLS if not sure
            trendline="ols",
            # Define the trendline as logarithmic, this will return curved functions
            trendline_options=dict(log_x=True)
        )
        # Print Figure
        fig.show()


def show_relationship_between_variables(df, plot_for_line=5, show_only_one=''):
    # Iterative pair-plotting
    # Just set the @plot_for_line and eventually change DF name and it will do the rest

    # df already in scope as the pandas dataframe with data
    hue = 'label'

    # How many plots per row you want to display
    all_vars = list(df.columns.symmetric_difference([]))

    if show_only_one:
        display(Markdown(f"## {show_only_one}"))

        for var in all_vars:
            display(Markdown(f"### {var} vs {show_only_one}"))
            sns.pairplot(df, x_vars=[var], y_vars=show_only_one, palette='bright')
            plt.show()
            plt.close()

    else:
        for var in all_vars:
            rest_vars = list(all_vars)
            rest_vars.remove(var)
            display(Markdown(f"## {var}"))

            while rest_vars:
                line_vars = rest_vars[:plot_for_line]
                del rest_vars[:plot_for_line]
                line_var_names = ", ".join(line_vars)
                display(Markdown(f"### {var} vs {line_var_names}"))
                sns.pairplot(df, x_vars=line_vars, y_vars=[var], palette='bright', )
                plt.show()
                plt.close()
