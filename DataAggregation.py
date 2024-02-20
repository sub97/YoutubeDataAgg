from googleapiclient.discovery import build
import concurrent.futures
import os
import argparse
import sys

def getKey():
    with open('C:\\Users\\'+os.getenv("USERNAME")+'\\Desktop\\key.txt', 'r') as file: #key stored locally
        API_KEY = file.read()
        file.close()
    return API_KEY

youtube = build("youtube", "v3", developerKey=getKey())

def getChannelSubscriberCount(channelInfo):
    return channelInfo["statistics"]["subscriberCount"]

def getChannelTitle(channelInfo):
    return channelInfo["snippet"]["title"]

def getChannelUniqueID(channelInfo):
    return channelInfo["id"]

def getProfileBio(channelInfo):
    return channelInfo["snippet"]["description"]

def getVideoTitle(videoInfo):
    return videoInfo["snippet"]["title"]

def getVideoID(videoInfo):
    return videoInfo["snippet"]["resourceId"]["videoId"]

def getVideoViewCount(videoInfo):
    return videoInfo["statistics"]["viewCount"]

def getVideoLikeCount(videoInfo):
    return videoInfo["statistics"]["likeCount"]

def getVideoCommentCount(videoInfo):
    return videoInfo["statistics"]["commentCount"]


def getChannelDetails(Handle):

    if Handle.find('.com'):
        Handle = Handle[Handle.find('.com/')+len('.com/'):]

    if Handle.endswith("/"): 
        Handle = Handle[:-1] #just getting the channel handle only

    print('retriving for '+Handle)

    parts = ["brandingSettings", "contentDetails", "contentOwnerDetails", "id","localizations","snippet","statistics","status","topicDetails"]

    request = youtube.channels().list(
        forHandle=Handle,  
        part=",".join(parts),
    )
    response = request.execute()

    if response["pageInfo"]["totalResults"]==0:
        print("Channel Not found")

    channelInfo = response["items"][0]
    
    getUploadsFromChannel(response)

def getUploadsFromChannel(uploads):
    
    uploads_playlist_id = uploads["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    parts = ["contentDetails", "id", "snippet","status"]

    request = youtube.playlistItems().list(
        playlistId=uploads_playlist_id,
        part=",".join(parts),
        maxResults=50, 
    )
    response = request.execute()

    videoIDList = []

    for item in response["items"]:
        videoIDList.append(getVideoID(item))

    getVideoComments(getVideoID(response["items"][0])) #testing only for one video to get comment. else I will exhaust 10,000 google api quota
    
    getVideoDetails(",".join(videoIDList))


def getVideoDetails(videoIDs):
    parts = ["contentDetails","id","liveStreamingDetails","localizations","player","recordingDetails","snippet","statistics","status","topicDetails"]

    request = youtube.videos().list(
        id=videoIDs,
        part=",".join(parts),
    )
    response = request.execute()

    return response

def getVideoComments(videoID):
    MAX_RESULTS = 100
    NEXT_PAGE_TOKEN = ''
    COMMENTS = []

    while True:
        try:
            request = youtube.commentThreads().list(
                part='snippet',
                videoId=videoID,
                maxResults=MAX_RESULTS,
                pageToken=NEXT_PAGE_TOKEN,
                textFormat='plainText'
            )
            response = request.execute()
            print("comment:-:"+str(response))

            for item in response["items"]:   
                commentText = item['snippet']['topLevelComment']['snippet']['textOriginal']
                who = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
                array = [commentText,who]
                COMMENTS.append(array)
            
            NEXT_PAGE_TOKEN = response.get('nextPageToken')
            if not NEXT_PAGE_TOKEN:
                break
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
            break

    for comment in COMMENTS:
        print(comment[0]+" by:-: "+comment[1])

    return COMMENTS

def main(channelIDs):
    print(arguments)

    if channelIDs.find(','): #batch processing
        channel = channelIDs.split(',')
        if (len(channel)>500): #only 10000 requests are available per day. hence, we have narrowed down number of channels can only be 500, as we cannot predict how many comments will be present for each video
            print("Can only process 2000 channels in a day")
            return
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(processMultipleChannels, channel)
    else:
        getChannelDetails(channelIDs)

def processMultipleChannels(channel):
    getChannelDetails(channel)


#if __name__ == "__main__":
#    main('https://www.youtube.com/@ThinkMediaTV,https://www.youtube.com/@AutoFocus,https://www.youtube.com/@cut,https://www.youtube.com/@LofiGirl')

parser = argparse.ArgumentParser(description="Retrieves info from YouTube Channels")
parser.add_argument("-c", "--channels", type=str, help="Enter Channel Id(s) to fetch data from")

arguments = parser.parse_args()

if len(arguments.channels) < 1:
    raise SystemExit("No ChannelId passed. Use '-h' flag for assistance.")

main(arguments.channels)
