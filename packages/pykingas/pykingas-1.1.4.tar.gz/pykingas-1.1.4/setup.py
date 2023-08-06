from setuptools import setup
from pathlib import Path

this_dir = Path(__file__).parent
readme = (this_dir / 'README.md').read_text()
setup(
    name='pykingas',
    version='1.1.4',
    packages=['pykingas'],
    package_data={'pykingas': ['KineticGas.*']},
    description='Revised Enskog solutions of the Boltzmann Equations '
                'for diffusion, thermal diffusion and thermal conductivity.',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Vegard Gjeldvik Jervell',
    author_email='vegard.g.j@icloud.com',
    url='https://github.com/vegardjervell/Kineticgas',
    install_requires=['numpy>=1.22.1',
                      'scipy>=1.7.3']
)