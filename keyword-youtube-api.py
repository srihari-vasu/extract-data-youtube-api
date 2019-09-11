from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

import csv

#The API requirements , ie , key and service name
DEVELOPER_KEY = "" 			# Insert your developer key
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

#data obtained from the search
videos = []
vdata = []
cha = []
cdata = []
playlists = []
pdata = []

#logger initialization
import logging
logger = logging.getLogger('classimp')
hdlr = logging.FileHandler('/var/tmp/classimp.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)

class youtubeop :
    
    #initialization for variables in the class 
    def __init__(self):
        self.videos = []
        self.cha = []
        self.playlists = []

    #search function to get all the meta data for the particular search
    def yt_search(self,options):
         youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY) #connection establishment with youtube
         search_response = youtube.search().list(
    q=options.q,
    part="id,snippet",
    maxResults=options.max_results
  ).execute()#executes the search on the API
         for search_result in search_response.get("items", []):
             if search_result["id"]["kind"] == "youtube#video": #checks if its a video
                  videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                 search_result["id"]["videoId"]))
                  vdata.append("%s" % search_result)
             elif search_result["id"]["kind"] == "youtube#channel": #checks if its a channel
                  cha.append("%s (%s)" % (search_result["snippet"]["title"],
                                   search_result["id"]["channelId"]))
                  cdata.append("%s" % search_result)
             elif search_result["id"]["kind"] == "youtube#playlist": #checks if its a playlist
                  playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                    search_result["id"]["playlistId"]))
                  pdata.append("%s" % search_result)

    #to print the obtained list of videos,channels and playlists
    def yt_print(self):
        print "Videos:\n", "\n".join(videos), "\n"
        print "Channels:\n", "\n".join(cha), "\n"
        print "Playlists:\n", "\n".join(playlists), "\n"

    #to save the obtained metadata into a csv file
    def yt_save(self,name) :
        logger.setLevel(logging.INFO)
        logger.info('The keyword(s) saved in file : %s' % name)
        #to save in csv file
        with open(name+'.csv','wb') as csvfile:
                  spamwriter = csv.writer(csvfile,delimiter=' ')
                  spamwriter.writerow("VIDEOS");
                  for i in range(len(vdata)):
                         spamwriter.writerow(vdata[i])
                  spamwriter.writerow("CHANNELS");
                  for i in range(len(cdata)):
                         spamwriter.writerow(cdata[i])
                  spamwriter.writerow("PLAYLISTS");
                  for i in range(len(pdata)):
                         spamwriter.writerow(pdata[i])


if __name__ == "__main__":
    c=True
    Test = Module()
    while c is True :
        print "MENU"
        print "1.Search"
        print "2.Save"
        print "3.Print"
        print "4.Exit"
        print "Choice "
        n = int(raw_input())
        try:
            if n==1 :
               print "Enter keyword"
               a=raw_input()
               logger.setLevel(logging.INFO)
               logger.info('The keyword(s) used : %s' % a)
               argparser.add_argument("--q",help="Search term",default=a)
               argparser.add_argument("--max-results",help="Max results",default=30)
               args = argparser.parse_args()
               Test.yt_search(args)
            elif n==2:
                print "Enter file name"
                a=raw_input()
                Test.yt_save(a)
            elif n==3:
                Test.yt_print()
            else:
                c=False
        except HttpError, e:
            logger.setLevel(logging.ERROR)
            logger.error('An HTTP error %d occurred:\n%s' %(e.resp.status,e.content))
