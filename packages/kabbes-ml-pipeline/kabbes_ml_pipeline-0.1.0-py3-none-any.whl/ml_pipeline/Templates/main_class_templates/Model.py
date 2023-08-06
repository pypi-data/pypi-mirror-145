### import from ml_pipeline
import ml_pipeline
import py_starter.py_starter as ps



class Model( ml_pipeline.ML_Model.Model ):

    OVERRIDE_KWARGS = {
     }

    def __init__( self, Models_inst, name, **supplemental_kwargs ):

        kwargs = ps.merge_dicts( Model.OVERRIDE_KWARGS, supplemental_kwargs )
        ml_pipeline.ML_Model.Model.__init__( self, Models_inst, name, **kwargs  )
