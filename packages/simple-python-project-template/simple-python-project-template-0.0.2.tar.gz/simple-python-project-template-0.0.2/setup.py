import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="simple-python-project-template",
    version="0.0.2",
    description="A simple Python project template.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hreikin/simple-python-project-template",
    author="user",
    author_email="user@example.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["simple_python_project_template"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "simple_python_project_template=simple_python_project_template.__main__:main",
        ]
    },
)

# setup(
#     name="simple-python-project-template",
#     version="0.0.1",
#     description="A simple Python project template.",
#     long_description=README,
#     long_description_content_type="text/markdown",
#     url="https://github.com/hreikin/simple-python-project-template",
#     author="user",
#     author_email="user@example.com",
#     license="MIT",
#     classifiers=[
#         "License :: OSI Approved :: MIT License",
#         "Programming Language :: Python :: 3",
#         "Programming Language :: Python :: 3.7",
#     ],
#     packages=["tkintermd"],
#     include_package_data=True,
#     # install_requires=[],
#     entry_points={
#         "console_scripts": [
#             "simple_python_project_template=simple_python_project_template.__main__:main",
#         ]
#     },
# )
