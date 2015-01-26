from setuptools import setup, find_packages
setup(
    name="ltur-notifier",
    version="1.0",
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    test_suite='test',
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt'],
    }
)

 
