import urllib.request
import os
import shutil
x = 0
counter = 0


def append_ids(url, name):
    urllib.request.urlretrieve(url, name)


def get_images(name, path):
    x = 0
    if os.path.isdir(path):
        shutil.rmtree(path)
        os.mkdir(path)
    else:
        os.mkdir(path)
    print(path)
    with open(name, encoding="utf8") as file:
        # print(file)
        for line in file:
            # print(line)
            filename = str(x) + ".jpg"
            fullfilename = path + "\\" + filename
            try:
                urllib.request.urlretrieve(line, fullfilename)
                counter += 1
            except Exception as C:
                pass
            x += 1
    os.remove(name)


def return_sub_files(data):
    urllib.request.urlretrieve(
        "http://www.image-net.org/api/text/wordnet.structure.hyponym?wnid=" + data, "temp.txt")
    file2 = open("temp.txt")
    list_temp = file2.readlines()
    if len(list_temp) > 1:
        # print("Sub sub folder detected", str(data), list_temp)
        for x in list_temp:
            # response = return_sub_files(x)
            string = x[1:10]
            if string[0] == "n":
                # print(response)
                # print("Adding to IDS")
                file_IDS = open("IDS.txt", mode="a")
                with open("temp.txt") as file_temp:
                    for line in file_temp:
                        if line[0] == "-":
                            # print(line, "Was added to IDS.txt")
                            file_IDS.write(line)
                file_IDS.close()
                return False
    else:
        return False


# append_ids("http://www.image-net.org/api/text/wordnet.structure.hyponym?wnid=n03544360", "IDS.txt")

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
            else:
                pass


print(counter, "image files were processed")
