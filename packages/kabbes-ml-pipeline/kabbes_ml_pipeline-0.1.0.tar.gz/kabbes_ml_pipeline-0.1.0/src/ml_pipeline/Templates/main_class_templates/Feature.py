### import from ml_pipeline
import ml_pipeline
import py_starter.py_starter as ps


class Feature( ml_pipeline.ML_Feature.Feature ):

    OVERRIDE_KWARGS = {
    }

    def __init__( self, Features_inst, ncol, flag, **supplemental_kwargs ):

        kwargs = ps.merge_dicts( Feature.OVERRIDE_KWARGS, supplemental_kwargs )
        ml_pipeline.ML_Feature.Feature.__init__( self, Features_inst, ncol, flag, **kwargs  )
