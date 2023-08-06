import pandas as pd


def clean( Model_inst ):

    """Take the joined df (df_joined) and clean it, export as df_cleaned"""

    df = Model_inst.df_joined.copy()
    ###

    # Insert cleaning instructions

    ###
    Model_inst.df_cleaned = df
