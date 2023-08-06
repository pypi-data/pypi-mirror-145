import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="atila-atlas",
    version="0.0.2",
    author="Atila Tech",
    author_email="info@atila.ca",
    description="Atlas is a search engine for parsing a collection of web pages and making it searchable.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atilatech/atlas",
    project_urls={
        "Bug Tracker": "https://github.com/atilatech/atlas/issues",
    },
    license="MIT",
    packages=["atlas"],
    python_requires='>=3.6',
    install_requires=[
        'algoliasearch==2.6.1',
        'beautifulsoup4==4.10.0',
        'docopt==0.6.2',
        'publicsuffix2==2.20191221',
        'requests==2.27.1',
    ],
    entry_points={
        'console_scripts': [
            'atlas=atlas.run_atlas:main',
        ],
    }
)
