import ml_pipeline
import ml_pipeline.ML_params as mlp

import py_starter.py_starter as ps
import dir_ops.dir_ops as do
import analytics_packages.custom_xlwings as cxw

import pandas as pd
import datetime
import numpy as np

def join_nickname_and_col( nickname, col ):

    '''Given "EXP", "HOME_AGE", return "EXP-HOME_AGE" '''
    return nickname + mlp.NICKNAME_SEP + col

def split_ncol( string ):

    '''Given EXP-HOME_AGE, return ("EXP", "HOME_AGE") '''
    values = string.split( mlp.NICKNAME_SEP )

    nickname = values[0]
    if len(values) > 1:
        col = mlp.NICKNAME_SEP.join( values[1:] )
    else:
        col = None

    return nickname, col

def get_df_from_dict( dictionary: dict, key_col: str = 'Key', val_col: str = 'Value' ) -> pd.DataFrame:

    '''Given a dictionary, turn it into a pandas DF with KEY and VALUE columns'''

    keys = []
    vals = []

    for key in dictionary:
        keys.append( key )
        vals.append( dictionary[key] )

    return pd.DataFrame( {key_col: keys, val_col: vals} )

def get_dict_from_df( df, key_col: str = 'Key', val_col: str = 'Value' ) -> dict:

    '''for a dataframe with keys and values, return a dictionary'''
    dict_mapping = {}

    for i in range(len(df)):
        dict_mapping[ df.loc[i, key_col] ] = df.loc[i, val_col]

    return dict_mapping

def generate_sample_df( df, length = 100 ):

    if len(df) > length:
        return df.sample( length )
    return df

def gen_from_template( copy_Path, paste_Path, overwrite = False ):

    if paste_Path.exists():
        if overwrite:
            paste_Path.remove( override = True )
        else:
            return

    copy_Path.copy( paste_Path, print_off = False )

def create_unique_Path( location_Dir, file_root, file_ending ):

    dt_string = datetime.datetime.now().strftime( '%Y-%m-%d' )
    existing_Paths = location_Dir.list_contents_Paths( block_dirs = True, block_paths = False )
    existing_paths = [ P.path for P in existing_Paths ]

    padding = ''
    counter = 1

    while True:

        filename = dt_string + padding + ' ' + file_root + '.' + file_ending
        full_path = location_Dir.join( filename )

        if full_path in existing_paths:
            counter += 1
            padding = '_' + str(counter)

        else:
            return do.Path( full_path )

### Exporting
def import_df( self, attribute_name_df = None, import_Path = None, **kwargs ):

    if import_Path.ending == 'parquet':
        kwargs = ps.replace_default_kwargs( {'engine': self.Models.parquet_engine}, **kwargs )

    df_import = import_df_from_Path( import_Path, **kwargs )

    if attribute_name_df == None:
        return df_import

    self.set_attr( attribute_name_df, df_import )

def export_df( self, attribute_name_df = None, export_Path = None, df = pd.DataFrame(), **kwargs ):

    if export_Path.ending == 'parquet':
        kwargs = ps.replace_default_kwargs( {'engine': self.Models.parquet_engine}, **kwargs )

    if attribute_name_df != None:
        df = self.get_attr( attribute_name_df )

    export_df_to_Path( df, export_Path, **kwargs )

def import_df_from_Path( Path_df, print_off = True, **kwargs ):

    '''import a file from given path into a pandas dataframe '''

    if print_off:
        print ('Importing DataFrame from ' + Path_df.p)

    if Path_df.ending == 'parquet':
        return pd.read_parquet( Path_df.p, **kwargs )

    elif Path_df.ending == 'csv':
        if 'error_bad_lines' not in kwargs:
            kwargs['error_bad_lines'] = False
        return pd.read_csv( Path_df.p, **kwargs )

    elif Path_df.ending == 'xlsx' or Path_df.ending == 'xlsm':
        wb = cxw.get_wb( Path_df.p )
        ws = cxw.get_ws( wb, **kwargs )
        return cxw.get_df_from_ws( ws )

    else:
        print ('No instructions on how to import file with ending ' + Path_df.ending)
        return None

def export_df_to_Path( df, Path_df, print_off = True, **kwargs ):

    '''given a df and a path, export the dataframe'''

    if print_off:
        print ('Exporting DataFrame to ' + Path_df.p)

    if Path_df.ending == 'parquet':
        df.to_parquet( Path_df.p, **kwargs )

    elif Path_df.ending == 'csv':
        if 'index' not in kwargs:
            kwargs['index'] = False
        df.to_csv( Path_df.p, **kwargs )

    elif Path_df.ending == 'xlsx' or Path_df.ending == 'xlsm':
        wb = cxw.get_wb( Path_df.p )
        ws = cxw.get_ws( wb, **kwargs )
        cxw.write_df_to_ws( ws, df )

    else:
        print ('No instructions on how to export file with ending ' + Path_df.ending)

def shap_importance( Model ):

    import shap
    import matplotlib.pyplot as plt
    shap.initjs()

    shap_Dir = Model.data_Dirs['shap']

    ###
    # FEATURE IMPORTANCE - Get important features and plot using shap
    ###
    explainer = shap.TreeExplainer( Model.model )
    shap_values = explainer.shap_values( Model.df_features )
    Model.shap_values = shap_values

    shap.summary_plot(shap_values, Model.df_features, plot_type="bar", show = False )
    plt.gcf().set_size_inches( 12.0, 12.0)

    file_root = ' '.join( [ Model.algorithm_code, 'Feature Importance' ])
    feature_importance_Path = create_unique_Path( shap_Dir, file_root, 'png' )

    print ('Exporting Feature Importance graph')
    plt.title(Model.target_ncol + ' - Feature Importance')
    plt.tight_layout()
    plt.savefig( feature_importance_Path.p )
    plt.clf()

    ###
    #FEATURE SHAP, beeswatm plot
    ###
    shap.summary_plot(shap_values, Model.df_features, show = False )
    plt.gcf().set_size_inches( 12.0, 12.0)

    file_root = ' '.join( [Model.algorithm_code, 'Feature Shap'] )
    feature_shap_Path = create_unique_Path( shap_Dir, file_root, 'png' )

    print ('Exporting Feature Breakdown graph')
    plt.title(Model.target_ncol + ' - Feature Breakdown')
    plt.tight_layout()
    plt.savefig( feature_shap_Path.p )
    plt.clf()

    ###
    #BREAKDOWN BY TOP FEATURES FEATURE
    ###

    df_temp = pd.DataFrame()
    df_temp["Features"] = Model.df_features.columns
    df_temp["SHAP"] = [np.mean(np.abs(shap_values[:,i])) for i in range(Model.df_features.shape[1])]
    df_temp.sort_values(by=["SHAP"], ascending=False, inplace=True)
    top_features = list(df_temp['Features'])

    for i in range( int(Model.top_shap_features) ):

        shap.dependence_plot( top_features[i], shap_values, Model.df_features, interaction_index = None, show = False )
        plt.gcf().set_size_inches( 12.0, 12.0 )

        file_root = ' '.join( [Model.algorithm_code, top_features[i] ]  )
        dependence_plot_Path = create_unique_Path( shap_Dir, file_root, 'png' )

        print ('Exporting ' + top_features[i] + ' graph')
        plt.title(Model.target_col + ' - ' + top_features[i])
        plt.tight_layout()
        plt.savefig( dependence_plot_Path.p )
        plt.clf()
