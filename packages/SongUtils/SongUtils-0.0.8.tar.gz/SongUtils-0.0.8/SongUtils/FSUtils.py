import os
import os.path as osp
import shutil
import random
    
def _check_ignore_keywords(curr_path, ignore_keywords):
    for kw in ignore_keywords:
        if kw in curr_path:
            return True
    return False

def get_recur_file_list(root, ignore_keywords=None):
    if (not isinstance(ignore_keywords, list)) and (ignore_keywords is not None):
        print("Argument \"ignore_keywords\" need to be a list")
        raise ValueError
    def recur(path, ignore_keywords=None):
        filesList = os.listdir(path)
        for fileName in filesList:
            fileAbsPath = os.path.join(path, fileName)
            if (ignore_keywords is not None) and (_check_ignore_keywords(fileAbsPath, ignore_keywords)):
                continue
                    
            if os.path.isdir(fileAbsPath):
                all_dirs_list.append(fileAbsPath)
                recur(fileAbsPath, ignore_keywords)
            else:
                all_files_list.append(fileAbsPath)
    all_dirs_list = []
    all_files_list = []
    recur(root, ignore_keywords)
    return all_dirs_list, all_files_list



def split_files(root_files_dir, output_dir, num_per_group, shuffle=False):
    files_list = os.listdir(root_files_dir)
    if shuffle:
        random.shuffle(files_list)
    split_folder_index = 0
    for i, image in enumerate(files_list):
        if i % num_per_group == 0:
            split_folder_index += 1
            currDir = osp.join(output_dir, str(split_folder_index))
        if not osp.isdir(currDir):
            os.mkdir(currDir)
        shutil.copyfile(osp.join(root_files_dir, image), osp.join(currDir, image))

if __name__ == "__main__":
    root = ".."
    all_dirs_list, all_files_list = get_recur_file_list(root, ["git"])
    for i in all_files_list:
        print(i)
    print("*" * 100)
    for i in all_dirs_list:
        print(i)
