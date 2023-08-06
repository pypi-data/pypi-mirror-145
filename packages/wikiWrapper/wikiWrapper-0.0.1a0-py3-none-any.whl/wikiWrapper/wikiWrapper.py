import requests
import json
from bs4 import BeautifulSoup as bs

hosts = {
    "wikipedia": "https://en.wikipedia.org/w/api.php",
    "wikidata": "https://www.wikidata.com/w/api.php",
    "wikibooks": "https://en.wikibooks.org/w/api.php"
}
responses = {
    "wikipedia": "https://en.wikipedia.org/?curid=",
    "wikidata": "https://en.wikidata.org/?curid=",
    "wikibooks": "https://en.wikibooks.org/?curid="
}


class SearchQuery:
    def __init__(self, search_q, host="wikipedia", srnamespace=0, srlimit=10, sroffset=0, srqiprofile="classic", _format="json"):
        self.action = "query"
        self.list = "search"
        self.host = host
        self.search_q = search_q
        self.format = _format
        self.srnamespace = srnamespace
        self.srlimit = srlimit
        self.sroffset = sroffset
        self.srqiprofile = srqiprofile
        self.url = None

    def search(self):
        payload = {
            "action": self.action,
            "list": self.list,
            "format": self.format,
            "srsearch": self.search_q,
            "srnamespace": self.srnamespace,
            "srlimit": self.srlimit,
            "sroffset": self.sroffset,
            "srqiprofile": self.srqiprofile
        }
        try:
            r = requests.get(hosts[self.host], params=payload)
        except KeyError:
            raise RuntimeError("Invalid host specified")
        self.url = get_wiki_url(r, self.host)
        return r

    def content_summary(self):
        pid = get_wiki_url(self.search(), self.host, rtn_pid=True)
        payload = {
            "action": "query",
            "prop": "extracts",
            "exintro": "explaintext",
            "redirects": 1,
            "pageids": pid,
            "format": self.format
        }
        r = requests.get(hosts[self.host], params=payload)
        # decodes bytes into str type
        utf_raw = r.content.decode("utf-8")
        # turns str into dict
        raw = json.loads(utf_raw)
        # gets HTML data and turns it into a bs4 object
        html_data = raw["query"]["pages"][str(pid)]["extract"]
        soup = bs(html_data, "html.parser")
        content = "".join(soup.find_all(text=True))
        return content.strip()


def get_wiki_url(pid, response, rtn_pid=False):
    if type(pid) is not requests.models.Response:
        raise TypeError("Argument must be a requests object")
    try:
        pid = pid.json()["query"]["search"][0]["pageid"]
    except IndexError:
        return None
    if rtn_pid:
        return pid
    return f"{responses[response]}{pid}"
