import glob
import setuptools

with open( "README.md", "r", encoding="utf-8" ) as fh:
    long_description = fh.read( )

with open( "requirements.txt", "r", encoding="utf-8" ) as fh:
    install_requires = [ x.replace( "==", ">=" ).strip( ) for x in fh.readlines( ) ]

packages = setuptools.find_packages(where='./src')

print( 'fonts', glob.glob( './src/*/fonts/files/*.otf' ) )
setuptools.setup(
    name                         = "demure_captcha",
    version                      = "0.8.2",
    author                       = "Trishkin Sergey",
    author_email                 = "grdvsng@gmail.com",
    description                  = "Simple but customize captcha generator( image + voice )",
    long_description             = long_description,
    long_description_content_type= "text/markdown",
    url                          = "https://github.com/grdvsng/demure_captcha",
    project_urls                 = { },
    classifiers                  = [
        'Programming Language :: Python :: 3.8',
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    ],
    data_files                   = [ ( 'fonts/files', glob.glob( './src/*/fonts/files/*.otf' ) ) ],
        include_package_data=True,
    install_requires             = install_requires,
    package_dir                  = { "": "src" },
    packages                     = packages,
    python_requires              = ">=3.8",
)