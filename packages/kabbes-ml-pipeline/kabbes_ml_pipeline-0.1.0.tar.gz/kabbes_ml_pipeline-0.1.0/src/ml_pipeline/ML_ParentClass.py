from parent_class import ParentClass
import py_starter.py_starter as ps
import random

class ML_ParentClass( ParentClass ):

    BASE_OPTIONS =  {
        1: [ 'open_Child_user', 'open_Child_user' ],
        2: [ '', 'do_nothing' ],
        3: [ '', 'do_nothing' ],
        4: [ '', 'do_nothing' ],
        5: [ '', 'do_nothing' ],
        6: [ '', 'do_nothing' ],
        7: [ 'Print all attributes', 'print_all_atts' ],
        8: [ 'Print attributes', 'print_atts' ],
        9: [ 'Run Custom Function', 'custom_func' ]
    }

    def __init__( self, DEFAULT_KWARGS, **override_kwargs ):

        ParentClass.__init__( self )

        kwargs = ps.merge_dicts( DEFAULT_KWARGS, override_kwargs )
        self.set_atts( kwargs )

        self.OPTIONS = self.BASE_OPTIONS.copy()
        self.OPTIONS.update( self.UPDATED_OPTIONS )


    def __list_self( self ):

        instances = []

        for Child_inst in self:
            instances.append( Child_inst )
        return instances

    def do_nothing( self ):

        pass

    def run( self ):

        '''Give the user options on what to run'''

        while True:
            print()
            self.print_one_line_atts( leading_string = '')
            option_keys = list(self.OPTIONS.keys())

            for i in range( 1,  max(option_keys) + 1 ):

                if i in option_keys:
                    option = self.OPTIONS[ i ][ 0 ]
                    method = self.OPTIONS[ i ][ 1 ]

                else:
                    option = ''
                    method = 'do_nothing'

                print (str(i) + '. ' + str(option))

            input_key = ps.get_int_input( 1, max(option_keys), prompt = 'Choose the ' + self.type + ' Class method you would like to run: ', exceptions = [''] )
            if input_key == '':
                break

            method = self.OPTIONS[ input_key ][ 1 ]
            self.run_method( method )

        self.exit()

    def custom_func( self ):

        func_input = input( 'Enter the ' + self.type + ' Class method you would like to run: ' )

        if self.has_attr( func_input ):
            self.run_method( func_input )

        else:
            print ('class ' + str(self.type) + ' does not have that method')

    def get_random_Child( self ):

        ind = random.randrange( len(self) )
        instances = self.__list_self()
        return instances[ ind ]

    def open_Child_user( self ):

        Child_inst = self.select_Child_user()
        if Child_inst != None:
            Child_inst.run()

    def select_Child_user( self ):

        instances = self.__list_self()

        for i in range(len(instances)):
            Child_inst = instances[i]
            print ( str(i+1)+'. ' + Child_inst.print_one_line_atts( print_off = False, leading_string = '' ) )

        selection = ps.get_int_input( 1, len(self), prompt = 'Select your Child: ', exceptions = [''] )

        if selection == '':
            return None
        else:
            return instances[ selection - 1 ]

    def lambda_on_Children( self, lambda_func ):

        return [ lambda_func(Child_inst) for Child_inst in self ]

    def select_Children_where( self, att, value ):

        '''return a list of Children instances where Child_add == Child_value '''

        instances = []
        for Child_inst in self:

            if Child_inst.has_attr( att ):
                if Child_inst.get_attr( att ) == value:
                    instances.append( Child_inst )

        return instances

    def exit( self ):

        pass
