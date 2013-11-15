import numpy as np
import pylast

API_KEY = "b544c9a0541faf9934aef05ab9d48ef3"
API_SECRET = "c9240638690dea0384baa7e5c0a6b489"

network=pylast.get_lastfm_network(api_key = API_KEY, api_secret = API_SECRET)
artist = network.get_artist("Backstreet Boys")
topAlbums = artist.get_top_albums()