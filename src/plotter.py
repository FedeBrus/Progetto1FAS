import matplotlib.pyplot as plt
import geodatasets
import geopandas as gpd
import contextily as cx
import seaborn as sns

def bar_plot(series, figsize=(10, 6), title="", xlabel="", ylabel="", annotate=False):
    ax = series.plot.bar(
        figsize=figsize,
        edgecolor="black"
    )

    plt.title(title, fontsize=16, pad=20, fontweight="bold")
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.6)

    if annotate:
        for p in ax.patches:
            ax.annotate(
                str(p.get_height()), 
                (p.get_x() + p.get_width() / 2., p.get_height() / 2), 
                ha="center", 
                va="center",
                fontsize=10,
                fontweight="bold"
            )

    plt.show()

def pie_plot(series, figsize=(10, 6), title=""):
    ax = series.plot.pie(
        figsize=figsize
    )

    plt.title(title, fontsize=16, pad=20, fontweight="bold")

    plt.show()

def _setup_ax_for_map(ax=None, figsize=(12, 8)):
    if ax is None:
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

def plot_density_on_map(gdf, identifier):
    ax = _setup_ax_for_map()

    sns.kdeplot(
        data=gdf,
        x=gdf.geometry.x, 
        y=gdf.geometry.y,
        ax=ax,
        thresh=0.05,
        levels=15,
        common_norm=False,
        hue=identifier,
        fill=True, 
        alpha=0.6,
        zorder=1,
    )
    
    gdf.plot(
        ax=ax,
        color="black",
        markersize=5,
        zorder=2
    )
    
    add_background_map(ax)
    return ax
