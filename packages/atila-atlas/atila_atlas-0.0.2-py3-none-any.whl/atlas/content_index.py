import json
import warnings
from collections import defaultdict
from pathlib import Path

from algoliasearch.search_client import SearchClient

from atlas.settings import ATLAS_ALGOLIA_APPLICATION_ID, ATLAS_ALGOLIA_API_KEY, ATLAS_ALGOLIA_INDEX_NAME

# While searchable attributes could be set to links.text and images.label
# Doing so would have omitted the url from showing in the search result snippets.
SEARCHABLE_ATTRIBUTES = ["title", "description", "body", "url", "links", "images"]


class ContentIndex:
    def __init__(self, application_id=None, api_key=None, index_name=None):
        if index_name is None:
            index_name = ATLAS_ALGOLIA_INDEX_NAME
            if not index_name:
                raise TypeError("ATLAS_ALGOLIA_INDEX_NAME environment variable is not set "
                                "and index_name not provided to ContentIndex(index_name='') constructor.")

        if application_id is None:
            application_id = ATLAS_ALGOLIA_APPLICATION_ID
            if not application_id:
                raise TypeError("ATLAS_ALGOLIA_APPLICATION_ID environment variable is not set "
                                "and application_id not provided to ContentIndex(application_id='') constructor.")

        if api_key is None:
            api_key = ATLAS_ALGOLIA_API_KEY
            if not api_key:
                raise TypeError("ATLAS_ALGOLIA_API_KEY environment variable is not set "
                                "and index_name not provided to ContentIndex(api_key='') constructor.")

        search_client = SearchClient.create(application_id, api_key)
        self.search_client_index = search_client.init_index(index_name)

    def initialize_index(self, settings=None):
        if not settings:
            # About 15-20 words in a sentence
            # https://wordcounter.net/blog/2017/04/04/102966_word-count-list-how-many-words.html
            words_in_snippet = 25
            settings = {
                "searchableAttributes": SEARCHABLE_ATTRIBUTES,
                "attributesToHighlight": [],
                "snippetEllipsisText": "...",
                "attributesToSnippet": [f"{attribute}:{words_in_snippet}" for attribute in SEARCHABLE_ATTRIBUTES],
                "restrictHighlightAndSnippetArrays": True,
                'removeStopWords': True,
                "attributesToRetrieve": ["title", "description", "header_image_url", "url"]
            }
        self.search_client_index.set_settings(settings)

    def add_sample_content_data_to_index(self):
        self.initialize_index()

        with open("data/parsed_content.json") as outfile:
            content_to_save = json.load(outfile)
            content_to_save = list(content_to_save.values())
            self.search_client_index.save_objects(content_to_save, {'autoGenerateObjectIDIfNotExist': True})

    def search(self, query, show_raw_results=False):
        if show_raw_results:
            return self.search_client_index.search(query)["hits"]

        hits = self.search_client_index.search(query)["hits"]

        for hit in hits:
            hit["snippets"] = self.clean_snippets(hit["_snippetResult"])
            # for key, value in hit.items():
            #     if key not in ["title", "description", "header_image_url", "url", "snippets"]:
            #         del hit[key]
            del hit["_snippetResult"]

        return hits

    def clean_snippets(self, snippets):

        snippets = {
            "body": [{"text": self.remove_highlight_tags(snippet["text"]["value"]),
                      "type": self.remove_highlight_tags(snippet["type"]["value"])}
                     for snippet in snippets.get("body", [])
                     if snippet["text"]["matchLevel"] != "none"
                     ][:10],
            "images": [{"label": self.remove_highlight_tags(snippet["label"]["value"]),
                        "url": self.remove_highlight_tags(snippet["url"]["value"])}
                       for snippet in snippets.get("images", [])
                       if snippet["label"]["matchLevel"] != "none"
                       ][:10],
            "links": [{"text": self.remove_highlight_tags(snippet["text"]["value"]),
                       "url": self.remove_highlight_tags(snippet["url"]["value"])}
                      for snippet in snippets.get("links", [])
                      if snippet["text"]["matchLevel"] != "none"][:10]
        }
        return snippets

    @staticmethod
    def remove_highlight_tags(input_string: str):
        return input_string.replace("<em>", "").replace("</em>", "")

    def save_to_search_index(self, content):
        return self.search_client_index.save_object(content)

    def get_inbound_links(self, minimum_link_count=2):
        minimum_link_count = int(minimum_link_count)
        """
        Counting the inbound links to a page can be used to determine the priority of which pages to index next.

        Inspired by the page rank algorithm, which will be added later:
        https://towardsdatascience.com/pagerank-3c568a7d2332
        https://medium.com/analytics-vidhya/how-google-search-works-page-rank-algorithm-using-python-9643d9c9a981
        """
        results = self.search_client_index.browse_objects({"query": "",
                                                           "attributesToRetrieve": [
                                                               "title",
                                                               "url",
                                                               "objectID",
                                                               "links"
                                                           ]
                                                           })

        inbound_links = defaultdict(lambda: {"unique_sources_count": 0, "sources": []})

        for result in results:
            for outbound_link in result.get("links", []):
                outbound_link_id = outbound_link["objectID"]
                outbound_link["source_url"] = result["url"]
                inbound_links[outbound_link_id]["sources"].append(outbound_link)
                inbound_links[outbound_link_id]["url"] = outbound_link["url"]

        for object_id in list(inbound_links.keys()):
            inbound_link = inbound_links[object_id]
            unique_sources = set([source["source_url"] for source in inbound_link["sources"]])
            inbound_link["unique_sources_count"] = len(unique_sources)

            if inbound_link["unique_sources_count"] < minimum_link_count:
                del inbound_links[object_id]

        inbound_links = {k: v for k, v in sorted(inbound_links.items(),
                                                 key=lambda key_value: key_value[1]["unique_sources_count"],
                                                 reverse=True)}

        parent_directory = Path(__file__).resolve().parents[0]
        output_json_file = "data/inbound_links_metadata.json"
        Path("data").mkdir(parents=True, exist_ok=True)

        with open(output_json_file, 'w') as outfile:
            json.dump(inbound_links, outfile, indent=4)

        output_links_file = parent_directory / "data/inbound_links_urls.txt"
        with open(output_links_file, 'w') as f:
            for inbound_link in inbound_links.values():
                f.write("%s\n" % inbound_link["url"])


if __name__ == "__main__":
    content_index = ContentIndex()
    content_index.initialize_index()
