import pandas as pd

def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError as e:
        raise e
