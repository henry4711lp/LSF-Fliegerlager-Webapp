from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='Fliegerlager Web App',
    description='This app is to replace a handwritten list for "bought" drinks, dinners and accomodation days. The purpose of this webapp is to decrease the workload of the club youth management in the accounting process of the flying camp and to prevent the loss of the handwritten lists.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='henry4711lp',
    url='',
    packages=find_packages('src'),
    package_dir={
        'src': 'src'},
    include_package_data=True,
    keywords=[
        'web_app', 'test', 'flask', 'lsf-wesel-rheinhausen',
    ],
    entry_points={
        'console_scripts': [
            'web_server = app:main']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
