### import from ml_pipeline
import ml_pipeline
import py_starter.py_starter as ps
import dir_ops.dir_ops as do

import os


file_Path = do.Path( os.path.abspath(__file__) )
name = file_Path.root.split( ml_pipeline.ML_Models.Models.SUFFIX )[0]
repo_Dir = file_Path.ascend()

custom_Model_module =       do.Path.import_module_path( repo_Dir.join( name + ml_pipeline.ML_Model.Model.SUFFIX + '.py' ) ) 
custom_Input_Files_module = do.Path.import_module_path( repo_Dir.join( name + ml_pipeline.ML_Input_Files.Input_Files.SUFFIX + '.py' ) )
custom_Input_File_module =  do.Path.import_module_path( repo_Dir.join( name + ml_pipeline.ML_Input_File.Input_File.SUFFIX + '.py' ) )
custom_Features_module =    do.Path.import_module_path( repo_Dir.join( name + ml_pipeline.ML_Features.Features.SUFFIX + '.py' ) )
custom_Feature_module =     do.Path.import_module_path( repo_Dir.join( name + ml_pipeline.ML_Feature.Feature.SUFFIX + '.py' ) )

### Edit your own database params here
database_conn_params = {}

class Models( ml_pipeline.ML_Models.Models ):

    OVERRIDE_KWARGS = {
    'Model_class_pointer':       custom_Model_module.Model,
    'Input_Files_class_pointer': custom_Input_Files_module.Input_Files,
    'Input_File_class_pointer':  custom_Input_File_module.Input_File,
    'Features_class_pointer':    custom_Features_module.Features,
    'Feature_class_pointer':     custom_Feature_module.Feature,
    'database_conn_params':      database_conn_params
    }

    def __init__( self, **supplemental_kwargs ):

        kwargs = ps.merge_dicts( Models.OVERRIDE_KWARGS, supplemental_kwargs )
        ml_pipeline.ML_Models.Models.__init__( self, name, repo_Dir, **kwargs )

if __name__ == '__main__':

    Models_inst = Models()
    Models_inst.run()
