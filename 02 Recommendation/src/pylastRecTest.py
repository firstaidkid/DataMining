import numpy as np
import pylast

API_KEY = "b544c9a0541faf9934aef05ab9d48ef3"
network=pylast.get_lastfm_network(api_key = API_KEY)

myArtist = "The Rolling Stones"

# get artist
artist = network.get_artist(myArtist)

# get top fans
topfans = artist.get_top_fans(10)

# extract users from topfans-answer
users = [a.item for a in topfans]
