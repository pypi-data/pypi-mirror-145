from setuptools import setup, find_packages


setup(
    name='dag auto gen',
    version='0.1',
    license='None',
    author="Rony",
    author_email='email@example.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='',
    keywords='dag auto gen',
    install_requires=[
          'jinja2', 'yaml', 'json' , 'logging'
      ],

)