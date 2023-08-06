import sys
import pathlib

sys.path.append( str( pathlib.Path( __file__ ).parent ) )

import argparse
import uuid
import json
import tempfile

from os          import path as os_path
from captcha import Captcha, generate
from themes  import THEMES
from typing      import Literal


parser = argparse.ArgumentParser( description='Captcha generator' )

parser.add_argument( '--word'       , type=str,  help='word for captcha'                    , required=False )
parser.add_argument( '--length'     , type=int,  help='length of random word'               , required=False )
parser.add_argument( '--onlyLower'  , type=bool, help='use only lowwer chars in random word', required=False )
parser.add_argument( '--useIntegers', type=bool, help='use integers in random word'         , required=False )
parser.add_argument( '--width'      , type=int,  help='image width'                         , required=False )
parser.add_argument( '--height'     , type=int,  help='image height'                        , required=False )
parser.add_argument( '--theme'      , type=str,  help='name of theme'                       , required=False )
parser.add_argument( '--format'     , type=str,  help=Literal[ 'json', 'file' ]                              )


params = { k: v for k,v in vars( parser.parse_args( ) ).items( ) if not v is None }

if params.get( 'theme', None ):
    params['theme'] = THEMES[ params.get( 'theme' ) ]

captcha = generate( **params )

if params.get( 'format', None ) == 'json':
    print( json.dumps( captcha.as_object( ).__dict__ ) )
else:
    path = os_path.join( tempfile.gettempdir(), str( uuid.uuid4( ) ) )

    for _path in captcha.save( path ):
        print( _path )