from distutils.core import setup, Extension

module1 = Extension('cfunctions',
					libraries=['rt'],
                    sources = ['functions.c'])

setup (name = 'CFunctions',
       version = '1.0',
       description = 'Funciones de C para los modulos de Python',
       ext_modules = [module1])
