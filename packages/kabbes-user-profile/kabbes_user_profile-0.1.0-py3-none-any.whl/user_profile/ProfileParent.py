from parent_class import ParentClass

class ProfileParent( ParentClass ):

    def __init__( self ):

        ParentClass.__init__( self )

    def welcome_message( self ):

        print ()
        print ('----------------')
        print ('hi ' + self.first_name )
        print ('----------------')
        print ()

    def init_user( self ):

        self.welcome_message()

    def print_imp_atts( self, **kwargs ):
        return self._print_imp_atts_helper( atts = ['id','email','first_name','last_name','Path'], **kwargs )

    def print_one_line_atts( self, **kwargs):
        return self._print_one_line_atts_helper( atts = ['type','id','name'], **kwargs )
