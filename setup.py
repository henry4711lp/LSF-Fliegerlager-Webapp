from setuptools import find_packages
from setuptools import setup

setup(
    name='Fliegerlager Web App',
    description='This app is to replace a handwritten list for "bought" drinks, dinners and accomodation days. The purpose of this webapp is to decrease the workload of the club youth management in the accounting process of the flying camp and to prevent the loss of the handwritten lists. ',
    author='henry4711lp',
    url='',
    packages=find_packages('src'),
    package_dir={
        '': 'src'},
    include_package_data=True,
    keywords=[
        'web_app', 'test', 'flask'
    ],
    entry_points={
        'console_scripts': [
            'web_server = app:main']},
)