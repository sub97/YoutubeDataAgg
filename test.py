from googleapiclient.discovery import build
import pyperclip
import json

def getKey():
    with open('C:\\Users\\tsubr\\folders\\Scripts\\YTAgg\\key.txt', 'r') as file:
        API_KEY = file.read()
        file.close()
    return API_KEY

youtube = build("youtube", "v3", developerKey=getKey())

def getChannelDetails(Handle):
    parts = ["brandingSettings", "contentDetails", "contentOwnerDetails", "id","localizations","snippet","statistics","status","topicDetails"]

    request = youtube.channels().list(
        forHandle=Handle,  
        part=",".join(parts),
    )
    response = request.execute()

    print(response["items"][0])  

    if response["pageInfo"]["totalResults"]==0:
        print("Channel Not found")
    
    getVideosFromChannel(response["items"][0]["id"])


def getVideosFromChannel(CHANNEL_ID):
    request = youtube.channels().list(
        id=CHANNEL_ID,
        part="contentDetails",
    )
    response = request.execute()

    uploads_playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    request = youtube.playlistItems().list(
        playlistId=uploads_playlist_id,
        part="snippet",
        maxResults=1000, 
    )
    response = request.execute()
    pyperclip.copy(json.dumps(response))

    print("\n\n"+str(len(response["items"])))

    for item in response["items"]:
        video_id = item["snippet"]["resourceId"]["videoId"]
        video_title = item["snippet"]["title"]
        print(f"Video ID: {video_id}, Title: {video_title}")

getChannelDetails("pewdiepie")