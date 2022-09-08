import ChurchtoolsAPI

ctApi = ChurchtoolsAPI.ChurchToolsAPI()

# Example for editing the key of a song
print("Edit Arrangement...")
ctApi.editArrangementKeyForSongName("Danke", "G")

# Example for returning a whole song
print("Print song...")
print(ctApi.findSongByName("Danke"))

# Example for returning an arrangement
print("Print arrangement...")
print(ctApi.findStandardArrangementBySongName("Danke"))