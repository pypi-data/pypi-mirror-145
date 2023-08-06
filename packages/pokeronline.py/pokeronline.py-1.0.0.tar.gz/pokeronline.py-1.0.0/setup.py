from setuptools import setup, find_packages

with open("README.md", "r") as stream:
    long_description = stream.read()

setup(
    name = "pokeronline.py",
    version = "1.0.0",
    url = "https://github.com/Zakovskiy/pokeronline.py",
    download_url = "https://github.com/Zakovskiy/pokeronline.py/tarball/master",
    license = "MIT",
    author = "Zakovskiy",
    author_email = "gogrugu@gmail.com",
    description = "A library to create Poker Online bots.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    keywords = [
        "durak",
        "online",
        "pokeronline",
        "pokeronline.py",
        "pokeronline-bot",
        "rstgame",
        "rstgames",
        "api",
        "socket",
        "python",
        "python3",
        "python3.x",
        "zakovskiy",
        "official"
    ],
    install_requires = [
        "setuptools",
        "requests",
        "loguru",
        "aiohttp"
    ],
    setup_requires = [
        "wheel"
    ],
    packages = find_packages()
)
