import api,auth_api
import pandas as pd
import os
import psycopg2
import pycld2 as cld2
import draw_map

def download(service,keyword,result_num):
    videos = api.youtube_search(service, keyword, result_num)
    videos = pd.DataFrame(videos)
    printable_str = ''.join(x for x in videos['title'][0] if x.isprintable())
    lan_detect = []
    for i in videos['title']:
        printable_str = ''.join(x for x in str(i) if x.isprintable())
        lan_detect.append(cld2.detect(printable_str)[2][0][0])
    videos['lang_detect'] = lan_detect
    videos_selected = pd.DataFrame()
    for i, grp in videos.groupby("videoid"):
        videos_selected = pd.concat([videos_selected,grp[(grp['lang_detect']=="ENGLISH") ]], axis=0)
    videos_selected.drop(['lang_detect'], axis=1, inplace=True)
    return videos_selected

def get_comment_threads(youtube, vid, comments):
    try:
        results = youtube.commentThreads().list(
            part="snippet",#replies
            videoId=vid,
            order="relevance",
            maxResults=100, # at most 100 comments
            textFormat="plainText"## or 'html'
        ).execute()
        for item in results["items"]:
            if 'snippet' in item:
                data = {
                    'commentId':item['id'],
                    'videoId':item['snippet']['videoId'],
                    'textDisplay':item['snippet']['topLevelComment']['snippet']['textDisplay'],
                    'publishedAt':item['snippet']['topLevelComment']['snippet']['publishedAt'],
                    'authorDisplayName':item['snippet']['topLevelComment']['snippet']['authorDisplayName'],#
                    'authorProfileImageUrl':item['snippet']['topLevelComment']['snippet']['authorProfileImageUrl'],#
                    'likeCount':int(item['snippet']['topLevelComment']['snippet']['likeCount'])
                }
                comments.append(data)
    except Exception as e: print(e)
    return comments

def download_comments(service,keyword,result_num):
    print("Keyword = ", keyword)
    print("num = ", result_num)
    vids = download(service,keyword,result_num)
    vlist = list(vids['videoid'])
    ## save youtube quota
    # vlist = ['gElfIo6uw4g']
    comments_all = []
    for i in range(len(vlist)):
        print(vlist[i])
        comments = []
        comments = get_comment_threads(service, vlist[i], comments)
        if comments:
            print(len(comments))
            comments_all += comments
        else:
            print("videoid: ",vlist[i]," do not allow/have comments!")
    pd_comments_all = pd.DataFrame(comments_all)
    return vids, pd_comments_all

def build_func():
    keyword = input("Enter keyword: ")
    result_num = 20
    return keyword, result_num

def main():
    keyword, result_num = build_func()
    service_personal = auth_api.get_authenticated_service()
    vids, comments_all = download_comments(service_personal,keyword,result_num)
    ## save quota
    os.environ['DB_USERNAME'] = "postgres"
    os.environ['DB_PASSWORD'] = 'eh20010421'
    comments_all = comments_all[['commentId','videoId','textDisplay','publishedAt','authorDisplayName','authorProfileImageUrl','likeCount']]
    # remove comments contain code
    remove_code = ['pip', 'install', 'ValueError:', 'import']
    ## lang detect, only use english comments
    comments_all = comments_all[comments_all["textDisplay"].str.contains('|'.join(remove_code)) == False]
    printable_str = ''.join(x for x in comments_all['textDisplay'][0] if x.isprintable())
    lan_detect = []
    for i in comments_all['textDisplay']:
        printable_str = ''.join(x for x in str(i) if x.isprintable())
        lan_detect.append(cld2.detect(printable_str)[2][0][0])
    comments_all['lang_detect'] = lan_detect
    comments_selected = pd.DataFrame()
    for i, grp in comments_all.groupby("videoId"):
        comments_selected = pd.concat([comments_selected,grp[(grp['lang_detect']=="ENGLISH") ].sort_values(['likeCount'])], axis=0)
    comments_selected.drop(['lang_detect'], axis=1, inplace=True)
    print("Connecting database")
    conn = psycopg2.connect(
        host="database-1.cgrpfuvmepy7.us-east-1.rds.amazonaws.com",
        database="hw3",
        port='5432',
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])
    
    cur = conn.cursor()
    conn.autocommit=True
    print("write comment table...")
    # comment table
    cur.execute("DROP TABLE IF EXISTS comments;")
    cur.execute('''
        CREATE TABLE comments (
        commentId varchar (125) PRIMARY KEY,
        videoId varchar (100) NOT NULL,
        textDisplay text NOT NULL,
        publishedAt DATE NOT NULL,
        authorDisplayName varchar (150) NOT NULL,
        authorProfileImageUrl varchar (200) NOT NULL,
        likeCount integer NOT NULL)''')
    cur.execute("CREATE INDEX c_ind on comments(commentId);")
    for index, row in comments_selected.iterrows():
        cur.execute('''INSERT INTO comments (commentId,videoId,textDisplay,publishedAt,
                                            authorDisplayName,authorProfileImageUrl,likeCount) 
                        VALUES (%s,%s,%s,%s,%s,%s,%s);''', (row['commentId'],row['videoId'],row['textDisplay'],row['publishedAt'],row['authorDisplayName'],row['authorProfileImageUrl'],row['likeCount']))
    print("write video table...")
    # video table
    cur.execute("DROP TABLE IF EXISTS videos;")
    cur.execute('''
        CREATE TABLE videos (
        videoid varchar (125) PRIMARY KEY,
        title varchar (200) NOT NULL,
        channel_title varchar (200) NOT NULL,
        thumbnail varchar (200) NOT NULL)''')
    cur.execute("CREATE INDEX v_ind on videos(videoid);")
    for index, row in vids.iterrows():
        cur.execute('''INSERT INTO videos (videoid,title,channel_title,thumbnail) 
                        VALUES (%s,%s,%s,%s);''', (row['videoid'],row['title'],row['channel_title'],row['thumbnail']))
    

    # closing connection
    cur.close()
    conn.close()
    print("connect finish")
    draw_map.get_map()
    vids.to_csv('./comment_map/vids.csv', index=False)

if __name__ == '__main__':
    main()










