import pandas as pd


def preprocess( Model_inst ):

    """Perform preprocessing on the dataset which has been preprocessed according to the Input_File modules"""

    df = Model_inst.df_pre.copy()
    ###

    #   insert preprocessing instructions

    ###
    Model_inst.df_pre = df
