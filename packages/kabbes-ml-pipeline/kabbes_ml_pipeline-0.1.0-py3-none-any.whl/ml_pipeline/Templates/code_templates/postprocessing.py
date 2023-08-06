import pandas as pd


def postprocess( Model_inst ):

    """Perform postprocessing on the Results Dataframe and turn it into the Postprocessed DataFrame (df_post) """

    df = Model_inst.df_results_pre.copy()
    ###

    #   insert preprocessing instructions

    ###
    Model_inst.df_post = df
