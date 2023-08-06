from setuptools import setup, find_packages

VERSION = '1.0.150'

setup(
    name='pyopereto',
    version=VERSION,
    author='Dror Russo',
    author_email='dror.russo@opereto.com',
    description='Opereto Python Client',
    url = 'https://github.com/opereto/pyopereto',
    download_url = 'https://github.com/opereto/pyopereto/archive/%s.tar.gz'%VERSION,
    keywords = [],
    classifiers = [],
    packages = find_packages(),
    package_data={'': ['service.md', 'service.sam.json', 'service.yaml']},

    entry_points = {
        'console_scripts': ['opereto=pyopereto.command_line:main']
    },
    install_requires=[
        "requests > 2.7.0",
        "requests_toolbelt == 0.9.1",
        "pyyaml >= 5.1",
        "docopt == 0.6.2",
        "colorlog == 6.6.0",
        "pyjwt == 2.3.0"
    ]
)

