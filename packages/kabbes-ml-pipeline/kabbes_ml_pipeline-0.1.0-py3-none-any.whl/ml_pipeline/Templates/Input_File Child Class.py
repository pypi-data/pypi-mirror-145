import ml_pipeline
import py_starter.py_starter as ps
import dir_ops.dir_ops as do

import {{Parent_Input_File_Pointer}} as Parent_Input_File

import os
import pandas as pd
file_Path = do.Path( os.path.abspath(__file__) )

###
#  FILL OUT AS NEEDED
###
QUERY = None
DATABASE_CONN_PARAMS = {}
NICKNAME = '{{NICKNAME}}' #This should be automatically replaced by Input_Files.gen_Input_File_child()
###
#
###

class Input_File( Parent_Input_File.Input_File ):

    DEFAULT_KWARGS = {
    'query': QUERY,
    'database_conn_params': DATABASE_CONN_PARAMS,
    'root': file_Path.root,
    'nickname': NICKNAME
    }

    def __init__( self, Input_Files_inst, **override_kwargs ):

        ### set the default/overridden kwargs
        joined_kwargs = ps.replace_default_kwargs( Input_File.DEFAULT_KWARGS, **override_kwargs )
        Parent_Input_File.Input_File.__init__( self, Input_Files_inst, **joined_kwargs )

    def clean( self ):

        df = self.df_raw.copy()
        ### Insert Preprocessing instructions



        ###
        self.df_cleaned = df

    def preprocess( self ):

        df = self.Model.df_pre.copy()
        ### Insert Preprocessing instructions



        ###
        self.Model.df_pre = df
