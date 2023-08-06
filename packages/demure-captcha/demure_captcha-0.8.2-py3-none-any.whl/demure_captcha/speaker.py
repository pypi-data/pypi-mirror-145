import re
import pyttsx3


class Speaker:
    def __init__( self, rate: int=60 ):
        self._synthesizer = pyttsx3.init( )
        
        self._synthesizer.setProperty( 'voice', self.voice )  
        self._synthesizer.setProperty( 'rate', rate        )

    @property
    def rate( self ) -> int:
        return self._synthesizer.getProperty( 'rate' )

    @rate.setter
    def rate( self, rate: int ):
        self._synthesizer.setProperty( 'rate', rate )


    @property
    def voice( self ) -> str:
        voices = self._synthesizer.getProperty( 'voices' )

        for _voice in voices: 
            if re.findall( r'English', _voice.name ):
                return _voice.id
        
        raise Exception( "Can't find English language for voice" )
    
    def say( self, phrase: str, save: str=None ):
        if save:
            self._synthesizer.save_to_file( phrase, save )
        else:
            self._synthesizer.say( phrase ) 

        self._synthesizer.runAndWait( ) 

        self._synthesizer.stop( )
