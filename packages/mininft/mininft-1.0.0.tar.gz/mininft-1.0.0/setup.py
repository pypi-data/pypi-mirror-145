from distutils.core import setup


VERSION = '1.0.0'

setup(name='mininft',
      version='1.0.0',
      description='Mini nft transfer helper',
      author='dave',
      author_email='dave@endlesstruction.com.ar',
      url='https://example.com/mininft',
      py_modules=['mininft'],
      install_requires=[
          'Click',
      ],
      entry_points={
          'console_scripts': [
              'mininft = mininft:cli',
          ],
      })
