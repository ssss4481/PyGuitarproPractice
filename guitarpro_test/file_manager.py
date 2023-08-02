import os
import shutil
import json
import datetime


#make a copy of dadaGP without duplicated files.

def main():
    with open("./setting.json") as jsonfile:
        setting = json.load(jsonfile)
        File_Manager(setting.get("src"), setting.get("dst")).do_task()

class File_Manager:
    def __init__(self, src: str, dst: str):
        self.file_filter = File_Filter()
        self.path_builder = Path_Builder()
        self.logger = File_Logger()
        self.src = src
        self.dst = dst
    
    def do_task(self):
        self.path_builder.build_path("./log")

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
                print(f"copy {src} to {dst}")
                self.logger.log_copied_File(src)
                shutil.copyfile(src, dst)
            
        self.logger.save()
        return
      

class File_Filter:
    def __init__(self):
        self.logger = File_Logger()
    
    def filt_files(self, files: list[str])->list[str]:
        clean_list = []        
        included_song = set()

        for file in files:            
            origin_name, name_without_duplication_number = self.prune_filename(file)

            if(name_without_duplication_number in included_song):
                self.logger.log_ingnored_File(origin_name, f"{name_without_duplication_number} is already included")
                continue
            
            included_song.add(name_without_duplication_number)

            files_set = set(files)
            for i in [5, 4, 3]:
                gpfile = f"{origin_name}.gp{i}"
                if(gpfile in files_set):
                    clean_list.append(gpfile)
                    break
        
        return clean_list
    
    def prune_filename(self, filename):
        tokens = filename.split('.')
        idx = 0
        while(tokens[idx] not in ["gp3", "gp4", "gp5"] and idx < len(tokens)):
            idx += 1

        origin_name = '.'.join(tokens[0:idx])
        name_without_duplication_number = origin_name

        if(origin_name[-1] == ')'):
            whiteSpaceIdx = len(origin_name)-1
            while(origin_name[whiteSpaceIdx] != ' '):
                whiteSpaceIdx -= 1
            name_without_duplication_number = origin_name[0:whiteSpaceIdx].strip()

        return origin_name, name_without_duplication_number
    
    @DeprecationWarning
    def duplicated_file(self, song):
        tail = song.split(' ')[-1]
        #largest duplicate file in dadaGP is (13).
        for i in range(14):
            if tail == f"({i})":
                return True
        return False

            
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
    
    
class File_Logger:
    ignore_key = "ignored_file"
    copied_key = "copied_key"
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    record = dict()
    record[ignore_key] = []
    record[copied_key] = []    

    def __init__(self) -> None:
        pass

    def log_ingnored_File(self, filename, reason):
        File_Logger.record[self.ignore_key].append([filename, reason])
    
    def log_copied_File(self, filename):
        File_Logger.record[self.ignore_key].append(filename)

    def save(self):
        with open(f"./log/process_record_{File_Logger.current_time}.json",'w') as jsonfile:
            json.dump(File_Logger.record, jsonfile)

        


if __name__ == "__main__":
    main()