import pandas as pd
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import numpy as np

def preprocess( Model ):

    # setup the Model features and target
    Model.df_features = Model.df_pre.drop( [ Model.target_ncol ], axis = 1 )
    Model.df_target = Model.df_pre[ Model.target_ncol ]

def split_features_and_target( Model ):

    # setup the Model features and target
    Model.df_features = Model.df_pre.drop( [ Model.target_ncol ], axis = 1 )
    Model.df_target = Model.df_pre[ Model.target_ncol ]

def postprocess( Model ):

    Model.df_results_pre = Model.df_results_propensity.join( Model.df_pre, how = 'left' )

def model_prep( Model ):

    """Model preparation"""

    split_features_and_target( Model )

    print ('Initializing Varibles')
    df = Model.df_pre
    df_features = Model.df_features
    df_target = Model.df_target

    # Split training and test data sheets
    print('Splitting Dataset')
    Model.df_train, Model.df_test, Model.df_train_target, Model.df_test_target = train_test_split( df_features, df_target, test_size = .25, random_state = 12 )

def fit_model( Model ) -> None:

    """Fits the model"""

    ###
    #  THIS IS WHERE YOU PUT YOUR MACHINE LEARNING ALGORITHM CODE
    ###

    Model.model = None

def run_model( Model ) -> None:

    """Saves the "model" attribute and "df_results_propensity" """

    ###
    #  Predict Results
    ###

    results_array = np.zeros( ( len(Model.df_features) ,2 ) )
    results_array[ :,1 ] = np.random.random( len(Model.df_features) )
    results_array[ :,0 ] = 1 - results_array[ :,1 ]

    # Export the results
    results = results_array[ :,1 ] #this is the probability of positive class
    Model.df_results_propensity = pd.DataFrame( { Model.propensity_col: results }, index = Model.df_features.index )
