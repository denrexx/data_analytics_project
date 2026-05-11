import pandas as pd

def read_data_chunks(path, chunk_size=50):
    for chunk in pd.read_csv(path, chunksize=chunk_size):
        yield chunk

def load_data(path, show_info=True):
    df = pd.read_csv(path)
    if show_info:
        print(df.head())
        print(df.info())
        print(df.describe())
    return df
