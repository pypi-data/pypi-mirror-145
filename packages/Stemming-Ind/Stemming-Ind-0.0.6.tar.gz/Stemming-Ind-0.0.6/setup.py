from setuptools import setup, find_packages


setup(
    name='Stemming-Ind',
    version='0.0.6',
    license='MIT',
    author="Hangsbreaker",
    author_email='hangbreaker@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/hangsbreaker/stemming-ind',
    keywords='Stemming Bahasa Indonesia',
    install_requires=['re'],
)
