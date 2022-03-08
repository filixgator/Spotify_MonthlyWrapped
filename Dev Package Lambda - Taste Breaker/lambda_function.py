import json
from re import I
import requests
import datetime
import random

token_url = 'https://accounts.spotify.com/api/token'
clientSecret_64 = "MDVhNDNiZjIxMjQyNGRkMzhjYjIxZTYwYzExZjdiMzI6NmM4MGZkNDBkNmFkNDZkY2FjYTZhMjg3ZTYxMWIxODg="
spotify_token = ""
spotify_user_id = ""

__now__ = datetime.datetime.now()
__date__ = lambda x: x.strftime("%d %b %y")

class Spotify_wrapped():
    def __init__(self):
        self.spotify_user_id = ""
        self.spotify_token = ""
        self.refresh_token = ""
        self.scope = ""
        self.playlist_name = "Montlhy Wrapped - API"
        self.playlist_description = "Top user tracks from the last 4 weeks"
        self.playlist_id = ""
        self.tracks = ""
        self.display_name = ""
        self.now = "{}".format(__date__(__now__))
        self.headers = {"Content-Type" : "application/json",
                        "Authorization" : "Bearer {}".format(self.spotify_token)}

    def get_token(self, code):
        print("> getting token...")
        headers = {
            'Authorization': "Basic " + clientSecret_64,
        }
        
        data = {
            'grant_type': 'authorization_code',
            'code': code,
        ##    'redirect_uri': 'https://github.com/filixgator'
            'redirect_uri': 'https://38sgfvcwyf.execute-api.us-east-2.amazonaws.com/test/tastebreakers'
        }
        
        response = requests.post(token_url, headers=headers, data=data)
        
        full_token = response.json()
        print("> full token:")
        print(full_token)

        self.spotify_token = full_token["access_token"]
        self.refresh_token = full_token["refresh_token"]
        self.scope = full_token["scope"]
        print("> scope: " + self.scope)


        #self.get_user_id()
        return
        ## return response_json
    
    def get_user_id(self):
        print("> getting user id...")
        query = "https://api.spotify.com/v1/me"
        print("> token : " + self.spotify_token)
        response = requests.get(query, headers={"Content-Type" : "application/json",
                                                "Authorization" : "Bearer {}".format(self.spotify_token)})
        response_json = response.json()
        self.spotify_user_id = response_json["id"]
        try:
            self.display_name = response_json["display_name"]
        except:
            self.display_name = "User"
        
        print("> spotify_user_id: " + self.spotify_user_id)
        print("> display_name: " + self.display_name)
        
        #self.create_playlist()
        return

    def get_top_tracks(self):
        print("> getting user's top tracks from past 4 weeks...")
        self.playlist_name = "All Time High - API"
        self.playlist_description = "Top user tracks from the last 4 weeks (aprox)."
        self.tracks = ""
        time_range = "short_term"
        limit = "30"
        print("> token : " + self.spotify_token)
        query = "https://api.spotify.com/v1/me/top/tracks?limit={}&time_range={}".format(limit,time_range)
        response = requests.get(query, headers={"Content-Type" : "application/json",
                                                "Authorization" : "Bearer {}".format(self.spotify_token)})
                                                
        response_json = response.json()
        
        print("> top tracks:")
        
        for i in response_json["items"]:
            print(i["name"] + " : " + i["uri"])
            self.tracks += (i["uri"] + ",")
        
        self.tracks = self.tracks[:-1]
        return
    
    def get_alltimehigh_tracks(self):
        print("> getting user's top tracks from all time...")
        self.tracks = ""
        self.playlist_name = "All Time High - API"
        self.playlist_description = "Top user tracks from all time, calculated from several years of data."
        time_range = "long_term"
        limit = "30"
        print("> token : " + self.spotify_token)
        query = "https://api.spotify.com/v1/me/top/tracks?limit={}&time_range={}".format(limit,time_range)
        response = requests.get(query, headers={"Content-Type" : "application/json",
                                                "Authorization" : "Bearer {}".format(self.spotify_token)})
                                                
        response_json = response.json()
        
        print("> top tracks from all time:")
        
        for i in response_json["items"]:
            print(i["name"] + " : " + i["uri"])
            self.tracks += (i["uri"] + ",")
        
        self.tracks = self.tracks[:-1]
        return

    def get_userSaved_tracks(self):
        ## Get a list of the songs saved in the current Spotify user's 'Your Music' library.
        print("> getting songs saved in the current Spotify user's 'Your Music' library...")
        self.tracks = ""
        self.playlist_name = self.display_name + "'s Saved Songs - API"
        self.playlist_description = "List of the songs saved in the current Spotify user's 'Your Music' library, for easy sharing."
        limit = 50
        offset = 0
        # print("> token : " + self.spotify_token)
        available_songs = True
        
        self.create_playlist()
        
        while (available_songs):
            query = "https://api.spotify.com/v1/me/tracks?limit={}&offset={}".format(str(limit),str(offset))
            response = requests.get(query, headers={"Content-Type" : "application/json",
                                                    "Authorization" : "Bearer {}".format(self.spotify_token)})
                                                    
            response_json = response.json()
            
            print("> 'Your Music' library offset: " + str(offset))
            
            if len(response_json["items"]) > 0:
                for i in response_json["items"]:
                    # self.tracks = i
                    # print(i["track"]["name"] + " : " + i["track"]["uri"])
                    self.tracks += (i["track"]["uri"] + ",")
                offset = offset + limit
            else:
                available_songs = False
                
            if offset > 490:
                available_songs = False
        
            self.tracks = self.tracks[:-1]
            
            self.add_songs_2_playlist()
            
            self.tracks = ""
            
        return

    def get_TasteBreakers(self):
        print("> Creating Taste Breakers Playlist...")
        self.tracks = ""
        self.playlist_name = "{} - Taste Breakers - API".format(self.now)
        self.playlist_description = "Getting out of your usual music zone, some of these tracks may amuse you."
        time_range = "medium_term"
        limit = "1"
        offset = 0
        ## Get user's top artists
        ## query = "https://api.spotify.com/v1/me/top/artists?limit={}&time_range={}".format(limit,time_range)
        ## response = requests.get(query, headers={"Content-Type" : "application/json",
        ##                                         "Authorization" : "Bearer {}".format(self.spotify_token)})
        ## response_json = response.json()
        ## print("> top artists:")
        ## for i in response_json["items"]:
        ##     print(i["name"] + " : " + i["uri"])
        ##     self.tracks += (i["uri"] + ",")

        ## Get Current User's Playlists
        ## query = "https://api.spotify.com/v1/me/playlists?limit={}&offset={}".format(limit, offset)
        
        ## Get Featured Playlists
        ## query = "https://api.spotify.com/v1/browse/featured-playlists?limit={}&offset={}".format(limit, offset)
        ## for i in response_json["playlists"]["items"]:
            ## print(i["name"])
            
        ## Serch for item
        q = "Discover Weekly"
        type = "playlist"
        query = "https://api.spotify.com/v1/search?q={}&type={}&limit={}&offset={}".format(q, type, limit, offset)
        
        response = requests.get(query, headers={"Content-Type" : "application/json",
                                                 "Authorization" : "Bearer {}".format(self.spotify_token)})
        response_json = response.json()
        print("> Serch for item: " + q)
        print("> {} > {}".format(response_json["playlists"]["items"][0]["name"], response_json["playlists"]["items"][0]["external_urls"]["spotify"]))
        #for i in response_json["items"]:
        #    print(i["name"])
            ## print(i["name"] + " : " + i["uri"])
            ## self.tracks += (i["uri"] + ",")
            
        query_tracks = response_json["playlists"]["items"][0]["tracks"]["href"]
        response_tracks = requests.get(query_tracks, headers={"Content-Type" : "application/json",
                                                 "Authorization" : "Bearer {}".format(self.spotify_token)})
        response_tracks_json = response_tracks.json()
        print("> {} tracks:".format(response_json["playlists"]["items"][0]["name"]))
        # print(response_tracks_json["items"][0])
        randy = random.sample(response_tracks_json["items"], 5)
        
        tracks_ids = ""
        
        for i in randy:
            print(i["track"]["name"] + " : " + i["track"]["uri"])
            tracks_ids = tracks_ids + i["track"]["id"] + ","
            self.tracks += (i["track"]["uri"] + ",")
            
        limit = 45
        query_recommendations = "https://api.spotify.com/v1/recommendations?seed_tracks={}&limit={}".format(tracks_ids,limit)
        # print(query_recommendations)
        response_recommendations = requests.get(query_recommendations, headers={"Content-Type" : "application/json",
                                                 "Authorization" : "Bearer {}".format(self.spotify_token)})
        response_recommendations_json = response_recommendations.json()
        
        print("> track recommendations:")
        # print(response_recommendations_json)
        for i in response_recommendations_json["tracks"]:
            print(i["name"] + " : " + i["uri"])
            self.tracks += (i["uri"] + ",")

        return

    def create_playlist(self):
        print("> creating playlist...")
        query = "https://api.spotify.com/v1/users/{}/playlists".format(self.spotify_user_id)
        print("> query: " + query)

        body = json.dumps( {"name" : self.playlist_name,
                            "public" : True,
                            "collaborative" : False,
                            "description" : self.playlist_description})
        
        response  = requests.post(query, headers={"Content-Type" : "application/json", "Authorization" : "Bearer {}".format(self.spotify_token)}, data=body)

        response_json = response.json()
        print ("> create playlist response_json: ")
        print(response_json)
        self.playlist_id = response_json["id"].split(":")[-1]
        print("> Playlist " + self.playlist_name + " : " + self.playlist_id + ", created.")
        #self.playlist_id = playlist_id
        # playlist_id = playlist_id
        return

    def add_songs_2_playlist(self):
        print("> Adding songs to " + self.playlist_id)
        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(self.playlist_id, self.tracks)
        print("> query: " + query)
        
        response = requests.post(query, headers={"Content-Type" : "application/json",
                                                "Authorization" : "Bearer {}".format(self.spotify_token)})
        response_json = response.json()

        print(response_json)
        print("> Songs added")

        return

def lambda_handler(event, context):
    # TODO implement
    
    parameters = json.dumps(event)
    
    url_parameters = event["queryStringParameters"]
    
    print("> getting code parameter")
    code = url_parameters["code"]
    print("> code: " + code)

    wrapped = Spotify_wrapped()
    wrapped.get_token(code)
    wrapped.get_user_id()
    wrapped.get_TasteBreakers()
    wrapped.create_playlist()
    wrapped.add_songs_2_playlist()

    return {
        'statusCode': 200,
#        'body': wrapped.tracks
        'body': json.dumps('Hola ' + wrapped.display_name + ', tu playlist <' + wrapped.playlist_name + '> ha sido creado!')
    }
    
    ##return {
    ##    'statusCode': 200,
    ##    'body': json.dumps('Hello from Lambda! 2 ' + path)
    ##}


## spotify:playlist:37i9dQZEVXcMNt8luM1qxM