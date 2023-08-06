"""This contains all functions for plotting to avoid code duplication and 
improve code readability.
"""

import matplotlib.pyplot as plt
import seaborn as sns

def heatmap(table, title):
    table = table.reset_index()
    grid = table.pivot(*table.columns)
    ax = sns.heatmap(
        grid, annot=True, annot_kws={'fontsize': 'small'},
        cmap='Oranges', linewidths=.5)
    ax.set_title(title)
    return ax

def plot_alarms(
        measurements,
        high_thresholds=None,
        low_thresholds=None,
        high_alarms=None,
        low_alarms=None,
        patient_name='',
        parameter_name=''
    ):
    fig, ax = plt.subplots()

    ax.plot(measurements.index, measurements, c='green')

    if high_thresholds is not None:
        ax.step(measurements.index, high_thresholds, c='red')
    if low_thresholds is not None:
        ax.step(measurements.index, low_thresholds, c='blue')

    if high_alarms is not None:
        ax.scatter(high_alarms.index, high_alarms, c='red')
    if low_alarms is not None:
        ax.scatter(low_alarms.index, low_alarms, c='blue')

    ax.set_title(patient_name)
    ax.set_xlabel("Time (with dummy date)")
    ax.set_ylabel(parameter_name)

    ax.tick_params(axis='x', labelrotation=45)

    return ax