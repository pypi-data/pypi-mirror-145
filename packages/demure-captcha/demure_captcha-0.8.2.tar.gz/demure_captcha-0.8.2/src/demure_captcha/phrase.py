import random
import string


def generate( length: int=5, onlyLower: bool=True, useIntegers: bool=True ) -> str:
    if length < 1:
        raise Exception("length must be bigger than 0" )

    choice  = [ [ x for x in string.ascii_lowercase if x != 'o' ] ]

    if not onlyLower:
        choice.append(  [ x for x in string.ascii_uppercase if x != 'O' ] )

    if useIntegers:
        choice.append( [ x for x in range( 0,9 ) ] ) 

    chars = [ 
        str( random.choice( random.choice( choice ) ) )
        for _ in range( 0, length ) 
    ]

    return "".join( chars )
