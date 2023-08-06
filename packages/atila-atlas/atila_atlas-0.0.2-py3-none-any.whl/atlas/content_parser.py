import hashlib
import json
from datetime import datetime
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from requests import HTTPError
from typing import List
import requests
from publicsuffix2 import get_sld

from atlas.content_index import ContentIndex


def current_time_iso():
    return datetime.utcnow().replace(microsecond=0).isoformat()


FALLBACK_ENCODING = 'ISO-8859-1'


class ContentParser:

    def __init__(self,
                 urls: List[str] = None,
                 input_file: str = None,
                 application_id=None,
                 api_key=None,
                 index_name=None):

        if input_file:
            self.get_urls_from_file(input_file)
        else:
            self.urls = [url.rstrip("/") for url in urls]

        self.content_index = ContentIndex(application_id=application_id, api_key=api_key, index_name=index_name)
        # all_content ->'object_id' -> {'json': {}, 'html': '', 'object_id' : '', 'url': '', 'article', 'soup'}
        self.all_content = defaultdict(dict)

    def get_urls_from_file(self, file_name):
        with open(file_name) as f:
            urls = f.readlines()

        # remove whitespace characters like `\n` at the end of each line
        self.urls = [url.strip().rstrip("/") for url in urls]

    def parse_all_content(self, save=False):
        for index, url in enumerate(self.urls):
            print(f"Progress: {index + 1}/{len(self.urls)}")
            parsed_content = self.parse_content(url)
            if save:
                parsed_content['date_saved'] = current_time_iso()
                self.content_index.save_to_search_index(parsed_content)

    def save_to_file(self, save_type="json", file_name="parsed_content"):
        if save_type == "html":
            for content_id, content in self.all_content.items():
                domain = urlparse(self.all_content[content_id]["url"]).netloc
                file_name = f"{domain}-{content_id[:8]}"
                output_file_name = f"data/html_files/{file_name}.html"
                Path(output_file_name).parents[0].mkdir(parents=True, exist_ok=True)
                with open(output_file_name, 'w') as outfile:
                    outfile.write(content['html'])
        else:
            output_file_name = f"data/{file_name}.json"
            Path(output_file_name).parents[0].mkdir(parents=True, exist_ok=True)
            content_to_save = {}
            for content_id, content in self.all_content.items():
                content_to_save[content_id] = content['json']

            if Path(output_file_name).exists():
                with open(output_file_name) as outfile:
                    existing_content = json.load(outfile)
                    content_to_save = {**existing_content, **content_to_save}

            with open(output_file_name, 'w') as outfile:
                json.dump(content_to_save, outfile, indent=4)

    def parse_content(self, url: str):
        object_id = self.url_to_object_id(url)
        self.all_content[object_id]['objectID'] = object_id
        self.all_content[object_id]['url'] = url
        self.all_content[object_id]['html'] = ''

        response = requests.get(url)
        try:
            response.raise_for_status()
            response_html = self.get_html_from_response(response)
            soup = BeautifulSoup(response_html, "html.parser")
            self.all_content[object_id]['html'] = soup.prettify()

            content = {
                "objectID": object_id,  # use camelcase instead of underscore case to match Algolia syntax
                "url": url,
                "title": self.get_title(soup),
                "description": self.get_description(soup),
                "body": self.get_body(soup),
                "images": self.get_images(soup, url),
                "links": self.get_links(soup, url),
                "header_image_url": self.get_header_image_url(soup),
                "date_parsed": current_time_iso(),
            }
            content["body_byte_count"] = len(json.dumps(content["body"]).encode('utf-8'))
            content["images_byte_count"] = len(json.dumps(content["images"]).encode('utf-8'))
            content["links_byte_count"] = len(json.dumps(content["links"]).encode('utf-8'))
        except HTTPError as e:
            content = {
                "objectID": object_id,  # use camelcase instead of underscore case to match Algolia syntax
                "url": url,
                "error": str(e),
                "error_response": f"status code: {response.status_code} reason: {response.reason}",
                "title": "",
                "description": "",
                "body": [],
                "images": [],
                "links": [],
                "header_image_url": "",
                "date_parsed": current_time_iso(),
            }

        self.all_content[object_id]['json'] = content
        return content

    @staticmethod
    def get_html_from_response(response):
        """
        Logic copied from newspaper package network.py: _get_html_from_response()
        :param response:
        :return:
        """
        if response.encoding != FALLBACK_ENCODING:
            # return response as a unicode string
            html = response.text
        else:
            html = response.content
            if 'charset' not in response.headers.get('content-type'):
                encodings = requests.utils.get_encodings_from_content(response.text)
                if len(encodings) > 0:
                    response.encoding = encodings[0]
                    html = response.text

        return html or ''

    def get_links(self, soup, article_url):
        link_tags = soup.find_all(["a"])
        links = []
        article_domain = urlparse(article_url).netloc
        article_domain = get_sld(article_domain)
        for link_tag in link_tags:

            if not link_tag.attrs.get('href') or link_tag.attrs['href'].startswith("#"):
                continue

            link_text = link_tag.text.strip()
            link_url = urljoin(article_url, link_tag.attrs['href'].strip()).rstrip("/")
            link_domain = urlparse(link_url).netloc
            link_domain = get_sld(link_domain)
            # internal links don't need to be indexed because it's not a strong signal of importance
            if link_domain == article_domain:
                continue

            # mailto might be useful for getting contact information
            if not link_url.startswith("http") and not link_url.startswith("mailto:"):
                continue

            # skip link if it already exists in the list of links and it has the same text
            if next((existing_ink for existing_ink in links
                     if existing_ink["url"] == link_url and existing_ink["text"] == link_text),
                    False):
                continue

            link = {
                "url": link_url,
                "text": link_text,
                "objectID": self.url_to_object_id(link_url)
            }
            links.append(link)

        links = self.truncate_within_byte_limit(links, "links")
        return links

    @staticmethod
    def truncate_within_byte_limit(items: list, item_key):
        """
        params: max_bytes_size: The number of bytes allowed for a field, Algolia allows 100,000 bytes (100kb)
        However, we will limit our record sizes to 20kb
        so truncate to 14000 bytes for body and 3,000 bytes for links and 3,000 for images
        To prevent saving files that go over the bytes limit.
        If the number of items is over the bytesize limit, only
        see:
        algoliasearch.exceptions.RequestException: Record at the position 0
        objectID=3e631e488eb753c0a8bbd4f74d75accd769a0e666ad36b2673f77fce3b110991 is too big size=105283/100000 bytes.
         Please have a look at
         https://www.algolia.com/doc/guides/sending-and-managing-data/prepare-your-data/in-depth/index-and-records-size-and-usage-limitations/#record-size-limits

        """

        max_bytes_sizes = {
            "body": 50000,
            "links": 14000,
            "images": 7000,
        }
        max_bytes_size = max_bytes_sizes[item_key]

        bytes_count = len(json.dumps(items).encode('utf-8'))
        while bytes_count > max_bytes_size:
            # average bytes per item, round bytes per item up and truncated items down
            # so that the array is more likely to be within the desired range
            items = items[:-1]
            bytes_count = len(json.dumps(items).encode('utf-8'))

        return items

    def get_body(self, soup):
        sections = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "figcaption"])

        body = []
        for section in sections:
            text = " ".join(section.text.split())
            # exclude list items with 1 word because it's usually not relevant information
            if section.name == "li" and len(text.split(" ")) <= 1:
                continue

            body_item = {"type": section.name, "text": text}
            body.append(body_item)

        body = self.truncate_within_byte_limit(body, "body")
        return body

    def get_images(self, soup: BeautifulSoup, url):
        images_tags = soup.find_all(["img"])
        images = []
        # only save images with an alt tag to reduce likelihood of saving less relevant images
        # (e.g. social media images)
        for image_tag in images_tags:
            if not image_tag.attrs.get('src'):
                continue
            if image_tag.attrs['src'].startswith('data:'):
                continue
            # svg images are typically icons like right arrows, usually not a high value thing to index
            if image_tag.attrs['src'].endswith('.svg'):
                continue

            image_url = urljoin(url, image_tag.attrs['src'].strip()).rstrip("/")
            image = {"label": image_tag.attrs.get('alt', '').strip(),
                     "url": image_url,
                     "objectID": self.url_to_object_id(image_url)
                     }
            if not image["label"] and image_tag.find_next('figcaption'):
                # TODO very hacky, this may not be the correct caption
                image["label"] = image_tag.find_next('figcaption').text

            images.append(image)

        images = self.truncate_within_byte_limit(images, "images")
        return images

    @staticmethod
    def get_description(soup: BeautifulSoup):

        meta_description = soup.find(["meta"], attrs={'name': 'description'})
        if meta_description:
            return meta_description.get('content')
        meta_description = soup.find(["meta"], attrs={'property': 'og:description'})
        if meta_description:
            return meta_description.get('content')
        return ""

    @staticmethod
    def url_to_object_id(url: str):
        url = url.rstrip("/")
        hash_object = hashlib.new('sha256')
        hash_object.update(url.encode())
        object_id = hash_object.hexdigest()
        return object_id

    @staticmethod
    def get_title(soup: BeautifulSoup):
        meta_title = soup.find(["meta"], attrs={'property': 'og:title'})
        if meta_title:
            return meta_title.get('content')
        meta_title = soup.find(["title"])
        if meta_title:
            return meta_title.text
        return ""

    @staticmethod
    def get_header_image_url(soup: BeautifulSoup):
        meta_image = soup.find(["meta"], attrs={'property': 'og:image'})
        if meta_image:
            return meta_image.get('content')
        else:
            return ""


if __name__ == "__main__":
    sample_urls = [
        "https://ethereum.org/en/nft",
        "https://linda.mirror.xyz/df649d61efb92c910464a4e74ae213c4cab150b9cbcc4b7fb6090fc77881a95d",
    ]
    content_bot = ContentParser(urls=sample_urls)
    content_bot.parse_all_content(save=True)
    content_bot.save_to_file(save_type="html")
    content_bot.save_to_file(save_type="json")
