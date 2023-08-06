### ML-Pipeline
import ml_pipeline
import dir_ops.dir_ops as do
import py_starter.py_starter as ps
import pandas as pd

class Input_Files( ml_pipeline.ML_ParentClass.ML_ParentClass ):

    SUFFIX = '_INPUT_FILES'

    DEFAULT_KWARGS = {
    }

    UPDATED_OPTIONS = {
    1: [ 'Open Input File', 'open_Child_user' ],
    2: [ 'Make Input File', 'make_Input_File_user' ]
    }

    def __init__( self, Model_inst, **override_kwargs ):

        ##
        ml_pipeline.ML_ParentClass.ML_ParentClass.__init__( self, Input_Files.DEFAULT_KWARGS, **override_kwargs )

        ###
        self.Model = Model_inst
        self.Models = self.Model.Models

        ###
        self.Input_Files = {} #root is the key, Input_File is the value
        self.load_Input_Files()

    def __len__( self ):

        return len(self.Input_Files)

    def __iter__( self ):

        self.i = -1
        return self

    def __next__( self ):

        self.i += 1
        if self.i >= len(self):
            raise StopIteration
        else:
            return self.Input_Files[ list(self.Input_Files.keys())[self.i] ]

    def print_imp_atts( self, print_off = True ):

        string = self._print_imp_atts_helper( atts = ['type'], print_off = False ) + '\n'
        string += 'Input Files:\n'
        for Child_inst in self:
            string += Child_inst.print_one_line_atts( print_off = False ) + '\n'

        string = string[:-1]
        return self.print_string( string, print_off = print_off )

    def print_one_line_atts( self, print_off = True, leading_string = '\t' ):

        return self._print_one_line_atts_helper( atts = ['type'], print_off = print_off, leading_string = leading_string )

    def load_Input_Files( self ):

        Input_File_Paths = self.Models.Input_File_child_Dir.list_contents_Paths( block_dirs = True )

        for Input_File_Path in Input_File_Paths:
            self.make_Input_File( Input_File_Path )

    def make_Input_File_user( self ):

        Input_File_Paths = self.Models.Input_File_child_Dir.list_contents_Paths( block_dirs = True )

        roots = [ P.root for P in Input_File_Paths ]
        while True:
            root = input('Enter the root for the new Input_File: ')
            if root not in roots:
                break
            else:
                print ('The root is already used, enter another')

        nicknames = [ InF.nickname for InF in self ]
        while True:
            nickname = input('Enter the nickname for ' + str(root) + ': ')
            if nickname not in nicknames:
                break
            else:
                print ('That nickname is already used, enter another')

        Input_File_Path = do.Path( self.Models.Input_File_child_Dir.join( root + '.py' ) )

        self.gen_Input_File_child( Input_File_Path, nickname )
        self.make_Input_File( Input_File_Path )

    def make_Input_File( self, Input_File_Path, **other_kwargs ):

        module = ps.import_module_from_path( Input_File_Path.p )

        class_pointer_params = {
        'Features_class_pointer': self.get_attr('Features_class_pointer'),
        'Feature_class_pointer': self.get_attr('Feature_class_pointer')
        }

        new_Input_File = module.Input_File( self, **class_pointer_params, **other_kwargs )
        self._add_Input_File( new_Input_File )

    def _add_Input_File( self, new_Input_File ):

        self.Input_Files[ new_Input_File.root ] = new_Input_File

    def gen_Input_File_child( self, Input_File_Path, nickname ):

        if not Input_File_Path.exists():

            ml_pipeline.ML_params.template_Paths['Input_File_child'].copy( Input_File_Path )
            string = Input_File_Path.read()

            formatting_dict = {
                'Parent_Input_File_Pointer': self.Models.name + self.Input_File_class_pointer.SUFFIX,
                'NICKNAME': nickname
            }
            formatted_string = ps.smart_format( string, formatting_dict ) 
            
            Input_File_Path.write( string = formatted_string )

        else:
            print ('This Input_File already exists')

    def run_queries( self ):

        for InF in self:
            InF.run_query()

    def read_files( self ):

        for InF in self:
            if InF.to_use:
                InF.import_cleaned()

    def preprocess( self ):

        for InF in self:
            if InF.to_use:
                InF.print_one_line_atts()
                InF.preprocess()

        for InF in self:
            Features_to_drop = InF.Features.select_Children_where( 'flag_code', 'drop_at_preprocess' )
            ncols_to_drop = [ Feature_inst.ncol for Feature_inst in Features_to_drop ]
            self.Model.df_pre = InF.Features.drop_ncols_from_df( self.Model.df_pre, ncols_to_drop, remove_from_Features = True )
