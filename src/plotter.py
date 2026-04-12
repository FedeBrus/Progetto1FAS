import matplotlib.pyplot as plt

def count_plot(count_series):
    count_series.plot.bar()
    plt.tight_layout()
    plt.show()

def plot_on_map(map):
    map.plot()
    plt.tight_layout()
    plt.show()
