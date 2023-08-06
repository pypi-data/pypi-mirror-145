import json
import os.path
import shutil
import sys

import setuptools

if 'sdist' in sys.argv:
    STATIC_PATH = os.path.join(os.path.dirname(__file__), 'MelodieStudio', 'static')
    # copy your Melodie Studio webpage dist path here
    with open('webpage-config.json') as f:
        web_dist_path = json.load(f)['dist-path']
        shutil.rmtree(STATIC_PATH)
        shutil.copytree(web_dist_path, STATIC_PATH)
setuptools.setup(
    name='MelodieStudio',
    version='0.2.0',
    description='A web-based toolbox for Melodie package.',
    long_description='',
    long_description_content_type='text/markdown',
    url='https://github.com/SongminYu/Melodie',
    author='Songmin Yu',
    author_email='songmin.yu@isi.fraunhofer.de',
    license='BSD 3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.6',
        # 'Programming Language :: Python :: 3.7',
        # 'Programming Language :: Python :: 3.8',
        # 'Programming Language :: Python :: 3.9',
        # 'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    project_urls={
        'Documentation': 'https://Melodie.readthedocs.io/en/latest/index.html',
    },
    packages=setuptools.find_namespace_packages(
        include=['MelodieStudio', 'MelodieStudio.*']
    ),
    install_requires=[
        'chardet',
        'websockets',
        'sqlalchemy',
        'flask',
        'flask_cors',
        'astunparse',
        'pprintast'
    ],
    python_requires='>=3.5',
    entry_points={
        'console_scripts': [
            'Melodie=Melodie.scripts.scripts:cli'
        ]
    },
    include_package_data=True,
)
