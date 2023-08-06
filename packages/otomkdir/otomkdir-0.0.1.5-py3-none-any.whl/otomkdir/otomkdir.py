import os
from pathlib import Path

def auto_create_folder( default_path = Path( os.environ[ 'USERPROFILE' ], "Desktop" ), folder_extend = "task_list", subfolder_extend = None ):
    default_path = Path( default_path )
    default_list = str( default_path ).split( "\\" )
    for elem in default_list:
        if elem == "":
            default_list.remove( "" )
        else:
            pass
    # print( default_list )

    if subfolder_extend == None:
        folder_path = Path( default_path, folder_extend )
    else:
        folder_path = Path( default_path, folder_extend, subfolder_extend )
        # print( folder_path )
    folder_list = str( folder_path ).split( "\\" )
    # print( folder_list )

    ##remove default path from full path
    for def_folder in default_list:
        folder_list.remove( def_folder )

    # print( len( folder_list ) )
    # print( folder_list )


    increment_path = default_path
    for folder in folder_list:
        increment_path = Path( increment_path, folder )
        # print( increment_path )

        if os.path.isdir( increment_path ) == False:
            os.mkdir( increment_path )
            # return folder_path

        else:
            print( "Directory already exists." )
            # return folder_path
            pass

    return folder_path
