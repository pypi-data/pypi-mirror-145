import pathlib
from setuptools import setup

BASEDIR = pathlib.Path(__file__).parent
README = (BASEDIR / "README.md").read_text()

setup(
    name="Stack Frame Analyzer",
    python_requires=">3.6",
    version="0.2.1",
    description="It helps to get the context of a frame from the caller's stack. Can be used to improve service and microservice logs.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/cesarmerjan/stack_frame_analyzer",
    download_url="https://github.com/cesarmerjan/stack_frame_analyzer/archive/refs/heads/master.zip",
    author="Cesar Merjan",
    author_email="cesarmerjan@gmail.com",
    keywords=["logging", "stack", "frame"],
    license="MIT",
    include_package_data=True,
    package_dir={"": "src"},
    packages=["stack_frame_analyzer"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Topic :: Software Development :: Bug Tracking",
        "Topic :: Software Development :: Debuggers",
        "Topic :: System :: Logging",
        "Topic :: System :: Software Distribution",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",

    ]
)
