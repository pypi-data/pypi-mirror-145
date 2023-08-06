from py_starter import py_starter as ps
from dir_ops import dir_ops as do

import os

###
file_Path = do.Path( os.path.abspath(__file__) )
repo_Dir = file_Path.ascend( level_to_ascend = 3 ) #user_profile/src/user_profile/profile_import.py
templates_Dir = do.Dir( file_Path.ascend().join( 'Templates' ) )

trigger_beg = '{{'
trigger_end = '}}'


def get_user_env_var() -> str:

    """returns the environment variable "USER", if it doesn't exists, return a default value"""

    user_var = ps.get_env_var( 'USER' )

    if user_var == None:
        user_var = 'USER'

    return user_var

def get_template_Path() -> do.Path:

    template_option_Paths = templates_Dir.list_contents_Paths(block_dirs=True,block_paths=False)

    # make sure we only have Profile Templates in here
    for i in range(len(template_option_Paths)-1, -1, -1):

        if template_option_Paths.Paths[i].ending != 'py':
            del template_option_Paths.Paths[i]
        elif template_option_Paths.Paths[i].root == '__init__':
            del template_option_Paths.Paths[i]

    # This will be an error, no template options present
    if len(template_option_Paths) == 0:
        print ('No templates available')
        assert False
    
    else:

        ps.print_for_loop( [ P.root for P in template_option_Paths ] )
        if len(template_option_Paths) == 1:
            ind = 0
 
        else:
            ind = ps.get_int_input( 1, len(template_option_Paths), prompt='Select a template' ) - 1

        return template_option_Paths.Paths[ind]


def create_profile( user_module_Path: do.Path ) -> None:

    template_Path = get_template_Path()

    #copy and paste the template
    print ('Generating your user Profile')
    template_Path.copy( user_module_Path, print_off = False )

    #read the contents of the newly created module
    template_contents = user_module_Path.read()

    #format the contents of the template 
    formatting_dict = {
        'id': get_user_env_var(),
        'default_repo_parent_Dir': repo_Dir.ascend().p
    }

    #enter values for all other values that couldn't be filled in
    formatting_values = ps.find_string_formatting( template_contents, trigger_beg=trigger_beg,trigger_end=trigger_end )

    for formatting_value in formatting_values:
        stripped_value = formatting_value[ len(trigger_beg): -1*len(trigger_end) ]

        if stripped_value not in formatting_dict:
            user_value = input('Enter a value for ' + str(stripped_value) + ': ')    
            formatting_dict[stripped_value] = user_value
    
    formatted_contents = ps.smart_format( template_contents, formatting_dict, trigger_beg=trigger_beg, trigger_end=trigger_end  )

    #write the formatted info back
    user_module_Path.write( string = formatted_contents )
    

def init():

    user_var = get_user_env_var()
    user_module_Path = do.Path( file_Path.ascend().join('Users', user_var + '.py') )

    if not user_module_Path.exists():
        create_profile( user_module_Path )

    user_module = user_module_Path.import_module()
    return user_module.Profile()

