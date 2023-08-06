### import from ml_pipeline
import ml_pipeline
import py_starter.py_starter as ps



class Input_Files( ml_pipeline.ML_Input_Files.Input_Files ):

    OVERRIDE_KWARGS = {
    }

    def __init__( self, Model_inst, **supplemental_kwargs ):

        kwargs = ps.merge_dicts( Input_Files.OVERRIDE_KWARGS, supplemental_kwargs )
        ml_pipeline.ML_Input_Files.Input_Files.__init__( self, Model_inst, **kwargs  )
