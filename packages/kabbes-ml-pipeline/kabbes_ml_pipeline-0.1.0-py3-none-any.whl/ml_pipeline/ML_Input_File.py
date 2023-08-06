### ML-Pipeline
import ml_pipeline
import dir_ops.dir_ops as do
import py_starter.py_starter as ps
import database_connections.sql_support_functions as ssf

import pandas as pd


class Input_File( ml_pipeline.ML_ParentClass.ML_ParentClass ):

    SUFFIX = '_INPUT_FILE'

    DEFAULT_KWARGS = {
    'root': '',
    'nickname': '',
    'query': None,
    'database_conn_params': {},
    'database_conn': None,
    'sample_length': 100,
    'cleaned_extension': '.parquet',
    'cleaned_sample_extension': '.csv',
    'raw_extension': '.parquet',
    'raw_sample_extension': '.csv',
    'to_use': False
    }

    UPDATED_OPTIONS = {
    1: [ 'Open Features', 'open_Child_user' ],
    2: [ 'Clean Raw Dataset', 'clean_pipeline' ],
    3: [ 'Query from Source Database', 'query_pipeline' ],
    4: [ 'Move from Query Staging', 'move_from_query_staging' ]
    }

    def __init__( self, Input_Files_inst, **override_kwargs ):

        ml_pipeline.ML_ParentClass.ML_ParentClass.__init__( self, Input_File.DEFAULT_KWARGS, **override_kwargs )

        ### initialize the attributes
        self.Input_Files = Input_Files_inst
        self.Model = self.Input_Files.Model
        self.Models = self.Model.Models #class ML_Model

        ### init the DFs
        self.df_raw = pd.DataFrame()
        self.df_raw_sample = pd.DataFrame()
        self.df_cleaned = pd.DataFrame()
        self.df_cleaned_sample = pd.DataFrame()

        self._set_Paths()
        self.make_Features()

        if len(self.Features) > 0:
            self.to_use = True

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
            return self.Features

    def _set_Paths( self ):

        self.raw_Path =            do.Path( self.Models.data_Dirs['raw'].join( self.root + self.raw_extension ) )
        self.raw_sample_Path =     do.Path( self.Models.data_Dirs['raw_samples'].join( self.root + self.raw_sample_extension ) )
        self.cleaned_Path =        do.Path( self.Models.data_Dirs['cleaned'].join( self.root + self.cleaned_extension ) )
        self.cleaned_sample_Path = do.Path( self.Models.data_Dirs['cleaned_samples'].join( self.root + self.cleaned_sample_extension ) )
        self.query_export_Path =   do.Path( self.Models.data_Dirs['query_results_staging'].join( self.raw_Path.filename ) )

    def print_imp_atts( self, **kwargs ):

        return self._print_imp_atts_helper( atts = ['root','nickname'], **kwargs )

    def print_one_line_atts( self, **kwargs ):

        return self._print_one_line_atts_helper( atts = ['type','root','nickname'], **kwargs )

    def make_Features( self ):

        class_pointer_params = {
        'Feature_class_pointer': self.get_attr('Feature_class_pointer')
        }

        self.Features = self.Features_class_pointer( self, **class_pointer_params )

    def move_from_query_staging( self ):

        if self.query_export_Path.exists():
            if self.raw_Path.exists():
                if input( 'This operation will overwrite the current file in Data/Raw/. Type "overwrite" to continue: ' ) == 'overwrite':
                    self.raw_Path.remove( override = True )

                else:
                    print ('Overwrite cancelled by user')
                    return

            print ('Moving from Query Staging to Raw')
            self.query_export_Path.copy( self.raw_Path )
            self.query_export_Path.remove( override = True )

            # generating raw sample
            self.import_raw()
            self.gen_raw_sample()
            self.export_raw_sample()

        else:
            print ('No file in Query Staging to move to Raw')

    def clean_pipeline( self ):

        self.import_raw()
        print ('DF_RAW')
        print (self.df_raw.head())

        self.gen_raw_sample()
        self.export_raw_sample()

        self.clean()
        print ('DF_CLEANED')
        print (self.df_cleaned.head())

        self.gen_cleaned_sample()
        self.export_cleaned()
        self.export_cleaned_sample()

    def clean( self ):

        """this needs to be defined by a child class"""
        pass

    def prep_for_joining( self ):

        self.df_cleaned = self.Features.rename_cols_to_ncols( self.df_cleaned )

    def gen_sample( self, att ):

        #att is equal to "raw" or "cleaned"
        gen_method = 'gen_' + att + '_sample'
        self.run_method( gen_method )

    def gen_cleaned_sample( self ):
        self.df_cleaned_sample = mlsf.generate_sample_df( self.df_cleaned, length = self.sample_length )

    def gen_raw_sample( self ):
        self.df_raw_sample = mlsf.generate_sample_df( self.df_raw, length = self.sample_length )

    def get_possible_ncols( self ):

        if self.df_cleaned_sample.empty:
            if self.cleaned_Path.exists():
                self.import_cleaned_sample( print_off = False )

        possible_ncols = []
        for col in list(self.df_cleaned_sample.columns):
            ncol = mlsf.join_nickname_and_col( self.nickname, col )
            possible_ncols.append( ncol )

        return possible_ncols

    ### Query
    def get_database_conn( self ):

        if self.database_conn == None:

            # the user has chosen to override the Models database connection
            if self.database_conn_params != {}:
                self.database_conn = ssf.get_DatabaseConnection( **self.database_conn_params )

            # the user wants to use the default connection params given
            else:
                if self.Models.database_conn == None:
                    self.Models.get_database_conn()

                self.database_conn = self.Models.database_conn

    def query_pipeline( self ):

        self.run_query()
        self.export_query_staging()

    def run_query( self ):

        self.get_database_conn()
        if self.query != None:
            self.df_query = self.database_conn.query( self.query ) #execute the query string

        else:
            print ('query is empty, cannot execute')

    ### IMPORT FUNCTIONS
    def import_df( self, attribute_name_df, import_Path, **kwargs ):

        if import_Path.ending == 'parquet':
            kwargs = ps.replace_default_kwargs( {'engine': self.Models.parquet_engine}, **kwargs )

        df_import = mlsf.import_df_from_Path( import_Path, **kwargs )
        self.set_attr( attribute_name_df, df_import )

    def import_cleaned( self, **kwargs ):

        mlsf.import_df( self, 'df_cleaned', self.cleaned_Path, **kwargs )

        cols_to_keep = self.Features.get_list_of_cols()
        self.df_cleaned = self.df_cleaned[ cols_to_keep ]

    def import_cleaned_sample( self, **kwargs ):
        mlsf.import_df( self, 'df_cleaned_sample', self.cleaned_sample_Path, **kwargs )

    def import_raw( self, **kwargs ):
        mlsf.import_df( self, 'df_raw', self.raw_Path, **kwargs )

    def import_raw_sample( self, **kwargs ):
        mlsf.import_df( self, 'df_raw_sample', self.raw_Path, **kwargs )

    ### EXPORT FUNCTIONS
    def export_cleaned( self, **kwargs ):
        mlsf.export_df( self,  'df_cleaned', self.cleaned_Path, **kwargs )

    def export_cleaned_sample( self, **kwargs ):
        mlsf.export_df( self,  'df_cleaned_sample', self.cleaned_sample_Path, **kwargs )

    def export_raw( self, **kwargs ):
        mlsf.export_df( self,  'df_raw', self.raw_Path, **kwargs )

    def export_raw_sample( self, **kwargs ):
        mlsf.export_df( self,  'df_raw_sample', self.raw_sample_Path, **kwargs )

    def export_query_staging( self, **kwargs ):
        mlsf.export_df( self,  'df_query', self.query_export_Path, **kwargs )
