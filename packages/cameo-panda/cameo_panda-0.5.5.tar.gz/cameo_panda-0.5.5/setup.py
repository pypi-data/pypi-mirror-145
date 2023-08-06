from setuptools import setup

setup(
    name='cameo_panda',
    version='0.5.5',
    description='This is a cameo_panda note️',
    url='https://github.com/panda19931217/cameo_panda',
    author='Bowen Chiu',
    author_email='panda19931217@gmail.com',
    license='BSD 2-clause',
    packages=['cameo_panda'],
    install_requires=[
        'requests',
        'polars',
        'pyyaml',
        'tqdm'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)

