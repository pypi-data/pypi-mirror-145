from setuptools import setup, find_packages
from uip import UIP_CLI_VERSION

def main():
    with open('README.rst', 'r') as readme:
        long_description = readme.read()
    setup(
        name='uip-cli',
        version=UIP_CLI_VERSION,
        packages=find_packages(exclude=['*test*']),
        include_package_data=True,
        install_requires=[
            "colorama >= 0.4.4",
            "requests >= 2.26.0",
            "jinja2 >= 2.11.3",
            "prettytable >= 1.0.1",
            "pyyaml >= 5.4.1",
            "setuptools >= 44.1.1"
        ],
        extras_require={
            'tests': ['configparser', 'mock', 'pyyaml', 'pytest']
        },
        author='Stonebranch',
        license="GNU General Public License",
        license_files='LICENSE.txt',
        description='Universal Extension CLI for interfacing with Controller Web Services',
        entry_points={
            'console_scripts': [
                'uip=uip.main:main'
            ]
        },
        python_requires='>=2.7',
        classifiers=[
            'Operating System :: POSIX :: Linux',
            'Operating System :: Microsoft :: Windows',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3'
        ],
        long_description=long_description,
        long_description_content_type="text/x-rst"
    )


if __name__ == '__main__':
    main()
