import guitarpro as gp
import json


class Specification_Checker:
    def __init__(self):
        pass

    def not_Guitar_Track(self, track):
        if(track.channel.instrument >= 24 and track.channel.instrument <= 31):
            return False
        return True
        #track.channel.instrument        

    def not_Standard_Tuning_Track(self, track):
        standard_tuning = [64, 59, 55, 50, 45, 40]
        #number means string# and value means the natural pitch of the string
        #standard tuning: the value seq should be 64, 59, 55, 50, 45, 40, from string 1 to string 6.            
        for i in range(6):
            if(track.strings[i].value != standard_tuning[i]):
                return True               
        return False


class Gpfile_Tokenizer:
    def __init__(self):
        self.song = None
        self.checker = Specification_Checker()
        return

    def song_injection(self, gpfile):
        try:
            self.song = gp.parse(gpfile)
        except:
            print(f"There is a exception problem with {gpfile}.")

    def parse_to_json_format(self, gpfile):
        song_obj = gp.parse(gpfile)
        song = {}
        for t, track in enumerate(song_obj.tracks):
            if(self.checker.not_Guitar_Track(track) or self.checker.not_Standard_Tuning_Track(track)):
                continue
            song[f"track_{t}"] = {}
            for m, measure in enumerate(track.measures):
                song[f"track_{t}"][f"measure_{m}"] = []
                for v, voice in enumerate(measure.voices):
                    for b, beat in enumerate(voice.beats):
                        tokens_in_a_beat = []
                        for n, note in enumerate(beat.notes):
                            if(note.type == gp.NoteType.tie or note.type == gp.NoteType.rest):
                                continue
                            elif(note.type == gp.NoteType.dead):
                                tokens_in_a_beat.append([note.string, -1])
                            else:
                                tokens_in_a_beat.append([note.string, note.value])
                        song[f"track_{t}"][f"measure_{m}"].append(tokens_in_a_beat)
        with open(f"{gpfile.split('.')[0]}.json", 'w') as jsonfile:
            json.dump(song, jsonfile)
                            

def main():
    Gpfile_Tokenizer().parse_to_json_format("Pokemon - Pokemon.gp4")





if __name__ == "__main__":
    main()




