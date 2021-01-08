from nptdms import TdmsFile, TdmsWriter, ChannelObject, RootObject
import numpy as np
import pandas as pd

def read_tdms_to_nparray(name):
    file = TdmsFile.read(name)
    data = []
    for group in file.groups():
        df_group = group.as_dataframe()
        data.append(df_group)
    df = pd.DataFrame(data[1])
    frames = [np.array(df.iloc[i]).reshape((256, 128)) for i in range(len(df))]
    return frames
