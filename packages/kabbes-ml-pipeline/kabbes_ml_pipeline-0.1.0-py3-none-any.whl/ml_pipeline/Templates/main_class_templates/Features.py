### import from ml_pipeline
import ml_pipeline
import py_starter.py_starter as ps


class Features( ml_pipeline.ML_Features.Features ):

    OVERRIDE_KWARGS = {
    }

    def __init__( self, Input_File_inst, **supplemental_kwargs ):

        kwargs = ps.merge_dicts( Features.OVERRIDE_KWARGS, supplemental_kwargs )
        ml_pipeline.ML_Features.Features.__init__( self, Input_File_inst, **kwargs  )
