import setuptools
from docconverter import __version__

setuptools.setup(
    name='CoDocConverter',
    version=__version__,
    # package_dir={'': 'docconverter'},  # Our packages live under src but src is not a package itself
    packages=setuptools.find_packages("."),  # I also tried exclude=["src/test"]
    url='https://www.cityocean.com',
    license='GPL',
    author='CityOcean',
    author_email='it@cityocean.com',
    description='文档转换器',
    keywords=['document', 'convert'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
    install_requires=[
        'pdfminer'
    ],
)
