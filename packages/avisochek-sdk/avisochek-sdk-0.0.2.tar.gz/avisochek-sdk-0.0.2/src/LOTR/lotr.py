import requests
import json

class LOTR:
    def __init__(self, token):
        self.api_token = token
    # Make a call to the API. 
    # TODO if time:
    ##  Abstract this to a separate client module.
    # TODO if time:
    ##  Error Handling
    def get_resource(self, endpoint):
        r = requests.get(
            f"https://the-one-api.dev/v2{endpoint}",
            headers={"Authorization": f"Bearer {self.api_token}"})
        return json.loads(r.text)["docs"]

    # Get full list of books.
    def get_book_info(self): 
        return self.get_resource("/book")

    # Get full list of movies.
    def get_movie_info(self): 
        return self.get_resource("/movie")

    # Get a full list of characters
    # TODO if time: 
    ##  Add filtration / pagination options for characters
    def get_character_info(self): # Get a full list of characters.
        return self.get_resource("/character")

    # Get a list of quotes from a particular movie 
    # (only works for lord of the rings trilogy for now)
    def get_quotes_from_movie(self,movie_id):
        return self.get_resource(f"/movie/{movie_id}/quote")

    # Get a list of Quotes from a particular character
    def get_quotes_from_character(self,character_id):
        return self.get_resource(f"/character/{character_id}/quote")

    # Get a list of chapters from a book
    def get_book_chapters(self,book_id):
        return self.get_resource(f"/book/{book_id}/chapter")
