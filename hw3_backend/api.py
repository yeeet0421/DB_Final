#### youtube search by keywords ###
# refer to : https://developers.google.com/youtube/v3/docs/search/list
# Get some information:
# 1.videoid
# 2.title
# 3.published_time
# 4.channel_id
# 5.channel_title
# 6.thumbnail:return image url

def youtube_search(youtube, keyword, result_num):
    search_response = youtube.search().list(q=keyword,
                                            part='id,snippet',
                                            maxResults=result_num,  # at most 50
                                            order='relevance'
                                            ).execute()
    videos = []
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            data = {'videoid': search_result['id']['videoId'],
                    'title': search_result['snippet']['title'],
                    'channel_title': search_result['snippet']['channelTitle'],
                    'thumbnail': search_result['snippet']['thumbnails']['high']['url']}
            videos.append(data)
    return videos