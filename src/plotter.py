import matplotlib.pyplot as plt
import geodatasets
import geopandas as gpd
import contextily as cx
import seaborn as sns

def bar_plot(series, figsize=(10, 10), title="", xlabel="", ylabel="", annotate=False):
    ax = series.plot.bar(
        figsize=figsize,
        edgecolor="black"
    )

    plt.title(title, fontsize=16, fontweight="bold")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(axis="y", linestyle="--", alpha=0.6)

    if annotate:
        for p in ax.patches:
            ax.annotate(
                str(p.get_height()), 
                (p.get_x() + p.get_width() / 2.0, p.get_height()), 
                ha="center",
                va="bottom",
                fontsize=12
            )

    plt.show()

def pie_plot(series, figsize=(10, 6), title=""):
    total = series.sum()
    labels = [f'{label} ({val/total:.1%})' for label, val in series.items()]
    ax = series.plot.pie(figsize=figsize, labels=labels)

    plt.title(title, fontsize=16, pad=20, fontweight="bold")

    plt.show()

def stacked_bar_plot(series, figsize=(10, 6), title="", legend=True):
    ax = series.plot.bar(
        figsize=figsize,
        stacked=True,
        legend=legend
    )

    plt.title(title, fontsize=16, pad=20, fontweight="bold")

    plt.show()


def scatter_plot(df, x, y, figsize=(10, 10), annotate=False):
  ax = df.plot.scatter(
    figsize=figsize, 
    x=x, 
    y=y
  )

  if annotate: 
    for k, v in df.iterrows():
      ax.annotate(
        k,
        (v[x], v[y]),
        xytext=(5, 5),               
        textcoords='offset points',
        fontsize=9
      )

  plt.show()

def plot_heatmap(qdf, figsize=(10, 10), annotate=False, title="", xlabel="", ylabel=""):
  plt.figure(figsize=figsize)
  sns.heatmap(qdf, annot=True, fmt='d', cmap='viridis')
  plt.title(title)
  plt.ylabel(ylabel)
  plt.xlabel(xlabel)

plt.show()
def _setup_ax_for_map(figsize=(12, 8)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_axis_off()
    return ax    

def add_background_map(ax):        
    world_path = geodatasets.get_path('naturalearth.land')
    world = gpd.read_file(world_path)
    world.plot(ax=ax, color='#f0f0f0', edgecolor='#d4d4d4', linewidth=0.5, zorder=0)

def plot_points_on_map(gdf, identifier):
    ax = _setup_ax_for_map()

    gdf.plot(
        ax=ax,
        column=identifier,
        cmap="tab20",
        legend="True",
        markersize=20,
        alpha=0.8
    )

    add_background_map(ax)
    return ax
