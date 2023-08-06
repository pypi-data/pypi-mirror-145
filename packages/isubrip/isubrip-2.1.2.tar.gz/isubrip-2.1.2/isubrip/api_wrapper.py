from typing import Union
import requests
import html

ITUNES_API_SEARCH_URL = "https://itunes.apple.com/search?"
ITUNES_API_LOOKUP_URL = "https://itunes.apple.com/lookup?"

class APIWrapper:

    @staticmethod
    def search_movie(search_term: str, country_codes: list = ["us"]):
        api_request_url = ITUNES_API_SEARCH_URL + "term=" + html.escape(search_term).replace(' ', '+') + "&media=movie&country=il"

        if country_codes
        pass

    @staticmethod
    def lookup_movie(itunes_id: str = None, amg_id: str = None):        
        if itunes_id is not None:
            api_request_url = ITUNES_API_LOOKUP_URL + "id=" + itunes_id + "&media=movie"

        elif amg_id is not None:
            api_request_url = ITUNES_API_LOOKUP_URL + "amgVideoId=" + amg_id + "&media=movie"

        else:
            raise ValueError("An iTunes ID or an AMG ID must be provided.")

        pass



if __name__ == "__main__":
    APIWrapper.search_movie("The Matrix")
    pass