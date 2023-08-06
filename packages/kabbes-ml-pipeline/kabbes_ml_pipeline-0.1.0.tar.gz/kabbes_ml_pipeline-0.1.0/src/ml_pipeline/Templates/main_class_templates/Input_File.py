### import from ml_pipeline
import ml_pipeline
import py_starter.py_starter as ps



class Input_File( ml_pipeline.ML_Input_File.Input_File ):

    OVERRIDE_KWARGS = {
    }

    def __init__( self, Input_Files_inst, **supplemental_kwargs ):

        kwargs = ps.merge_dicts( Input_File.OVERRIDE_KWARGS, supplemental_kwargs )
        ml_pipeline.ML_Input_File.Input_File.__init__( self, Input_Files_inst, **kwargs  )
