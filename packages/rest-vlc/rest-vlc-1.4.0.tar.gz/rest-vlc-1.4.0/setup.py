import setuptools

setuptools.setup(
    name="rest-vlc",
    version="1.4.0",
    author="Rukchad Wongprayoon",
    author_email="contact@biomooping.tk",
    description="A Python library for controlling VLC media player via REST API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/timelessnesses/rest-vlc",
    py_modules=["rest_vlc"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    tests_require=["pytest"],
    python_requires=">=3",
    license="MIT",
    install_requires=["requests", "xmltodict"],
    extras_require={
        "dev": ["pytest", "python-dotenv"],
        "build": ["build", "wheel"],
        "async": ["aiohttp[speedups]", "uvloop ; sys_platform == 'linux'"],
        "publish": ["twine", "wheel"],
    },
)
