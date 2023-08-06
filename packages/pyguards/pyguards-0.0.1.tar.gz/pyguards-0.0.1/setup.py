from setuptools import setup


def read_file(path: str):
    with open(path, encoding='utf-8') as f:
        return f.read()


def read_requirements(path):
    return [line for line in read_file(path).split('\n') if line and not line.strip().startswith('#')]


setup(
    name='pyguards',
    version=read_file('VERSION'),
    author='Mathius',
    author_email='ferymathieuy@gmail.com',
    description='Checks and Guards for Python',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/MathiusD/pyguards',
    project_urls={
        'Issues tracker': 'https://gitlab.com/MathiusD/pyguards/-/issues'
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',

        'Operating System :: OS Independent',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Intended Audience :: Developers',
    ],
    keywords='pyguards guards',
    packages=[
        'pyguards',
        'pyguards.checkers'
    ],
    include_package_data=True,
    python_requires='>=3.6',
    test_suite='tests',
    install_requires=read_requirements('requirements.txt'),
    tests_require=read_requirements('tests-requirements.txt'),
)
