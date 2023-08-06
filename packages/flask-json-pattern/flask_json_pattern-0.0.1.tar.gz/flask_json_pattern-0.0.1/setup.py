from setuptools import setup, find_packages
from flask_json_pattern import __version__

long_desc = ""
with open('./README.md') as fl:
    long_desc = fl.read()

setup(
    name='flask_json_pattern',
    packages=find_packages(
        include=["flask_json_pattern", "flask_json_pattern.*"]
    ),
    version=__version__,
    license='MIT',
    description='',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    author='Jeff Aguilar',
    author_email='jeff.aguilar.06@gmail.com',
    url='https://github.com/jeffaguilar08/flask-json-pattern',
    download_url='https://github.com/jeffaguilar08/flask-json-pattern.git',
    keywords=['flask', 'json', 'schema'],
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
    include_package_data=True
)
