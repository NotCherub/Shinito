#!/usr/bin/env python

"""
    Shinito Project was created to clean out all the remains of torrent files.
"""

try:
    import os
    import re
    import time
    import datetime
    from os.path import isfile, join
    from imdbpie import Imdb

except Exception as ex:
    print('Error! while loading the dependencies. Please make sure you have following dependencies\n')
    print('"imdbpie" : Please install this by using \'pip install imdbpie\' or refer to'
          ' \'https://pypi.org/project/imdbpie/\'\n')
    print('If you face any other problem please refer to \'https://github.com/NotCherub/Shinito\'')

__author__ = "Cherub"
__version__ = "1.7.beta"
__email__ = "mldata.apoorv@gmail.com"
__status__ = "Prototype"
__credit__ = "Dipansh, Cherub"

allVideos = []


class Video:
    """
        Holds the details of all the video files detected by Shinito.
    """

    def __init__(self, name, path, folder):
        """
        :param name: The name of the video file passed as str object.
        :param path: The complete path of the video starting at the program's directory.
        :param folder: The name of the folder that contains the given video file.
        """
        self.init_name = name
        self.stripped_name = re.split('[,. _-]', name)
        self.extension = self.stripped_name[-1]
        self.stripped_name = self.stripped_name[:-1]
        self.path = path
        self.folder = folder
        self.title = None
        self.year = None
        self.imdb_code = None

    def get_imdb(self):
        """
            Gets the IMDb details of the video file.
        :return: None
        """
        try:
            search_query = Imdb().search_for_title(' '.join(self.stripped_name))
        except Exception as ex:
            print('\n\nError! While getting data from IMDb, got the following error\n'
                  'Please make sure you are connected to Internet\n')
            print('\n------------------------------------------------------------------\n')
            print('\n', ex)
            print('\n------------------------------------------------------------------\n')

        poss_year = []

        for part in self.stripped_name:
            if len(part) == 4 and part.isdigit() :
                poss_year.append(part)

        counter = 1
        while len(search_query) == 0:
            self.stripped_name = self.stripped_name[:-counter]
            if len(self.stripped_name) == 0:
                return None
            try:
                search_query = Imdb().search_for_title(' '.join(self.stripped_name))
            except Exception as ex:
                print('\n\nError! While getting data from IMDb, got the following error\n'
                      'Please make sure you are connected to Internet\n')
                print('\n------------------------------------------------------------------\n')
                print('\n', ex)
                print('\n------------------------------------------------------------------\n')

        alpha_name = []
        for part in self.stripped_name:
            if part.isalpha() :
                alpha_name.append(part)

        for search in search_query:
            search['match'] = 0
            if search['year'] in poss_year:
                search['match'] += 1
            if len(alpha_name) == 1 and search['title'] == alpha_name[0]:
                search['match'] += 2

        search_query = sorted(search_query, key= lambda k :k['match'], reverse=True)
        search_query = search_query[0]
        self.imdb_code = search_query['imdb_id']
        self.title = search_query['title']
        self.year = search_query['year']

    def get_name(self, ):
        """
            Sets the self.title variable to movie name + year
        :return:
        """
        movie_name = self.title + ' (' +str(self.year)+').' + self.extension
        self.title = movie_name
        for er in ['>','<', ':', '\"', '\/', '\\', r"|", r"?", r"*" ]:
            if er in self.title :
                self.title.replace(er, ' ')

    def display(self):
        """
            Displays all the information stored in the class of particular object.
        :return: None
        """
        print('Original Name :', self.init_name)
        print('Name Expected :', self.title)
        print('Year :', self.year)
        print('IMDb ID :', self.imdb_code)


def ret_dir(given_path):
    """
    :return: Returns the directory that contain the given file
    """
    _, folder = os.path.split(given_path)
    return folder


def is_video(name):
    """
    :param name: The complete name and path of the file to be checked.
    :return: is Video or not
    """
    point = name.rfind('.')
    extension = name[point+1:]
    if extension == 'mkv' or extension == 'mp4' or extension == 'avi' or extension == 'flv':
        return True
    else:
        return False


def ret_subfolder(given_path):
    """
    :param given_path: The path whose subfolders and files are to be returned.
    :return: A tuple of lists of the folders and files in the given directory.
    """
    folds_list = []
    files_list = []
    for files in os.listdir(given_path):
        if isfile(join(given_path,files)):
            files_list.append(files)
        else:
            folds_list.append(files)

    return folds_list, files_list


def spider(given_path):
    """
        Crawls all the way to every sub-folder and files and detects them.
    :param given_path:The root directory where to search for items
    :return: None
    """
    # print('-------------------------------------------------------')
    # print('Working Directory : ', given_path)
    folds_list, files_list = ret_subfolder(given_path)

    if len(files_list) != 0:
        # print("Number of Folder : ", len(folds_list),"\t", "Number of files", len(files_list), '\n')
        vid_count =0
        # sub_count =0
        for files in files_list:
            if is_video(files):
                vid_count += 1
                allVideos.append(Video(files, join(given_path, files), ret_dir(given_path)))

    for fold in folds_list:
        spider(join(given_path, fold))


erase = '\x1b[1A\x1b[2K'

print('\n------------------------------------------------------------------\n')
print('BEWARE THAT THIS IS A BETA VERSION AND IS PRONE TO RUN-TIME ERRORS.')
print('THIS VERSION OF PROGRAM WILL NOT MAKE ANY CHANGES TO YOUR COMPUTER EXCEPT,')
print('YOU MAY FOUND AN EXTRA FILE NAMED "Data.txt" AFTER COMPLETION OF THE PROGRAM.')
print('PLEASE EMAIL THAT FILE TO THIS EMAIL ID : mldata.apoorv@gmail.com.\n')
print('-----------------------------------------------------------------\n')
n = input('Enter any key to begin crawling\n')
print('The current Directory will be represented by "." ')
now = datetime.datetime.now()

spider('.')
print('Crawling Complete. Total Video Files found : ', len(allVideos))
time.sleep(2)
print('\n------------------------------------------------------------------\n')

print('Now Starting to get names from IMDb database. Please make sure you are connected to Internet')
print('\nThis may take some time.\n')
time.sleep(1)
print('\n------------------------------------------------------------------\n')

f = open('Data.txt', 'w+')
f.write('This test was done on :' + str(now))
f.write('\n\nTotal Video Files Found : '+str(len(allVideos))+'\n\n')

for vid in allVideos:
    print('Working on Video Number :', allVideos.index(vid)+1, 'out of :', len(allVideos))
    print('File Name : ', vid.init_name)
    print('Searching...')
    vid.get_imdb()
    print(erase)
    print('Probable Name : ', vid.title)
    f.write(vid.init_name + '-->' + vid.title + '\n\n')
    print('\n------------------------------------------------------------------\n')
endtime = datetime.datetime.now()

accuracy = float(input('\n\nPlease enter how many files were correctly named by the program :'))
accuracyPercent = accuracy*100/len(allVideos)
print('Accuracy Percentage = ', accuracyPercent)
f.write('\n\nTotal Execution Time : '+str(endtime-now))
f.write('\n\n\n ACCURACY : '+str(accuracy)+' ACCURACY PERCENTAGE : '+str(accuracyPercent))
f.close()
print('\n------------------------------------------------------------------\n')
print('PLEASE EMAIL THE "Data.txt" FILE')
print('\n------------------------------------------------------------------\n')
