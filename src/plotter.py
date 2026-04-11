import matplotlib.pyplot as plt

def count_plot(count_series):
    count_series.plot.barh()
    plt.tight_layout()
    plt.show()
