import setuptools

from cap import __version__

setuptools.setup(
    name='CoCap',
    version=__version__,
    packages=setuptools.find_packages("."),  # I also tried exclude=["src/test"]
    url='https://www.cityocean.com',
    license='GPL',
    author='CityOcean',
    author_email='it@cityocean.com',
    description='CAP',
    keywords=['rabbitmq', 'cap'],
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
    ],
)
