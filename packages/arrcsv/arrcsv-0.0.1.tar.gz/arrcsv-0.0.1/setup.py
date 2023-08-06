import setuptools

setuptools.setup(
    name='arrcsv',
    version='0.0.1',
    description='A python package for converting array to csv',
    keywords = ['python', 'convert', 'array', 'csv'],
    author='Abdulla Malik',
    author_email='hi@abdulla.dev',
    url='https://github.com/saularis/arrcsv',
    download_url='https://github.com/saularis/arrcsv/archive/refs/tags/v0.0.1.tar.gz',
    install_requires=['numpy'],
    packages=setuptools.find_packages(),
    package_dir={'arrcsv': 'arrcsv'},
)