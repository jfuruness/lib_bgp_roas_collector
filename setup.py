from setuptools import setup, find_packages

setup(
    name='lib_bgp_roas_collector',
    packages=find_packages(),
    version='0.1.00',
    author='Justin Furuness',
    author_email='jfuruness@gmail.com',
    url='https://github.com/jfuruness/lib_bgp_roas_collector.git',
    download_url='https://github.com/jfuruness/lib_bgp_roas_collector.git',
    keywords=['Furuness', 'furuness', 'pypi', 'package'],  # arbitrary keywords
    test_suite='nose.collector',
    tests_require=['nose'],
    install_requires=[
        'psycopg2_binary>=2.7.6.1',
        'requests>=2.18.4',
        'pathos>=0.2.2.1',
        'mrtparse>=1.6',
        'setuptools>=39.0.1',
        'psycopg2>=2.7.7'
    ],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'],
    entry_points={
        'console_scripts': [
            'roas_collection = lib_bgp_roas_collection.__main__:main'
        ]},
)

