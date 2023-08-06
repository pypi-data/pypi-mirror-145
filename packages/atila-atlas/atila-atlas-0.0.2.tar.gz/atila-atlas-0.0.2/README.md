# Atlas

A search engine for the internet.

Atlas stands for Atila's Tool for Learning any Subject. 
To start, Atlas will be focused on effectively indexing and searching crypto and web3 related
content with plans to add other subjects in the future. 
However, you're welcome to use Atlas to index and search any type of content you want.

## Installation

`pip install atila-atlas`

Set your environment variables:
```shell
export ATLAS_ALGOLIA_APPLICATION_ID=""
export ATLAS_ALGOLIA_API_KEY=""
export ATLAS_ALGOLIA_INDEX_NAME=""
```

### Development Installation

```shell
source install.sh
pip install -e .
```

## Quickstart

```shell
atlas initialize_index
atlas add_content --file data/urls_to_parse.txt
atlas add_content --urls https://ethereum.org/en/nft,https://en.wikipedia.org/wiki/Ethereum
atlas search "what is an nft"
atlas get_inbound_links --min-inbound-links=2
```


```python
from atlas.content_parser import ContentParser, ContentIndex

sample_urls = [
   "https://ethereum.org/en/nft",
   "https://en.wikipedia.org/wiki/Ethereum",
   "https://linda.mirror.xyz/df649d61efb92c910464a4e74ae213c4cab150b9cbcc4b7fb6090fc77881a95d",
   "https://chain.link/education/nfts",
   "https://medium.com/superrare/no-cryptoartists-arent-harming-the-planet-43182f72fc61",
   "https://andrewsteinwold.substack.com/p/-quick-overview-of-the-nft-ecosystem",
   "https://medium.com/superrare/no-cryptoartists-arent-harming-the-planet-43182f72fc61"
]

content_bot = ContentParser(urls=sample_urls)
content_bot.parse_all_content()
content_bot.save_to_file()

content_index = ContentIndex()
content_index.initialize_index()
results = content_index.search("what is an nft")
```


### Development Quickstart

Note: Make sure you've put your environment variables into the newly created
`.env` file that was taken from `shared.env`

```shell
# 1. Parse and index your content:
python atlas/content_parser.py

# 2. Initialize your content:
python atlas/content_index.py

# 3. Run the API
python api/api.py

# 4. Send a GET request to your api
curl --location --request GET 'http://127.0.0.1:8080/api/search?q=what+is+an+NFT'
# or open your browser to `http://127.0.0.1:8080/api/search?q=<your_search_term>` 
```

## Publishing Package to PyPi

1. `python -m build`
2. Uploading to test PYPi server first to practice:
3. `python -m twine upload --repository testpypi dist/*`
   1. Note the use of no-dependencies flag: `--no-deps`. This is because the dependencies might not be in the TestPyPi 
   2. Set your username to `__token__`
   3. Set your password to the token value, including the pypi- prefix
   4. Test: https://test.pypi.org/manage/account/#api-tokens
   5. Prod: https://pypi.org/manage/account/#api-tokens
4. Upload to the real PyPI server: `python -m twine upload dist/*`

## Troubleshooting

`ModuleNotFoundError: No module named 'atlas'`

Set your $PYTHONPATH. See this [SO answer](https://stackoverflow.com/a/15622021/5405197)