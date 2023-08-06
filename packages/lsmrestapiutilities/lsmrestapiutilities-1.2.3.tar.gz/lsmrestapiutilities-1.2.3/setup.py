from setuptools import setup, find_packages


setup(
    name='lsmrestapiutilities',
    version='1.2.3',
    license='MIT',
    author="Jack Fink",
    author_email='jackfink68@yahoo.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/bugg86/LSM-REST-API-Utilities',
    keywords='lsm rest api utilities',
    install_requires=[
          'requests',
          'riotapiutilities'
      ],

)