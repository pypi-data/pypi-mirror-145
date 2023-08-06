# DEMURE_CAPTCHA
Simple liight-weight package for generate image and auidio captcha

# SUMMARY
#### Install
```shell
python3 -m pip install demure_captcha
```
#### Console
```shell
python3 -m demure_captcha --length 10 --useIntegers True --width 300 --height 300 --format file
# Created files with audio and video
>>> %AppData%\Local\Temp\0c7e4ddf-885b-4651-905e-b7efd758fc8d.png
>>> %AppData%\Local\Temp\0c7e4ddf-885b-4651-905e-b7efd758fc8d.mp3

python3 -m demure_captcha --length 10 --useIntegers True --width 300 --height 300 --format json
# Base64 strings
>>>{ "mp3": "rewwgwrrrwggrwrg...", "png": "wfweewggewegwg..." }
```
#### Pakage
```python
from demure_captcha import generate

captcha = generate( width=300, height=300 )

captcha.image.show( )
print( captcha.save( ) )
print( captcha.save( 'tmp/captcha' ) )
```
# Example captcha
![mp3](example-captcha.mp3)
![png](example-captcha.png)
