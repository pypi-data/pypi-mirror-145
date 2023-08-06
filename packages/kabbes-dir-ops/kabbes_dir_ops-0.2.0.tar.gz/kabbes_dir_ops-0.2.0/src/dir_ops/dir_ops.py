from __future__ import annotations
import shutil
import os
import sys
import pathlib
import datetime
import subprocess
import platform
import functools
from typing import List, Any

from parent_class import ParentClass
from py_starter import py_starter as ps


DELIM = '/'
SECONDARY_DELIM = '\\'

def get_cwd() -> str:

    """returns current working directory"""

    cd = os.getcwd()

    #replace the cd with primary delim
    cd_replaced = join( * path_to_dirs(cd) )
    return cd_replaced

def path_to_dirs( path: str ) -> List[str]:

    """splits a path into directories"""
    if path == '':
        return []
    return path.split( DELIM )

def is_file( path: str ) -> bool :

    """returns a boolean value to check if the path is a file"""
    return os.path.isfile( path )

def is_dir( path: str ) -> bool :

    """returns a boolean value to check if the path is a directory"""
    return os.path.isdir( path )

def replace_delims( path: str, secondary_delim: str = SECONDARY_DELIM, delim: str = DELIM ) -> str :

    """turns data\dir\file.txt into data/dir/file.txt"""
    return path.replace( secondary_delim, delim )

def join( *items: str ) -> str:

    """joins a list of dirs into a path"""
    return DELIM.join( items )

def convert_bytes( bytes: int, conversion: str = 'MB' ) -> Tuple[ Any, Any ]:

    try:
        conversion = conversion.upper()
    except:
        pass

    kb_to_b = 1024

    conversion_factors = ['KB','MB','GB','TB','PB','EB']
    if conversion in conversion_factors:

        power = conversion_factors.index(conversion) + 1
        return bytes / (kb_to_b ** power), conversion

    return bytes, None

def walk_root_dir( path ):

    roots = []
    dirs = []
    files = []

    for i,j,k in os.walk(path):

        roots.append(i)
        dirs.append(j)
        files.append(k)

    return roots, dirs, files

def rename_files_to_new_directory( input_folder, export_folder ):

    full_input_paths = get_paths_with_common_parent( input_folder )
    relative_input_paths = remove_prefix_from_paths( input_folder, full_input_paths )
    full_export_paths = add_prefix_to_paths( export_folder, relative_input_paths )

    return full_input_paths, full_export_paths

def add_prefix_to_paths( prefix_path, relative_paths ):

    """adds prefix to a list of relaive paths"""

    full_paths = []
    for relative_path in relative_paths:
        full_paths.append( join(prefix_path, relative_path) )

    return full_paths

def remove_prefix_from_paths( prefix_path, full_paths ):

    """Removes prefix from full paths"""

    number_of_dirs = len( path_to_dirs(prefix_path) )

    relative_paths = []
    for full_path in full_paths:

        folder_list = path_to_dirs( full_path )
        relative_list = folder_list[ number_of_dirs : ]

        relative_paths.append( join(*relative_list) )

    return relative_paths

def get_paths_with_common_parent( path ):

    """Returns full paths with common parent path
     Note: does not return empty directories"""

    roots, dirs, files = walk_root_dir( path )
    full_paths = []

    for i in range(len(roots)):
        for file in files[i]:

            full_path = join( roots[i], file )
            full_paths.append( full_path )

    return full_paths

def remove_hanging_slashes( path ):

    """removes ending slashes from paths
    turns "asdf/asdf//" into "asdf/sadf"   """

    # dont go through all the
    for i in range( len(path)-1, -1, -1 ):

        if path[i] != '/':
            return path[:i+1]

    return path

def get_desktop_dir() -> Any:

    """get the location of the desktop"""

    if platform.system() == 'Windows':
        import winshell
        return winshell.desktop()

    return None

def create_shortcut_on_desktop( target_Path: Path ) -> None:

    """places a shortcut to target_Path on the Desktop"""

    desktop_Dir = Dir( get_desktop_dir() )
    create_shortcut( target_Path, desktop_Dir )

def create_shortcut( target_Path: Path, shortcut_Dir: Dir ) -> None:

    """places a shortcut from target_Path to shortcut_Dir"""

    if platform.system() == 'Windows':
        import winshell

        shortcut_Path = Path( shortcut_Dir.join( target_Path.root + '.lnk' ) )
        winshell.CreateShortcut( Path=shortcut_Path.p, Target=target_Path.p )

    else:
        print ('No instructions for current OS')

def get_env_var_path_delim() -> str:

    """Returns the delimitter for the OS's path environment variables"""

    if platform.system() == 'Windows':
        return ';'
    elif platform.system() == 'Linux':
        return ':'

def split_env_var_paths( string: str ) -> List[str]:

    """returns a list of path strings split on the system delimitter"""

    return string.split( get_env_var_path_delim() )

def join_env_var_paths( paths: List[str] ) -> str:

    """ returns 'C:/Path1;C:/Path2' """
    return get_env_var_path_delim().join( paths )





def instance_method(method):

    """instance methods call the corresponding staticmethod 
    Example: Dir_instance.exists(*,**) calls Dir.exists_dir( Dir_instance.path,*,** )   """

    @functools.wraps(method)
    def wrapper( self, *called_args, **called_kwargs):

        new_method_name = method.__name__ + self.STATIC_METHOD_SUFFIX
        return self.get_attr( new_method_name )( self.path, *called_args, **called_kwargs )
        
    return wrapper


class Dir (ParentClass) :

    STATIC_METHOD_SUFFIX = '_dir'

    def __init__ ( self, *args, **kwargs ):

        ParentClass.__init__( self )
        self.dir_construct( *args, **kwargs )

    def __eq__( self, other_Dir ):

        if isinstance( other_Dir, Dir ):
            return self.path == other_Dir.path
        return False

    def dir_construct( self, absolute_path, **kwargs ):

        absolute_path = replace_delims( absolute_path )
        self.path = remove_hanging_slashes( absolute_path )  # 'C:/Users/e150445/Documents/MO-EE/Data/Raw'
        self.dirs = path_to_dirs( self.path )                #[ 'C','Users','e150445','Documents','MO-EE','Data','Raw' ]
        self.type_path = False
        self.type_dir = True

        #alias just for quick coding
        self.p = self.path

    def print_imp_atts( self, print_off = True ):

        return self._print_imp_atts_helper( atts = ['path','dirs'], print_off = print_off )

    def print_one_line_atts(self, print_off = True, leading_string = '\t' ):

        return self._print_one_line_atts_helper( atts = ['type','path'], print_off = print_off, leading_string = leading_string )

    @staticmethod
    def is_Dir( Object: Any ) -> bool:

        """returns boolean if Object is a Dir"""
        return isinstance( Object, Dir )

    def ascend( self, level_to_ascend: int = 1 ) -> Dir :
        
        """go up a x number directories -> "levels_to_ascend" """

        return Dir( join( *self.dirs[:-1*level_to_ascend] ))
    
    @staticmethod
    def ascend_dir( dir: str, levels_to_ascend: int = 1 ) -> str:

        """go up a x number directories -> "levels_to_ascend" """

        dirs = path_to_dirs( dir )
        return join( *dirs[:-1*levels_to_ascend] )

    @instance_method
    def join( self, *args, **kwargs ):
        pass
    
    @staticmethod
    def join_dir( dir: str, *other_dirs, **kwargs ):
        
        """add more dirs to the Dir path"""
        return join( dir, *other_dirs )

    @instance_method
    def open( self, *args, **kwargs ):
        pass
    
    @staticmethod
    def open_dir( dir ):

        """Opens the dir in the file explorer """

        if platform.system() == 'Windows':
            os.startfile(path)

        elif platform.system() == 'Darwin':
            subprocess.call(['open', path])

    @instance_method
    def get_unique_filename( self, *args, **kwargs ):
        pass

    def get_unique_filename_dir( self, filename ):

        if self.type_dir:
            return get_unique_filename( filename, export_dir = self.p )

    @instance_method
    def exists( self, *args, **kwargs ):
        pass

    @staticmethod
    def exists_dir( path: str, **kwargs ) -> bool:
        return os.path.exists( path )

    @instance_method
    def remove(self, *args, **kwargs):
        pass

    @staticmethod
    def remove_dir( dir: str, override: bool = False, print_off: bool = True) -> bool:

        """deletes the entire folder and all contents underneath, returns True is successful"""

        if not override:
            override = input('To delete folder ' + str(dir) + ' type "delete" :') == 'delete'

        if override:
            if print_off:
                print ('Deleting folder ' + str(dir) + '...')

            try:
                shutil.rmtree(dir)
            except:
                print ('Could not delete folder ' + str(dir))
                return False

            return True

    def create(self, *args, **kwargs) -> bool:

        """creates a directory at dir"""

        if not self.exists():
            self.create_parents()
            try:
                os.mkdir( self.path )
            except:
                return False
            return True
        return False

    def create_parents(self):

        """use recursion to travel all the way up the parent directories until we find one that exists, then unfold and create each directory"""

        parent_Dir = self.ascend()
        if parent_Dir.exists() or len(self.dirs) <= 1: #Parent Dir exists or we are at the base directory
            return

        else:
            parent_Dir.create_parents()
            parent_Dir.create()

    @instance_method
    def copy(self, *args, **kwargs):
        pass

    @staticmethod
    def copy_dir( source_dir: str, destination_Dir = None, destination_dir: str = '', print_off: bool = True ) -> bool:

        """copies an entire tree of files from source to destination"""

        if destination_Dir != None:
            destination_dir = destination_Dir.path

        if print_off:
            print ('Copy Location: ' + source_dir)
            print ('Paste Location: ' + destination_dir)
            print ('copying Tree...')

        try:
            shutil.copytree( source_dir, destination_dir )
        except:
            return False
        return True

    @instance_method
    def list_contents( self, *args, **kwargs ):
        pass

    @staticmethod
    def list_contents_dir( dir: str ) -> List[str]:

        """returns all directories and files contained in dir""" 
        return os.listdir( dir )

    def list_contents_Paths( self, block_dirs: bool = True, block_paths: bool = False ) -> Paths: 

        """returns all first sublevel contents of Directory as a Paths instance"""

        filenames = self.list_contents() # a list of filenames and directories
        Paths_inst = Paths()

        for filename in filenames:
            path = self.join( filename )

            if is_dir( path ):
                if not block_dirs:
                    Paths_inst._add( Dir( path ) )

            else:
                if not block_paths:
                    Paths_inst._add( Path( path ))
            
        return Paths_inst

    def walk_contents_Paths( self, block_dirs: bool = True, block_paths: bool = False, folders_to_skip: List[str] = [] ) -> Paths:

        """get all Paths and/or Dirs underneath the entire directory, optional params for returning paths and/or dirs"""

        Paths_inst = Paths()
        subfolders = get_subfolders_under_parent( dir, folders_to_skip = folders_to_skip )
        for subfolder in subfolders:
            Paths_under_subfolder = list_contents_Paths( subfolder, block_dirs = block_dirs, block_paths = block_paths )

            for Path_under_subfolder in Paths_under_subfolder:
                if not is_dir(Path_under_subfolder.p) and Path_under_subfolder.dirs[-1] not in folders_to_skip:
                    Paths.append( Path_under_subfolder )

        return Paths

    def get_child_Dirs( self, folders_to_skip: List[str] = ['.git'] ) -> Dirs:
                
        child_Dirs = Dirs()
        child_Dirs._add( self )

        Dirs_under = self.list_contents_Paths( block_dirs = False, block_paths = True )
        for Dir_inst in Dirs_under:
            if Dir_inst.dirs[-1] not in folders_to_skip:
                
                child_Dirs.merge( Dir_inst.get_child_Dirs( folders_to_skip = folders_to_skip ) )

        return child_Dirs

    def get_unique_Path( self, filename: str ) -> str:

        """finds a unique Path for the proposed filename based on the contents of the Directory
        if file.txt already exists in the dir, return file1.txt or file2.txt, etc  """

        Paths_in_Dir = self.list_contents_Paths( block_dirs=True, block_paths=False )
        filenames = [ P.filename for P in Paths_in_Dir ]

        if filename not in filenames:
            return Path( self.join(filename) )

        filename_Path = Path( filename )
        counter = 0

        while True:
            proposed_filename = filename_Path.root + str(counter) + filename_Path.extension
            if proposed_filename not in filenames:
                return Path( self.join(proposed_filename) )

            counter += 1

class Path( Dir ):

    """
    Inherits from the Dir class found in Dir.py
    absolute_path example: C:/Users/e150445/Documents/MO-EE/Data/Raw/experian.parquet
    Path (uppercase P) is a Path class, path (lowercase P) is a string with file absolute path
    """

    STATIC_METHOD_SUFFIX = '_path'

    def __init__( self, absolute_path ):

        self.path_construct(absolute_path)

    def path_construct(self, absolute_path):

        """Since the Path is different from a Dir, add the extra attiributes"""

        Dir.__init__( self, absolute_path )
        self.filename =     Path.get_filename( self.path )                  # feb_mar_v1.0.txt
        self.root =         Path.get_root( self.path )                      # feb_mar_v1
        self.root_dots =    Path.get_root( self.path, allow_dots=True )     # feb_mar_v1.0
        self.ending =       Path.get_ending( self.path )                    # txt
        self.extension =    '.' + self.ending                               # .txt
        self.size = None                          # don't init with checking the size, takes too long
        self.size_units = None
        self.mtime = None                        # a datetime object when its ready

        self.parent_Dir = self.ascend()
        self.type_path = True
        self.type_dir = False

    def __eq__( self, other_Path: Path ) -> bool:

        """checks if self is equal to other_Path, returns bool"""

        if isinstance( other_Path, Path ):
            return self.path == other_Path.path
        return False

    @staticmethod
    def is_Path( Object: Any ) -> bool:

        """returns boolean if Object is a Dir"""
        return isinstance( Object, Path )

    def print_imp_atts(self, print_off = True):

        return self._print_imp_atts_helper( atts = ['path','dirs','ending','size'], print_off = print_off )

    @instance_method
    def exists( self, *args, **kwargs ):
        pass

    @staticmethod
    def exists_path( path: str, **kwargs ) -> bool:
        return os.path.exists( path )

    @instance_method
    def copy( self, *args, **kwargs ):
        pass
    
    @staticmethod
    def copy_path( source_path: str, destination_Path = None, destination_path: str = '', print_off: bool = True ) -> bool:

        """copies an the contents from source to destination"""

        if destination_Path != None:
            destination_path = destination_Path.path

        if print_off:
            print ('Copy Location: ' + source_path)
            print ('Paste Location: ' + destination_path)
            print ('copying file...')

        if Path.exists_path(source_path) and not Path.exists_path(destination_path):
            try:
                shutil.copyfile(source_path, destination_path)
            except:
                return False
            return True

        else:        
            return False

    @instance_method
    def remove( self, *args, **kwargs ):
        pass

    @staticmethod
    def remove_path(path: str, override: bool = False, print_off: bool = True) -> bool:

        """deletes file at path: BE CAREFUL"""

        inp = 'delete'
        if not override:
            inp = input('Type "delete" to delete ' + str(path) + ': ')

        if inp == 'delete':
            if path_exists(path):
                if print_off:
                    print ('Deleting file ' + str(path))
                try:
                    os.remove(path)
                except:
                    return False
                return True
        return False

    @instance_method
    def rename( self, *args, **kwargs):
        pass
    
    @staticmethod
    def rename_path( path, new_Path = None, new_path = '', print_off = False ):

        """renames the file using string new_path or object new_Path
        Give option to overwrite Class instance with new path"""

        if new_Path != None:
            new_path = new_Path.path

        if Path.exists_path( path ) and not Path.exists_path( new_path ):
            if print_off:
                print ('Renaming ' + path + ' to ' + new_path )

            try:
                os.rename(path, new_path)
            except:
                return False
            return True

        else:
            return False

    @instance_method
    def get_size( self, *args, **kwargs ):
        pass

    @staticmethod
    def get_size_path( path, **kwargs ) -> None:

        """get the size of the path"""

        size = os.stat( path ).st_size
        converted_size, conversion = convert_bytes( size, **kwargs )

        self.size = converted_size
        self.size_units = conversion


    @instance_method
    def get_mtime( self, *args, **kwargs ):
        pass

    @staticmethod
    def get_mtime_path( path ):

        """get the time of modification as a datetime object"""
        mtime = pathlib.Path(self.p).stat().st_mtime
        self.mtime = datetime.datetime.fromtimestamp( mtime )
        return self.mtime

    @instance_method
    def write( self, *args, **kwargs):
        pass
       
    @staticmethod
    def write_path( path, **kwargs ):
        
        """writes to a text file at path, read py_starter.write_text_file() for kwargs """
        ps.write_text_file( path, **kwargs )

    @instance_method
    def create( self, *args, **kwargs ):
        pass
    
    @staticmethod
    def create_path( path, string = '', **kwargs ):

        """initialize the contents of the path"""
        Path.write_path( path, string = string, **kwargs )

    @instance_method
    def read( self, *args, **kwargs):
        pass
    
    @staticmethod
    def read_path( path, **kwargs ):

        """reads from a text file at path, read py_starter.read_text_file() for kwargs """
        return ps.read_text_file( path, **kwargs )

    @instance_method
    def import_module( self, *args, **kwargs):
        pass
    
    @staticmethod
    def import_module_path( path, *args, **kwargs ):

        """imports the contents of path as a module"""
        return ps.import_module_from_path( path, **kwargs )
    
    @staticmethod
    def get_filename( path: str ) -> str:

        """returns the filename ('file.txt') from a long path ('C:/path/to/file.txt') """

        dirs = path_to_dirs(path)
        return dirs[-1]
    
    @staticmethod
    def get_root( path: str, allow_dots: bool = False ) -> str:

        '''returns the root of the filename from a path  Dir/a_file1.txt returns "a_file1" '''
        filename = Path.get_filename(path)

        if allow_dots:
            root = '.'.join( filename.split('.')[:-1] )

        else:
            root = filename.split('.')[0]
        
        return root
    
    @staticmethod
    def get_ending( path: str ) -> str:

        '''returns the file ending from a path'''
        
        filename = Path.get_filename(path)
        ending = filename.split('.')[-1]
        return ending



class Dirs(ParentClass):

    def __init__ ( self, Dirs = [], dirs = [] ):

        ParentClass.__init__( self )

        self.Dirs = []
        self.Objs = self.Dirs # Make an Alias

        for D in Dirs:
            self._add( D )
        for d in dirs:
            self._add( Dir( d ) )

    @staticmethod
    def is_Dirs( Object: Any ) -> bool:

        """returns boolean if Object is a Dir"""
        return isinstance( Object, Dirs )

    def __len__( self ):

        return len( self.Objs )

    def __iter__( self ):

        self.i = -1
        return self

    def __next__( self ):

        self.i += 1

        if self.i < len(self):
            return self.Objs[self.i]
        else:
            raise StopIteration

    def __contains__( self, Obj_to_check: Any ) -> bool:

        """returns the boolean value for Dir/Path Obj being contained in the list of Objects"""

        for Obj in self:
            if Obj == Obj_to_check:
                return True
        return False

    def _add( self, new_Obj: Any ) -> None:

        """add a new Object to the list of Objects"""

        self.Objs.append( new_Obj )

    def print_imp_atts( self, print_off = True ):

        string = self._print_imp_atts_helper( print_off = False ) + '\n'
        string += 'Dirs:\n'

        for D in self:
            string += D.print_one_line_atts( print_off = False ) + '\n'

        string = string [:-1]
        return self.print_string( string, print_off = print_off )

    def print_one_line_atts(self, print_off = True, leading_string = '\t' ):

        self.len_Dirs = len(self)
        return self._print_one_line_atts_helper( atts = ['type','len_Dirs'], print_off = print_off, leading_string = leading_string )

    def merge( self, other_Dirs: Any ):

        """add all Dir objects from another Dirs instance to self"""

        for Dir_inst in other_Dirs:
            self._add( Dir_inst )

    def export_strings( self ) -> List[str]:

        """Returns all the paths of each Dir/Path contained"""

        return [ O.path for O in self ]


class Paths( Dirs ):

    def __init__ ( self, Paths = [], paths = [] ):

        ParentClass.__init__( self )

        self.Paths = []
        self.Objs = self.Paths # Make an Alias

        for P in Paths:
            self._add( P )
        for p in paths:
            self._add( Path( p ) )

    @staticmethod
    def is_Paths( Object: Any ) -> bool:

        """returns boolean if Object is a Dir"""
        return isinstance( Object, Paths )

    def print_imp_atts( self, print_off = True ):

        string = self._print_imp_atts_helper( print_off = False ) + '\n'
        string += 'Paths:\n'

        for P in self:
            string += P.print_one_line_atts( print_off = False ) + '\n'

        string = string [:-1]
        return self.print_string( string, print_off = print_off )

    def print_one_line_atts(self, print_off = True, leading_string = '\t' ):

        self.len_Paths = len(self)
        return self._print_one_line_atts_helper( atts = ['type','len_Paths'], print_off = print_off, leading_string = leading_string )

