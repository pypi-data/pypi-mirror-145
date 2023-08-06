import random
import fonts

from PIL    import Image, ImageDraw, ImageFont, ImageFilter
from typing import Tuple


class Char:
    def __init__( self, char: str, width: int=100, height: int=100, color: str='black', bg: str='white', font: ImageFont=None ):
        self.char     = char
        self.width    = width
        self.height   = height
        self.color    = color
        self._font    = font
        self.bg       = bg
        self._filter  = None
        self.font     = fonts.random( round( self.height * 0.9 ) ) if font is None else font

        if len( char ) > 1:
            raise Exception( "Too many characters, must be 1" )
    
    def filter( self, filter: ImageFilter ):
        self._filter = filter

        return self
    
    @property
    def top( self ) -> int:
        _, h = self.font.getsize( self.char )

        return round( ( self.height * 0.5 ) - ( h * 0.6 ) )
    
    @property
    def left( self ) -> int:
        w, _ = self.font.getsize( self.char )

        return round( ( self.width - w ) / 2 )

    @property
    def position( self ) -> Tuple[int, int]:
        return ( self.left, self.top )
    
    @property
    def blank( self ) -> Image:
        return Image.new( 'RGBA', ( self.width, self.height ), self.bg )
    
    @property
    def image( self ) -> Image:
        blank = self.blank
        draw  = ImageDraw.Draw( blank )

        draw.text( self.position, self.char, fill=self.color, font=self.font )

        if self._filter:
            blank.filter( self._filter )
        
        return blank
    
    def random_distortion( self, percent: int=random.randint( 0, 90 ) ) -> Image:
        blank    = self.image
        draw     = ImageDraw.Draw( blank )
        store    = { }
        poitsize = ( self.width * self.height )
        limit    = ( poitsize / 100 ) * percent

        while limit > 0:
            x   = random.randint( 0, self.width  )
            y   = random.randint( 0, self.height )
            key = f"{x}-{y}"

            if store.get( key, None ) is None:
                store[key] = True
                
                draw.point( ( x, y ), fill=self.bg )

                limit -= 1

        return blank