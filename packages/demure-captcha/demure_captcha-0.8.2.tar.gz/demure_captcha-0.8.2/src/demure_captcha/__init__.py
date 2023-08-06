import sys
import pathlib

sys.path.append( str( pathlib.Path( __file__ ).parent ) )

import themes

from captcha import Captcha, generate, CaptchaIn, CaptchaOut