import matplotlib.pyplot as plt
import geopandas as gpd
import geodatasets
import contextily as cx
import seaborn as sns

def count_plot(count_series):
    count_series.plot.bar()
    plt.tight_layout()
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

def plot_points_on_map(gdf, identifier, chunks=None):
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

def plot_density_on_map(gdf):
    ax = _setup_ax_for_map()

    sns.kdeplot(
        x=gdf.geometry.x, 
        y=gdf.geometry.y,
        ax=ax,
        fill=True, 
        alpha=0.6,
        zorder=1,
    )
    
    gdf.plot(
        ax=ax,
        color='black',
        markersize=5,
        alpha=0.8,
        zorder=2
    )
    
    add_background_map(ax)
    return ax
