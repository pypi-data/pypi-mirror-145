from setuptools import setup, find_packages


def get_requirements():
    with open('requirements.txt', 'r') as f:
        return f.read().splitlines()


def get_long_description():
    with open('README.md', 'r') as f:
        return f.read()


version_file = 'luffy/version.py'


def get_version():
    with open(version_file, 'r') as f:
        exec(compile(f.read(), version_file, 'exec'))
    return locals()['__version__']


setup(
    name='luffy',
    version=get_version(),
    packages=find_packages(),
    url='https://github.com/Fei-Wang/dl-pytorch',
    license='MIT',
    author='Fei Wang',
    author_email='fei.comm@icloud.com',
    description='Deep Learning - Pytorch',
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    install_requires=get_requirements(),
    keywords=[
        "artificial intelligence",
        "deep learning",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        'Operating System :: OS Independent',
    ],
)
