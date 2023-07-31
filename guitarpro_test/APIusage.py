import guitarpro as gp

 
def try_get_info():
    song_obj = gp.parse("Pokemon - Pokemon.gp4")
    measures = song_obj.tracks[0].measures
    print("m, v, b, n, note")
    for m, measure in enumerate(measures):
        for v, voice in enumerate(measure.voices):
            for b, beat in enumerate(voice.beats):
                for n, note in enumerate(beat.notes):
                    print(m, v, b, n, note)
    
    exit()
    for o in a[0].voices[0].beats:
        print(o)

def example(gpfile):
    def get_tracks(song):
        print("----------------------get_tracks----------------------")
        print(song.tracks)
        print("----------------------get_tracks----------------------")        
    
    def get_instrument_type_from_track(track):
        print("----------------------get_instrument_type_from_track----------------------")        
        print(track.channel.instrument)
        print("----------------------get_instrument_type_from_track----------------------")
    
    def check_the_tuning_of_tracks_string(track):
        print("----------------------check_the_tuning_of_tracks_string----------------------")   
        isStandard = True        
        standard_tuning = [64, 59, 55, 50, 45, 40]
        #number means string# and value means the natural pitch of the string
        #standard tuning: the value seq should be 64, 59, 55, 50, 45, 40, from string 1 to string 6.            
        for i in range(6):
            if(track.strings[i].value != standard_tuning[i]):
                isStandard = False
        print(isStandard)
        print("----------------------check_the_tuning_of_tracks_string----------------------")   


                  
        
    
    song_obj = gp.parse(gpfile)
    get_tracks(song_obj)
    get_instrument_type_from_track(song_obj.tracks[0])
    check_the_tuning_of_tracks_string(song_obj.tracks[0])
    

def run():
    #example("Pokemon - Pokemon.gp4")
    try_get_info()
    
    
    
    
if __name__ == "__main__":
    run()

