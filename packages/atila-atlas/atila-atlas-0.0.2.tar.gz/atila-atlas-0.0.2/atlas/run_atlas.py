#!/usr/bin/env python
"""
Atila Atlas: Save content to a database and search that data.

Usage:
  atlas initialize_index
  atlas add_content [--urls=<urls>] [--file=<file>]
  atlas search <query>
  atlas get_inbound_links [--min-inbound-links=<min>]

Options:
  -h --help     Show this screen.
  --urls=<urls>   The urls to parse, separated by a comma
  --file=<file> The input file that contains:
    - If a txt file is provided, a list of urls that should be parsed.
  --min-inbound-links=<min>   The minimum number of inbound links to include
Examples:
   atlas initialize_index
   atlas add_content --file data/urls_to_parse.txt
   atlas add_content --urls https://ethereum.org/en/nft,https://chain.link/education/nfts
   atlas query "what is an nft"
   atlas get_inbound_links --min-inbound-links=2
"""
import json

from docopt import docopt

from atlas.content_index import ContentIndex
from atlas.content_parser import ContentParser


def run_atlas(cli_args):
    """
    Call this function with any of the following arguments:
    {
        "--url": "entry_url",
        "--file": "input_file",
        "--limit": "limit",
        add_content: True | False,
    }
    """

    bot_args = {}

    args_map: dict = {
        "--urls": "urls",
        "<query>": "query",
        "--file": "input_file",
        "--min-inbound-links": "minimum_link_count",
        # "--limit": "limit",
    }

    for cli_arg, bot_arg in args_map.items():
        if cli_args.get(cli_arg, None):
            bot_args[bot_arg] = cli_args[cli_arg]

    if bot_args.get("urls"):
        bot_args["urls"] = bot_args["urls"].split(",")

    if bot_args.get("minimum_link_count"):
        bot_args["minimum_link_count"] = int(bot_args["minimum_link_count"])

    print("bot_args", bot_args)

    if cli_args.get('add_content'):
        content_parser = ContentParser(**bot_args)
        content_parser.parse_all_content(save=True)
        content_parser.save_to_file("html")
        content_parser.save_to_file("json")

    if cli_args.get('initialize_index'):
        content_index = ContentIndex()
        content_index.initialize_index()

    if cli_args.get('get_inbound_links'):
        content_index = ContentIndex()
        content_index.get_inbound_links(**bot_args)

    if cli_args.get('search'):
        content_index = ContentIndex()
        results = content_index.search(bot_args.get("query"))
        print(json.dumps(results, indent=4))


def main():
    cli_args = docopt(__doc__)
    print("cli_args", cli_args)
    run_atlas(cli_args)


if __name__ == '__main__':
    main()
