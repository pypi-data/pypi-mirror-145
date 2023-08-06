### ML-Pipeline
import ml_pipeline


class Features( ml_pipeline.ML_ParentClass.ML_ParentClass ):

    SUFFIX = '_FEATURES'
    DEFAULT_KWARGS = {
    }
    UPDATED_OPTIONS = {
    1: [ 'Open Feature', 'open_Child_user' ],
    }

    def __init__( self, Input_File_inst, **override_kwargs ):

        ml_pipeline.ML_ParentClass.ML_ParentClass.__init__( self, Features.DEFAULT_KWARGS, **override_kwargs )

        ### Set up Parents
        self.Input_File = Input_File_inst
        self.Input_Files = self.Input_File.Input_Files
        self.Model = self.Input_Files.Model
        self.Models = self.Model.Models

        #
        self.Features = {} #col is the key, Feature is the value
        self.load_Features()

    def __len__( self ):

        return len(self.Features)

    def __iter__( self ):

        self.i = -1
        return self

    def __next__( self ):

        self.i += 1
        if self.i >= len(self):
            raise StopIteration
        else:
            return self.Features[ list(self.Features.keys())[self.i] ]

    def print_imp_atts( self, print_off = True ):

        string = self._print_imp_atts_helper( atts = ['Input_File'], print_off = False ) + '\n'
        string += 'Features:\n'
        for Feat in self:
            string += Feat.print_one_line_atts( print_off = False ) + '\n'

        string = string[:-1]
        return self.print_string( string, print_off = print_off )

    def print_one_line_atts( self, print_off = True, leading_string = '\t' ):

        string = self._print_one_line_atts_helper( atts = ['type','Input_File'], print_off = False, leading_string = leading_string )
        string += ',\tFeatures: ' + str(len(self))

        return self.print_string( string, print_off = print_off )

    def make_Feature( self, ncol, flag ):

        new_Feature = self.Feature_class_pointer( self, ncol, flag )
        self._add_Feature( new_Feature )
        return new_Feature

    def _add_Feature( self, new_Feature ):

        self.Features[ new_Feature.col ] = new_Feature

    def remove_Feature( self, Feature_to_remove ):

        self.Features.pop( Feature_to_remove.col )

    def load_Features( self ):

        for i in range(len(self.Model.df_features)):

            ncol = self.Model.df_features.loc[ i, mlp.FEATURE_COL ]
            nickname, col = mlsf.split_ncol( ncol )
            if nickname == self.Input_File.nickname:
                flag = self.Model.df_features.loc[ i, self.Model.name ]

                if self.Models.feature_flag_codes[ flag ] != 'ignore':
                    self.make_Feature( ncol, flag )

    def get_list_of_cols( self ):

        return [ Feature_inst.col for Feature_inst in self ]

    ###
    def col_to_ncol( self, col ):

        return mlsf.join_nickname_and_col( self.Input_File.nickname, col )

    def cols_to_ncols( self, cols ):

        ncols = []
        for col in cols:
            ncols.append( self.col_to_ncol(col) )
        return ncols

    def ncol_to_col( self, ncol ):

        nickname, col = mlsf.split_ncol( ncol )
        return col

    def ncols_to_cols( self, ncols ):

        cols = []
        for ncol in ncols:
            cols.append( self.ncol_to_col(ncol) )
        return cols

    ###
    def add_col( self, col, flag = None ):

        ncol = self.col_to_ncol( col )
        if flag == None:
            flag = max(self.Models.feature_flag_codes.keys())

        return self.add_ncol( ncol, flag = flag )

    def add_cols( self, cols, flags = [] ):

        new_Features = []
        for i in range(len(cols)):
            if i < len(flags):
                new_Features.append( self.add_col( cols[i], flag = flags[i] ) )
            else:
                new_Features.append( self.add_col( cols[i] ) )

        return new_Features

    def add_ncol( self, ncol, flag = None ):

        if flag == None:
            flag = max(self.Models.feature_flag_codes.keys())

        return self.make_Feature( ncol, flag )

    def add_ncols( self, ncols, flags = [] ):

        new_Features = []
        for i in range(len(ncols)):
            if i < len(flags):
                new_Features.append( self.add_ncol( ncols[i], flag = flags[i] ) )
            else:
                new_Features.append( self.add_ncol( ncols[i] ) )

        return new_Features

    ### Removing col/fetures
    def remove_col( self, col ):

        Feature_inst = self.Features[ col ]
        self.remove_Feature( Feature_inst )

    def remove_cols( self, cols ):

        for col in cols:
            self.remove_col( col )

    def remove_ncol( self, ncol ):

        col = self.ncol_to_col( ncol )
        self.remove_col( col )

    def remove_ncols( self, ncols ):

        for ncol in ncols:
            self.remove_ncol( ncol )

    ### Dropping columns from dataset
    def drop_columns( self, df, columns, feature_type, remove_from_Features ):

        if remove_from_Features:
            if feature_type == 'col':
                self.remove_cols( columns )

            if feature_type == 'ncol':
                self.remove_ncols( columns )

        return df.drop( columns, axis = 1 )

    def drop_col_from_df( self, df, col, convert_to_ncol = False, remove_from_Features = True ):

        feature_type = 'col'
        column_to_drop = col

        if convert_to_ncol:
            column_to_drop = self.col_to_ncol( col )
            feature_type = 'ncol'

        return self.drop_columns( df, [column_to_drop], feature_type, remove_from_Features )

    def drop_cols_from_df( self, df, cols, convert_to_ncol = False, remove_from_Features = True ):

        feature_type = 'col'
        columns_to_drop = cols

        if convert_to_ncol:
            columns_to_drop = [ self.col_to_ncol( col ) for col in cols ]
            feature_type = 'ncol'

        return self.drop_columns( df, columns_to_drop, feature_type, remove_from_Features )

    def drop_ncol_from_df( self, df, ncol, convert_to_col = False, remove_from_Features = True ):

        feature_type = 'ncol'
        column_to_drop = ncol

        if convert_to_col:
            column_to_drop = self.ncol_to_col( ncol )
            feature_type = 'col'

        return self.drop_columns( df, [column_to_drop], feature_type, remove_from_Features )

    def drop_ncols_from_df( self, df, ncols, convert_to_col = False, remove_from_Features = True ):

        feature_type = 'ncol'
        columns_to_drop = ncols

        if convert_to_col:
            columns_to_drop = [ self.ncol_to_col( ncol ) for ncol in ncols ]
            feature_type = 'col'

        return self.drop_columns( df, columns_to_drop, feature_type, remove_from_Features )

    ###
    def rename_cols_to_ncols(self, df):

        '''Renames all features to have the nickname prefixes HOME_AGE to EXP-HOME_AGE'''

        mapping = {}
        for Feature_inst in self:
            mapping[ Feature_inst.col ] = Feature_inst.ncol

        return df.rename( columns = mapping )
