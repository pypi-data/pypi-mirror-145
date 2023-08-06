from setuptools import setup
import pathlib
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='prompt-wei',
    version='0.0.2',
    py_modules=['Prompt'],
    long_description=README,
    long_description_content_type="text/markdown",
    package_dir={'': 'src'},
    install_requires=[
        'pynput>=1.7.6',
        'six>=1.16.0'
    ]
)
