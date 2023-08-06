import os
from setuptools import setup, find_packages

NAME = 'sphere_temp_conversion'

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

# Load the package's __version__.py module as a dictionary.
here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, NAME, '__version__.py')) as f:
    exec(f.read(), about)


setup_args = dict(
    name=NAME,
    version=about['__version__'],
    description='Unofficial package to convert sample temperatures and setpoints for the Sphere Energy ASC-T - All-solid-state battery testing device. Not affiliated with Sphere Energy.',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='GNU',
    packages=find_packages(),
    author='Thomas Vranken',
    author_email='thvranken@gmail.com',
    keywords=['Sphere Energy', 'Temperature conversion', 'ASC-T'],
    url='https://github.com/thvranken/sphere_temp_conversion',
    download_url='https://pypi.org/project/sphere-temp-conversion/',
)

install_requires = [

]

if __name__ == '__main__':
    setup(**setup_args,
          install_requires=install_requires,
          include_package_data=True,
          )