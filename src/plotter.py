import matplotlib as mpl

def plot_average(df):
    df.plot(kind="bar", y="Number")
    mpl.pyplot.show()    
