import os
import dir_ops.dir_ops as do 

'''
This is a file for all repository-specific parameters.
If you have something changes user by user, put it in your user profile
'''

### Set up the file structure info - these are objects from the Path/Dir classes
params_Path = do.Path( os.path.abspath(__file__) )
repo_Dir = params_Path.ascend()
data_Dir = do.Dir( repo_Dir.join('Data') )
wiki_Dir = do.Dir( repo_Dir.join( repo_Dir.dirs[-1] + '.wiki' ) ) #Repository/Repository.wiki
templates_Dir = do.Dir( repo_Dir.join('Templates') )
main_class_templates_Dir = do.Dir( templates_Dir.join('main_class_templates') )
code_templates_Dir = do.Dir( templates_Dir.join('code_templates') )

template_Paths = {
'Models':                   do.Path( main_class_templates_Dir.join('Models.py') ),
'Model':                    do.Path( main_class_templates_Dir.join('Model.py') ),
'Input_Files':              do.Path( main_class_templates_Dir.join('Input_Files.py') ),
'Input_File':               do.Path( main_class_templates_Dir.join('Input_File.py') ),
'Features':                 do.Path( main_class_templates_Dir.join('Features.py') ),
'Feature':                  do.Path( main_class_templates_Dir.join('Feature.py') ),
'Input_File_child':         do.Path( templates_Dir.join('Input_File Child Class.py') ),
'model_inputs':             do.Path( templates_Dir.join('model_inputs.xlsx') ),
'algorithm':                do.Path( code_templates_Dir.join( 'algorithm.py' ) ),
'preprocessing':            do.Path( code_templates_Dir.join( 'preprocessing.py' ) ),
'postprocessing':           do.Path( code_templates_Dir.join( 'postprocessing.py' ) ),
'generic_cleaning':         do.Path( code_templates_Dir.join( 'generic_cleaning.py' ) ),
'joining':                  do.Path( code_templates_Dir.join( 'joining.py') )
}

relative_dirs = {
'Input_File_child': 'Input Files',
'algorithm': 'Algorithms',
'preprocessing': 'Preprocessing',
'postprocessing': 'Postprocessing',
'generic_cleaning': 'Generic Cleaning',
'joining': 'Joining',
'data': 'Data'
}

CLASSES_KEYS = [
'Models',
'Model',
'Input_Files',
'Input_File',
'Features',
'Feature'
]

CODE_KEYS = [
'algorithm',
'joining',
'generic_cleaning',
'preprocessing',
'postprocessing'
]

relative_data_dirs = {
'business_users' : 'Business Users',
'cached': 'Cached',
'cleaned': 'Cleaned',
'cleaned_samples': 'Cleaned Samples',
'model_pickles': 'Model Pickles',
'query_results_staging': 'Query Results Staging',
'raw': 'Raw',
'raw_samples': 'Raw Samples',
'results': 'Results',
'results_sample' : 'Results Sample',
'results_simple' : 'Results Simple',
'shap': 'SHAP',
}

FEATURES_SHEET_NAME = 'Features'
PARAMETERS_SHEET_NAME = 'Parameters'

FEATURE_COL = 'Feature'
PARAMETER_COL = 'Parameter'

MODEL_INPUTS_SUFFIX = '_MODEL_INPUTS'
PROPENSITY_COL_PREFIX = 'PROPENSITY_'

NICKNAME_SEP = '-'

### DEFAULT PARAMS, CAN BE CHANGED IN THE MODELS CLASS
PARQUET_ENGINE = 'fastparquet'
DEFAULT_FEATURE_FLAG = 0
FEATURE_FLAG_CODES = {
0: 'ignore',
1: 'drop_at_preprocess',
2: 'use_in_model'
}
