import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DarbouxCoins",
    version="0.1",
    author="Subrata",
    author_email="",
    description="A discord bot who generate coins and lives for HQ Trivia.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Subrata2402/Darboux-Coins",
    #entry_points={'console_scripts': ['HQApi = HQApi.hq_api_cli:main']},
    install_requires=['aiohttp', 'discord.py', 'pymongo', 'requests', 'lomond', 'dnspython', 'pytz', 'aniso8601', 'unidecode', 'bs4', 'jwt'],
    packages=["Darboux"],
    python_requires='>=3.8',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)