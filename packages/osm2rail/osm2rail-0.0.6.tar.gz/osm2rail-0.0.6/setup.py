# python setup.py sdist
# python setup.py bdist_wheel
# twine upload dist/*0.1.7*

import setuptools

setuptools.setup(
    name='osm2rail',
    version='0.0.6',
    author='Jiawei Lu, Qian Fu, Zanyang Cui, Dr.Junhua Chen',
    author_email='jiaweil9@asu.edu, q.fu@bham.ac.uk, zanyangcui@outlook.com, cjh@bjtu.edu.cn',
    url='https://github.com/PariseC/osm2rail',
    description='An open-source education tool for constructing modeling datasets of railway transportation',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license='Apache License 2.0',
    packages=['osm2rail'],
    include_package_data=True,
    python_requires=">=3.6.0",
    install_requires=[
        'bs4',
        'matplotlib',
        'osmium',
        'fuzzywuzzy',
        'shapely',
        'pandas',
        'numpy',
        'requests',
    ],
    classifiers=['License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python :: 3']
)
