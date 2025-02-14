from setuptools import setup, find_packages

setup(
    name='LogseqMdPy',
    version='0.1.0',
    author='Jonathan Wolf',
    # author_email='your.email@example.com',
    description='A Python library for handling logseq functionalities',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/wolfj123/LogseqMdPy.git',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'networkx',
    ],
)