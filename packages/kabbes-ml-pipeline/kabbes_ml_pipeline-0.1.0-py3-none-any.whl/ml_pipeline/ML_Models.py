import ml_pipeline
import ml_pipeline.ML_support as mlsf
import ml_pipeline.ML_params as mlp

### Analytics-Packages
import analytics_packages.custom_xlwings as cxw
import dir_ops.dir_ops as do
import py_starter.py_starter as ps
import database_connections.sql_support_functions as ssf

### import other
import os
import pandas as pd

file_Path = do.Path( os.path.abspath(__file__) )


class Models( ml_pipeline.ML_ParentClass.ML_ParentClass ):

    SUFFIX = '_MODELS'

    DEFAULT_KWARGS = {
    'Model_class_pointer': ml_pipeline.ML_Model.Model,
    'Input_Files_class_pointer': ml_pipeline.ML_Input_Files.Input_Files,
    'Input_File_class_pointer': ml_pipeline.ML_Input_File.Input_File,
    'Features_class_pointer': ml_pipeline.ML_Features.Features,
    'Feature_class_pointer': ml_pipeline.ML_Feature.Feature,

    'user_profile': None,
    'database_conn_params': {},
    'database_conn': None,
    'parquet_engine' : mlp.PARQUET_ENGINE,
    'default_feature_flag': mlp.DEFAULT_FEATURE_FLAG,
    'feature_flag_codes': mlp.FEATURE_FLAG_CODES.copy()
    }

    UPDATED_OPTIONS = {
    1: [ 'Open Model', 'open_Child_user' ],
    2: [ 'Run Models', 'run_Models' ],
    3: [ 'Make Model', 'make_Model_user' ],
    4: [ 'Delete Model', 'delete_Model_user' ],
    5: [ 'Delete Results', 'delete_results']
    }

    def __init__( self, name, repo_Dir, **override_kwargs ):

        self.DEFAULT_KWARGS['Models_class_pointer'] = Models

        ml_pipeline.ML_ParentClass.ML_ParentClass.__init__( self, self.DEFAULT_KWARGS, **override_kwargs )

        self.name = name
        self.Dir = repo_Dir
        self.Models = {} #key is the Model name, value is the Model Object

        self._set_Dirs()
        self._set_Paths()
        self._gen_excel()
        self._import_from_excel()

        ### Generate the templates from the newly found excel data, if the files don't exist
        self._gen_child_classes()
        self.load_Models()
        self._export_to_excel()

        ###
        self.print_imp_atts()

    def __len__( self ):

        '''returns the number of Models in the class instance '''

        return len(self.Models)

    def __iter__( self ):

        self.i = -1
        return self

    def __next__( self ):

        self.i += 1
        if self.i >= len(self):
            raise StopIteration
        else:
            return self.Models[ list(self.Models.keys())[self.i] ]

    def _set_Dirs( self ):

        '''Input_File_child_Dir = Dir( 'asdf/asdf/asdf' ) '''

        self.Dirs = []
        for relative_dir_key in list(mlp.relative_dirs.keys()):

            relative_dir_value = mlp.relative_dirs[ relative_dir_key ]
            Dir_key = relative_dir_key + '_Dir'

            if not self.has_attr( Dir_key ): #if the user didn't override with their own Dir

                # algorithm_Dir = Dir( self.repo_dir.join( 'Algorithms' )   )
                Dir_value = do.Dir( self.Dir.join( relative_dir_value ) )
                self.set_attr( Dir_key, Dir_value )

            else:
                Dir_value = self.get_attr( Dir_key )

            self.Dirs.append( Dir_value )

        self._set_data_Dirs()
        self._create_Dirs()

    def _set_data_Dirs( self ):

        '''data_Dirs = { 'business_users': Dir(self.data_Dir.join('Business Users')) } '''

        self.data_Dirs = {}
        for relative_data_dir_key in list(mlp.relative_data_dirs.keys()):

            relative_data_dir_value = mlp.relative_data_dirs[ relative_data_dir_key ]
            Dir_value = do.Dir( self.data_Dir.join( relative_data_dir_value ) )
            self.data_Dirs[relative_data_dir_key] = Dir_value

    def _create_Dirs( self ):

        '''initialize the Dirs if they do not already exist '''

        for Dir in self.Dirs:
            Dir.create()
        for key in self.data_Dirs:
            self.data_Dirs[ key ].create()

    def _set_Paths( self ):

        '''Set the paths of various child Paths'''

        for class_key in mlp.CLASSES_KEYS:

            # ML_Features.Features
            class_pointer = self.get_attr( class_key + '_class_pointer' )
            suffix = class_pointer.SUFFIX

            # repo_Dir/name_FEATURES.py
            child_class_Path = do.Path( self.Dir.join( self.name + suffix + '.py' ) )

            # child_Features_class_Path = child_class_Path
            self.set_attr( 'child_' + class_key + '_class_Path', child_class_Path )

        self.excel_Path = do.Path( self.Dir.join( self.name + mlp.MODEL_INPUTS_SUFFIX + '.xlsx' ) )

    def _gen_child_classes( self ):

        '''generate child classes from templates'''

        for class_key in mlp.CLASSES_KEYS:

            # template_Paths[ 'Features' ]
            template_Path = mlp.template_Paths[ class_key ]

            # self.child_Features_class_Path
            inst_Path = self.get_attr( 'child_' + class_key + '_class_Path' )

            mlsf.gen_from_template( template_Path, inst_Path )

    def _gen_excel( self ):

        mlsf.gen_from_template( mlp.template_Paths['model_inputs'], self.excel_Path )

    def print_imp_atts( self, print_off = True ): #if print_off==True, returns None, else: returns str

        atts_and_display_names = {
        'name':'Name',
        'Dir': 'Dir'
        }

        string = self._print_imp_atts_helper( atts_and_display_names = atts_and_display_names, print_off = False ) + '\n'
        string += 'Models:\n'

        for Model in self:
            string += Model.print_one_line_atts( print_off = False ) + '\n'

        if len(self) > 0:
            string = string[:-1]

        return self.print_string( string, print_off = print_off )

    def print_one_line_atts( self, print_off = True, leading_string = '\t' ):  #if print_off==True, returns None, else: returns str

        atts_and_display_names = {
        'type': 'type',
        'name': 'Name',
        'Dir': 'Dir'
        }
        return self._print_one_line_atts_helper( atts_and_display_names = atts_and_display_names, print_off = print_off, leading_string = leading_string )

    def delete_Model( self, Model_inst ):

        del self.Models[ Model_inst.name ]
        self._export_to_excel()

    def delete_Model_user( self ):

        Model_inst = self.select_Child_user()

        if Model_inst !=  None:
            self.delete_Model( Model_inst )

    def make_Model( self, name, print_off = False, **Model_params ):

        class_pointer_params = {
        'Input_Files_class_pointer': self.get_attr('Input_Files_class_pointer'),
        'Input_File_class_pointer':  self.get_attr('Input_File_class_pointer'),
        'Features_class_pointer':    self.get_attr('Features_class_pointer'),
        'Feature_class_pointer':     self.get_attr('Feature_class_pointer')
        }

        new_Model = self.Model_class_pointer( self, name, **Model_params, **class_pointer_params )
        self._add_Model( new_Model )

        if print_off:
            print ('Adding new Model:')
            new_Model.print_atts()

    def make_Model_user( self ):

        while True:
            name = input('Enter a name for the new Model: ')
            if name in list( self.Models.keys() ):
                print ('That Model name has already been used')
                continue
            break

        self.make_Model( name )
        self._export_excel()

    def _add_Model( self, new_Model ):

        self.Models[ new_Model.name ] = new_Model

    def load_Models( self ):

        '''Loads Models from the Parameters sheet on the Excel Model Inputs file'''

        for col in list(self.df_params.columns):
            if col != mlp.PARAMETER_COL:

                Model_name = col
                self.make_Model( Model_name )

    def run_Models( self ):

        '''Run each Model'''

        for Model in self:
            if Model.to_run:
                Model.run_pipeline()

    def get_database_conn( self ):

        '''get a database connection from said database_conn_params, only needed if you query an Input File'''

        if self.database_conn == None:
            self.database_conn = ssf.import_connection_object( **self.database_conn_params )

    def delete_results( self, override = False ):

        Dirs_to_delete = [
            self.data_Dirs['business_users'],
            self.data_Dirs['cached'],
            self.data_Dirs['model_pickles'],
            self.data_Dirs['results'],
            self.data_Dirs['results_sample'],
            self.data_Dirs['results_simple'],
            self.data_Dirs['shap'],
            ]

        for Dir_to_delete in Dirs_to_delete:
            Dir_to_delete.remove( override = override ) #delete the folder and all contents
            Dir_to_delete.create() #create the folder again

        print ('To properly save changes, exit the program')

    def _import_from_excel( self ):

        '''imports the features and params from excel '''

        self.wb = cxw.get_wb( self.excel_Path.p )
        self.df_features = self.import_df_features()
        self.df_params =   self.import_df_params()

    def import_df_features( self ):

        return cxw.get_df_from_ws( cxw.get_ws( self.wb, sheet = mlp.FEATURES_SHEET_NAME ) )

    def import_df_params( self ):

        return cxw.get_df_from_ws( cxw.get_ws( self.wb, sheet = mlp.PARAMETERS_SHEET_NAME ) )

    def _export_to_excel( self ):

        '''Refreshes the params and features'''

        self._export_params()
        self._export_features()
        self._export_excel()

    def _export_excel( self ):

        '''export the features and parameters dataframes to excel '''

        ws = cxw.get_ws(self.wb, sheet = mlp.FEATURES_SHEET_NAME)
        cxw.clear_all(ws)
        cxw.write_df_to_ws( ws, self.df_features )

        ws = cxw.get_ws(self.wb, sheet = mlp.PARAMETERS_SHEET_NAME)
        cxw.clear_all(ws)
        cxw.write_df_to_ws( ws, self.df_params )

    def _export_params( self ):

        '''export the Model params for each Model'''

        self.df_params = pd.DataFrame( {mlp.PARAMETER_COL: self.Model_class_pointer.EXCEL_PARAMS } )
        for Model_inst in self:
            Model_inst._export_to_df_params()

    def _export_features( self ):

        '''Finds all available features from the Input Files, records each Models flag for each feature'''

        feature_ncols = []
        if len(self) > 0:
            for Input_File_inst in self.get_random_Child().Input_Files:
                feature_ncols.extend( Input_File_inst.get_possible_ncols() )

        df_possible_features = pd.DataFrame( { mlp.FEATURE_COL: feature_ncols } )
        df_possible_features[ mlp.FEATURE_COL ] = df_possible_features[ mlp.FEATURE_COL ].astype( str )

        df_existing_excel_features = self.import_df_features()

        # merge them together, only keeping features that are in df_possible_features
        df_joined_features = df_possible_features.merge( df_existing_excel_features, how = 'left', on = mlp.FEATURE_COL )

        # fill all NaN's with the default feature flag
        df_joined_features.fillna( self.default_feature_flag, inplace = True )
        self.df_features = df_joined_features.sort_values( mlp.FEATURE_COL )

    def exit( self ):

        print ('Exiting...')
        self._export_to_excel()


def init_Models( **kwargs ):

    name = input('Enter a name for your Models class: ')
    repo_Dir = do.Dir(do.get_cwd())

    Models_inst = Models( name, repo_Dir, **kwargs )
    return Models_inst
