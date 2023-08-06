import random as py_random
import base64
import tempfile
import uuid
import fonts
import phrase


from io       import BytesIO
from themes   import Theme, THEMES, random as random_theme
from pip      import List
from PIL      import Image
from char     import Char
from os       import path as os_path
from pathlib  import Path
from speaker  import Speaker
from pydantic import BaseModel
from typing   import Optional, Tuple


class CaptchaOut( BaseModel ):
    mp3 : str
    png : str


class CaptchaIn( BaseModel ):
    length      : Optional[int]   = 5
    onlyLower   : Optional[bool]  = True
    useIntegers : Optional[bool]  = True 
    width       : Optional[int]   = 300
    height      : Optional[int]   = 300 
    theme       : Optional[Theme] = THEMES['masala']
    word        : Optional[str]   = None


class Captcha:
    def __init__( self, words: List[str]|str, width: int=None, height: int=100, font_size: int = None, theme: Theme=random_theme( ), bg: str='rgba( 255, 255, 255, 0 )' ):
        self.words      = " ".join( words ) if isinstance( words, list ) else words
        self._theme     = theme
        self._width     = width
        self._height    = height
        self._font_size = font_size
        self.bg         = bg

        if len( self.words ) == 0:
            raise Exception( "Word can't be null" )

    @property
    def font_size( self ) -> int:
        if self._font_size is None:
            if self._width:
                self._font_size = ( self._width / len( self.words ) ) * 0.9
            else:
                self._font_size = 100
        
        return self._font_size
    
    @property
    def width( self ) -> int:
        if self._width is None:
            self._width = len( self.words ) * self.font_size
        
        return self._width
    
    @property
    def blank( self ) -> Image:
        return Image.new( 'RGBA', ( self.width, self._height ), self.bg )

    @property
    def image( self ) -> Image:
        blank = self.blank
        pos   = 0
        width = round( self.width / len( self.words ) )
        theme = self._theme

        for idx, symbal in enumerate( self.words ):
            color = py_random.choice( theme['colors'] )
            fs    = py_random.randint( round( self.font_size * 0.7 ), round( self.font_size * 1.5 ) )
            font  = fonts.new( *theme['font'], fs )
            char  = Char( symbal, width, self._height, color, self.bg, font  )
            _pos  = pos
            im    = char.random_distortion( py_random.randint( 0, 70 ) ).rotate( py_random.randint( -40, 45 ) )

            if idx > 0:
                _pos = py_random.randint( round( pos * 0.9 ), pos )
            
            blank.paste( im, ( _pos, 0 ), im )

            pos   += width
        
        return blank

    def image_as_base64( self ) -> str:
        buff = BytesIO()

        self.image.save( buff, format="png" )

        return base64.b64encode( buff.getvalue( ) )
    
    def save_sound( self, _path: str ) :
        Speaker( py_random.randint( 40, 70 ) ).say( self.words, _path )

    def sound_as_base64( self ):
        _path = os_path.join( tempfile.gettempdir(), str( uuid.uuid4( ) ) + '.mp3' )

        Speaker( py_random.randint( 40, 70 ) ).say( self.words, _path )

        with open( _path, 'rb' ) as f:
            content = base64.b64encode( BytesIO( f.read( ) ).getvalue() )

        Path( _path ).unlink( )

        return content

    def save_image( self, path: str ):
        self.image.save( path )

    def save( self, path=os_path.join( tempfile.gettempdir(), str( uuid.uuid4( ) ) ) ) -> Tuple[ str, str ]:
        image_path = path + '.png'
        mp3_path   = path + '.mp3'
        
        self.save_sound( mp3_path   )
        self.save_image( image_path )

        return image_path, mp3_path 
    
    def as_object( self ) -> CaptchaOut:
        return CaptchaOut( mp3=self.sound_as_base64( ), png=self.image_as_base64( ) )


def generate( **kwargs: CaptchaIn ) -> Captcha:
    params      = CaptchaIn( **kwargs )
    params.word = phrase.generate( params.length, params.onlyLower, params.useIntegers ) if params.word is None else params.word

    return Captcha( params.word, params.width, params.height, theme=params.theme )