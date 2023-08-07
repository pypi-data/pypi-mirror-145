from setuptools import setup, find_packages
from dictcopy import __version__


long_desc = ""
with open('./README.md') as fl:
    long_desc = fl.read()

setup(
    name='dictcopy',
    packages=find_packages(
        include=["dictcopy", "dictcopy.*"]
    ),
    version=__version__,
    license='MIT',
    description='Dict copy',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    author='Jeff Aguilar',
    author_email='jeff.aguilar.06@gmail.com',
    keywords=['dict', 'copy', 'clone'],
    install_requires=[
        'Werkzeug',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    include_package_data=True,
    python_requires='>=3.6'
)
