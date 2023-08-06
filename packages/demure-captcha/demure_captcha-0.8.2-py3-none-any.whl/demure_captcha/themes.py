from random import choice as random_choice
from pip    import List
from typing import Tuple, TypedDict, List, Dict


class Theme( TypedDict ):
    colors : List[str]
    font   : Tuple[ str, str ] 


THEMES: Dict[ str, Theme ]= dict(
    spring    = { 'colors': [ '#d72631', '#a2d5c6', '#077b8a', '#5c3c92' ], 'font' : ( 'butler'      , 'bold'           ) },
    pom       = { 'colors': [ '#e2d810', '#d9138a', '#12a4d9', '#322e2f' ], 'font' : ( 'butler'      , 'light_stencil'  ) },
    masala    = { 'colors': [ '#cf1578', '#e8d21d', '#039fbe', '#b20238' ], 'font' : ( 'butler'      , 'extra_bold'     ) },
    cocao     = { 'colors': [ '#e75874', '#be1558', '#fbcbc9', '#322514' ], 'font' : ( 'butler'      , 'thin'           ) },
    casual    = { 'colors': [ '#316879', '#f47a60', '#7fe7dc', '#ced7d8' ], 'font' : ( 'butler'      , 'medium'         ) },
    romantic  = { 'colors': [ '#d902ee', '#ffd79d', '#f162ff', '#320d3e' ], 'font' : ( 'Roboto Serif', 'regular'        ) },
    beach     = { 'colors': [ '#ffcce7', '#daf2dc', '#81b7d2', '#4d5198' ], 'font' : ( 'Roboto Serif', 'medium'         ) },
    pop       = { 'colors': [ '#d71b3b', '#e8d71e', '#16acea', '#4203c9' ], 'font' : ( 'Roboto Serif', 'light'          ) },
)


def random( ) -> Theme:
    return random_choice( [ v for _, v in THEMES.items( ) ] )

def get( name: str ) -> Theme:
    theme = THEMES.get( name, None )

    if theme is None:
        raise Exception( f"Theme '{theme}' not found" )
    else:
        return theme