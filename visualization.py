import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def proportion_plot(data, field_name):

    """
    data -> Pandas Dataframe
    field_name -> Column to be plotted.
    """
    n_data = data.shape[0]
    counts = data[field_name].value_counts()
    order = counts.index

    try:
        max_count = counts[0]
        max_prop = max_count / n_data
    except KeyError as e:
        print("An error occured : {e}".format(e))
        return

    tick_props = np.arange(0, max_prop, 0.2)
    tick_names = ["{:0.2f}".format(v) for v in tick_props]
    sns.countplot(data=data, y=field_name, order=order)
    plt.xticks(tick_props * n_data, tick_names)
    plt.xlabel("Proportion")

    for i in range(counts.shape[0]):
        count = counts[i]
        pct_string = "{:0.1f}%".format(100 * count / n_data)
        plt.text(counts + 1, i, pct_string, va="center")

    return

