from glob    import glob
from os      import path as os_path
from pathlib import Path
from random  import randint, choice as random_choice
from PIL     import ImageFont


FONTS_ROOT  = str( Path( __file__ ).parent )
FONTS_FILES = glob( os_path.join( FONTS_ROOT, '*', '*.ttf' ) ) + glob( os_path.join( FONTS_ROOT, '*', '*.otf' ) )
FONTS       = { 
    Path( f ).name.split( '.' )[0] : f
    for f in FONTS_FILES
}  

def new( name: str, style: str='', size: int=10 ):
    path = [ name ]

    if len( style ) > 0:
        path.append( style )
    
    path   = "-".join( path )
    exists = FONTS.get( path, None ) 

    if exists:
        return ImageFont.truetype( exists, size )
    else:
        raise Exception( f"Could not find font '{path}'" )

def random( size: int=randint( 10, 20 ) ):
    return ImageFont.truetype( random_choice( [ v for _, v in FONTS.items( ) ] ), size ) 