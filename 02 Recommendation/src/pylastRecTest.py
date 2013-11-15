import numpy as np
import pylast
import recommendations as rm
from recommtest1 import topMatches, getRecommendations

API_KEY = "b544c9a0541faf9934aef05ab9d48ef3"
network=pylast.get_lastfm_network(api_key = API_KEY)

myArtist = "The Rolling Stones"

# get artist
artist = network.get_artist(myArtist)

# get top fans
topfans = artist.get_top_fans(10)

# extract users from topfans-answer
users = [a.item for a in topfans]

userDict = rm.createLastfmUserDict(users)

#print userDict['LauraKay87']['Red Hot Chili Peppers']
print topMatches(userDict, 'LauraKay87', rm.sim_euclid)
print getRecommendations(userDict, 'LauraKay87', rm.sim_euclid)