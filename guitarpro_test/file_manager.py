import os
import shutil
import json

#make a copy of dadaGP without duplicated files.

m = 0

class File_Manager:
    def __init__(self, src: str, dst: str):
        self.file_filter = File_Filter()
        self.path_builder = Path_Builder()
        self.src = src
        self.dst = dst
    
    def do_task(self):
        for src_root, dirs, files in os.walk(self.src):
            if(src_root == self.src or len(files) == 0):
                continue            

            commonpath = os.path.commonpath([src_root, self.dst])
                    
            suffix = src_root.replace(commonpath, '') 

            if(suffix[0] == '/'):
                suffix = suffix[1::]
            dst_root = os.path.join(self.dst, suffix)
            #print(dst_root)
            self.path_builder.build_path(dst_root)
            clean_files = self.file_filter.filt_files(files)
            
            for file in clean_files:
                src = os.path.join(src_root, file)
                dst = os.path.join(dst_root, file)
                #print(f"copy {src} to {dst}")
                #shutil.copyfile(src, dst)
        print("tail------", m)
        return


        

class File_Filter:
    def __init__(self):
        pass
    
    def filt_files(self, files: list[str])->list[str]:
        clean_list = []        
        contained_song = set()

        for file in files:
            song = file.split('.')[0]

            if(song in contained_song):
                continue
            
            contained_song.add(song)

            if(self.duplicated_file(song)):
                continue            

            for i in [5, 4, 3]:
                gpfile = f"{song}.gp{i}"
                if(gpfile in files):
                    clean_list.append(gpfile)
                    break
        
        return clean_list
    
    def duplicated_file(self, song):
        global m
        tail = song.split(' ')[-1]        
        for i in range(14):
            if tail == f"({i})":
                return True

            
class Path_Builder:        
    def __init__(self):
        pass

    def build_path(self, path: str):
        if(os.path.isdir(path)):
            return
        
        dirname = ""
        for d in path.split('/'):
            dirname += f"{d}"
            if(self.is_creatable_dir(dirname)):
                os.mkdir(dirname)
            dirname += '/'        

    def is_creatable_dir(self, path):
        return os.path.isdir(os.path.dirname(path)) and not os.path.exists(path)            

def main():
    with open("./setting.json") as jsonfile:
        setting = json.load(jsonfile)
        File_Manager(setting.get("src"), setting.get("dst")).do_task()

if __name__ == "__main__":
    main()