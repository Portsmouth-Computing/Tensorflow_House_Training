import urllib.request
import os
import shutil
from multiprocessing import Process
x = 0
procs = []


def append_ids(url, name):
    urllib.request.urlretrieve(url, name)


def get_images(name, path):
    if os.path.isdir(path):
        shutil.rmtree(path)
        os.mkdir(path)
    else:
        os.mkdir(path)

    with open(name, encoding="utf8") as file:
        # print(file)
        for line in file:
            # request(line,path)
            proc = Process(target=request, args=(line,path))
            procs.append(proc)
            proc.start()

def request(line,path):
    proc = os.getpid()
    # print("PID for process is ",proc)
    line = line.strip()
    filename = line.split("/")[-1]
    fullfilename = path + "\\" + filename
    print(path, fullfilename)
    try:
        urllib.request.urlretrieve(line, fullfilename)
        print("did request for "+ str(line) + " on filename " + str(filename))
    except Exception as C:
        print(C)

def return_sub_files(data):
    urllib.request.urlretrieve(
        "http://www.image-net.org/api/text/wordnet.structure.hyponym?wnid=" + data, "temp.txt")
    file2 = open("temp.txt")
    list_temp = file2.readlines()
    if len(list_temp) > 1:
        for x in list_temp:
            string = x[1:10]
            if string[0] == "n":
                file_IDS = open("IDS.txt", mode="a")
                with open("temp.txt") as file_temp:
                    for line in file_temp:
                        if line[0] == "-":
                            print(line, "Was added to IDS.txt")
                            file_IDS.write(line)
                file_IDS.close()
                return False
    else:
        return False


append_ids("http://www.image-net.org/api/text/wordnet.structure.hyponym?wnid=n03544360", "IDS.txt")

with open("IDS.txt") as file:
    for line in file:
        string = line[1:10]
        print(string)
        if string[0] == "n":
            response = return_sub_files(string)
            # print(response)
            if response is False:
                urllib.request.urlretrieve(
                    "http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=" + string, "images_for_" + string + ".txt")
                get_images("images_for_" + string + ".txt", string)



print(counter, "image files were processed")
