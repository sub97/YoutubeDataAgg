from googleapiclient.discovery import build
import pyperclip
import json
import os

def getKey():
    with open('C:\\Users\\'+os.getenv("USERNAME")+'\\Desktop\\key.txt', 'r') as file:
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

def getUploadsFromChannel(response):
    
    uploads_playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
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

    getVideoComments(getVideoID(response["items"][0]))
    
    #getVideoDetails(",".join(videoIDList))


def getVideoDetails(videoIDs):
    parts = ["contentDetails","id","liveStreamingDetails","localizations","player","recordingDetails","snippet","statistics","status","topicDetails"]

    request = youtube.videos().list(
        id=videoIDs,
        part=",".join(parts),
    )
    response = request.execute()

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
            pyperclip.copy(str(response))
            print(response)

            for item in response["items"]:            
                COMMENTS.append(item['snippet']['topLevelComment']['snippet']['textOriginal'])
            
            NEXT_PAGE_TOKEN = response.get('nextPageToken')
            if not NEXT_PAGE_TOKEN:
                break
        except Exception as e:
            print(f"An exception occurred: {str(e)}")
            break

    print('\n'.join(COMMENTS))

getChannelDetails("@ThinkMediaTV")