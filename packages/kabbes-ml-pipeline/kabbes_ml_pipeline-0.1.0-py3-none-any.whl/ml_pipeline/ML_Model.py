import ml_pipeline
import ml_pipeline.ML_params as mlp
import ml_pipeline.ML_support as mlsf

import py_starter.py_starter as ps
import dir_ops.dir_ops as do

import time
import pandas as pd


class Model( ml_pipeline.ML_ParentClass.ML_ParentClass ):

    SUFFIX = '_MODEL'

    DEFAULT_KWARGS = {
    'target_ncol' : 'NICKNAME-INSERT_YOUR_TARGET_COLUMN',
    'to_run' : False,
    'id_ncol': 'ID',
    'algorithm_code' : 'default',
    'joining_code': 'default',
    'generic_cleaning_code': 'default',
    'preprocessing_code': 'default',
    'postprocessing_code': 'default',
    'generate_shap': True,
    'top_shap_features': 5,
    'use_cached_dataset': False,
    'cached_extension': '.parquet',
    'use_cached_model': False,
    'pickle_extension': '.pickle'
    }

    EXCEL_PARAMS = ['target_ncol','to_run','id_ncol','algorithm_code',
                    'joining_code','generic_cleaning_code','preprocessing_code',
                    'postprocessing_code','generate_shap','top_shap_features','use_cached_dataset','use_cached_model']

    RELATIVE_DATA_DIR_KEYS = [ 'business_users','cached','model_pickles','results','results_sample','results_simple','shap' ]

    UPDATED_OPTIONS = {
    1: [ 'Open Input Files', 'open_Child_user' ],
    2: [ 'Run Pipeline', 'run_pipeline' ],
    }

    def __init__( self, Models_inst, name, **override_kwargs ):

        ml_pipeline.ML_ParentClass.ML_ParentClass.__init__( self, Model.DEFAULT_KWARGS, **override_kwargs )

        ### initalize the attributes
        self.Models = Models_inst
        self.name = name

        self._import()
        self._set_Dirs()
        self._set_Paths()
        self._gen_templates()
        self._load_modules()

        ###
        self.id_nickname, self.id_col = mlsf.split_ncol( self.id_ncol )
        self.target_nickname, self.target_col = mlsf.split_ncol( self.target_ncol )
        self.propensity_col = mlp.PROPENSITY_COL_PREFIX + self.target_col

        self.make_Input_Files()


    def __len__( self ):

        return 1

    def __iter__( self ):

        self.i = -1
        return self

    def __next__( self ):

        self.i += 1
        if self.i >= len(self):
            raise StopIteration
        else:
            return self.Input_Files

    def _set_Dirs( self ):

        self._set_data_Dirs()
        self._create_Dirs()

    def _set_data_Dirs( self ):

        self.data_Dirs = {}
        for key in self.RELATIVE_DATA_DIR_KEYS:
            Model_Dir = do.Dir( self.Models.data_Dirs[key].join( self.name ) )
            self.data_Dirs[ key ] = Model_Dir

    def _create_Dirs( self ):

        for key in self.data_Dirs:
            self.data_Dirs[ key ].create()

    def _set_Paths( self ):

        """this is separate from _set_Paths because we need to import "algorithm" from the excel file first"""

        for key in mlp.CODE_KEYS:

            # algorithm_code
            key_code = key + '_code'
            key_code_value = self.get_attr( key_code )

            # algorithm_Dir
            Dir_key = key + '_Dir'
            Dir_value = self.Models.get_attr( Dir_key )

            # algorithm_Path
            Path_key = key + '_Path'
            Path_value = do.Path( Dir_value.join( key_code_value + '.py' ) )

            self.set_attr( Path_key, Path_value )

        self.cached_pre_Path =     do.Path( self.data_Dirs['cached'].join( 'PRE' + self.cached_extension ) )
        self.cached_cleaned_Path = do.Path( self.data_Dirs['cached'].join( 'CLEANED' + self.cached_extension ) )
        self.model_export_Path =   do.Path( self.data_Dirs['model_pickles'].join( self.algorithm_code + self.pickle_extension ) )

    # Generating templates
    def _gen_templates( self ):

        '''checks to see if each of these has been created, otherwise it loads them '''

        for key in mlp.CODE_KEYS:

            #algorithm_Path
            template_Path = mlp.template_Paths[ key ]
            inst_Path = self.get_attr( key + '_Path' )

            mlsf.gen_from_template( template_Path, inst_Path )

    ### Loading modules
    def _load_modules( self ):

        for key in mlp.CODE_KEYS:

            #algorithm_Path
            inst_Path = self.get_attr( key + '_Path' )
            module = ps.import_module_from_path( inst_Path.p )

            #algorithm_module = module
            self.set_attr( key + '_module', module )

    def _import( self ):

        # check if the Models instance has columns for this Model, otherwise the defaults will be exported
        if self.name not in list(self.Models.df_params.columns):
            self._export_to_df_params()

        if self.name not in list(self.Models.df_features.columns):
            self._export_to_df_features()

        self._import_from_df_params()
        self._import_from_df_features()

    def _import_from_df_params( self ):

        self.df_params = self.Models.df_params[ [mlp.PARAMETER_COL, self.name] ]
        dict_mapping = mlsf.get_dict_from_df( self.df_params, key_col = mlp.PARAMETER_COL, val_col = self.name )
        self.set_atts( dict_mapping )

    def _import_from_df_features( self ):

        self.df_features = self.Models.df_features[ [mlp.FEATURE_COL, self.name] ]

    def _export_to_df_params( self ):

        params = []
        for param in self.EXCEL_PARAMS:
            params.append( self.get_attr( param ) )

        self.Models.df_params[ self.name ] = pd.DataFrame( { self.name: params } )[ self.name ]

    def _export_to_df_features( self ):

        self.Models.df_features[ self.name ] = pd.DataFrame( {self.name: []} )[ self.name ]

    def make_Input_Files( self ):

        class_pointer_params = {
        'Input_File_class_pointer': self.get_attr('Input_File_class_pointer'),
        'Features_class_pointer': self.get_attr('Features_class_pointer'),
        'Feature_class_pointer': self.get_attr('Feature_class_pointer')
        }

        self.Input_Files = self.Input_Files_class_pointer( self, **class_pointer_params )

    def print_imp_atts( self, print_off = True ): #if print_off==True, returns None, else: returns str

        atts_and_display_names = {
        'name': 'Name',
        'target_col':'Target Column',
        'to_run': 'To Run'
        }

        string = self._print_imp_atts_helper( atts_and_display_names = atts_and_display_names, print_off = False ) + '\n'
        string += 'Input_Files:\n'

        for Input_File in self:
            string += Input_File.print_one_line_atts( print_off = False ) + '\n'

        if len(self) > 0:
            string = string[:-1]

        return self.print_string( string, print_off = print_off )

    def print_one_line_atts( self, print_off = True, leading_string = '\t' ):  #if print_off==True, returns None, else: returns str

        atts_and_display_names = {
        'type': 'type',
        'name': 'Name',
        'target_col':'Target Column',
        'to_run': 'To Run'
        }
        return self._print_one_line_atts_helper( atts_and_display_names = atts_and_display_names, print_off = print_off, leading_string = leading_string )

    ### Cache Functions
    def import_cached( self, **kwargs ):
        mlsf.import_df( self, 'df_pre', self.cached_pre_Path, **kwargs )
        mlsf.import_df( self, 'df_cleaned', self.cached_cleaned_Path, **kwargs )

    def export_cached( self, **kwargs ):
        mlsf.export_df( self, 'df_pre', self.cached_pre_Path, **kwargs )
        mlsf.export_df( self, 'df_cleaned', self.cached_cleaned_Path, **kwargs )

    ### model I/O
    def import_model_from_pickle( self ):

        print ('Importing model from ' + str(self.model_export_Path))
        self.model = ps.import_from_pickle( self.model_export_Path.p )

    def export_model_to_pickle( self ):

        print ('Exporting model to ' + str(self.model_export_Path))
        ps.export_to_pickle( self.model, self.model_export_Path.p )

    ### PIPELINE Functions
    def read_files( self ):

        print ('Reading Files')
        self.Input_Files.read_files()

    def join_files( self ):

        print ('Joining Files: ' + str(self.joining_code))

        # renames each column to have the prefix
        for Input_File in self.Input_Files:
            Input_File.prep_for_joining()

        self.joining_module.join( self )

        # Set the ID Feature as the index for the Model
        self.df_joined.set_index( self.id_ncol, inplace = True )

    def generic_cleaning( self ):

        print ('Generic Cleaning: ' + str(self.generic_cleaning_code) )

        self.generic_cleaning_module.clean( self )

    def preprocess( self ):

        print ('Preprocessing: ' + str(self.preprocessing_code))

        self.df_pre = self.df_cleaned.copy()

        self.Input_Files.preprocess()
        self.preprocessing_module.preprocess( self )
        self.algorithm_module.preprocess( self )

    def run_algorithm( self ):

        print ('Running Algorithm: ' + str(self.algorithm_code) )

        self.algorithm_module.model_prep( self )

        if self.use_cached_model:
            self.import_model_from_pickle()
        else:
            self.algorithm_module.fit_model( self )
            self.export_model_to_pickle()

        self.algorithm_module.run_model( self )

    def postprocess( self ):

        print ('Postprocessing: ' + str(self.postprocessing_code))

        self.algorithm_module.postprocess( self ) #df_results_all
        self.postprocessing_module.postprocess( self ) #df_post

        print ('Prepping Exports')

        self.df_results_business = self.df_results_propensity.join( self.df_cleaned, how = 'left' )
        self.df_results_simple = self.df_post[ self.propensity_col ]
        self.df_results_sample = mlsf.generate_sample_df( self.df_post )

    def export_results( self ):

        print ('Exporting Results')

        self.export_data( self.df_results_business.reset_index(),                       'business_users', self.algorithm_code + '_Business Results', 'csv' )
        self.export_data( self.df_results_pre.reset_index(),                            'results',        self.algorithm_code + '_Results',          'parquet')
        self.export_data( self.df_results_simple.reset_index(),                         'results_simple', self.algorithm_code + '_Results Simple',   'csv' )
        self.export_data( mlsf.generate_sample_df( self.df_results_pre ).reset_index(), 'results_sample', self.algorithm_code + '_Results Sample', 'csv' )

    def export_data( self, df, data_Dir_key, root, ending ):

        unique_Path = mlsf.create_unique_Path( self.data_Dirs[ data_Dir_key ], root, ending )
        mlsf.export_df( self, export_Path = unique_Path, df = df )

    def shap( self ):

        if self.generate_shap:
            print('Generating SHAP graphs')
            mlsf.shap_importance( self )

    def run_pipeline( self ):

        print ('Starting Model Pipeline...')
        print (self)
        self.start_time = time.time()

        if not self.use_cached_dataset:
            self.read_files()
            self.join_files()
            self.generic_cleaning()
            self.preprocess()
            self.export_cached()

        else:
            self.import_cached()

        self.run_algorithm()
        self.postprocess()
        self.export_results()
        self.shap()

        self.end_time = time.time()
        print('Pipeline Completed in ' + str(self.end_time-self.start_time) + ' seconds.')
