import setuptools
from chaosmeter import __author__, __url__, __version__, __license__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='chaosmeter',
    version=__version__,
    url=__url__,
    author=__author__,
    author_email="ali.parsai@live.com",
    description="ChaosMeter Complexity Metric Calculator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=__license__,
    packages=setuptools.find_packages(),
    install_requires=['antlr4-python3-runtime', 'odfpy', 'littledarwin'],
    entry_points={'console_scripts': ['chaosmeter=chaosmeter.__main__:entryPoint', ], },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

