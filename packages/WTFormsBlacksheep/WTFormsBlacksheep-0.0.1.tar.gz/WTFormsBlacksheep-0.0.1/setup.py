from setuptools import setup, find_packages

classifiers = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
]

setup(
    name='WTFormsBlacksheep',
    version='0.0.1',
    description='WTForm Blacksheep',
    long_description_content_type="text/markdown",
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Abdulaminhon Khaydarov',
    author_email='info@thinkland.uz',
    license='MIT',
    classifiers=classifiers,
    keywords='wtformsblacksheep',
    packages=find_packages(),
    install_requires=['WTForms', 'blacksheep', 'multidict', 'pydantic']
)
