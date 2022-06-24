# DB_Final
## Manual
### Non Library Prerequisites
In order to use YouTube API, please apply project.json and client_secret.json from Google Cloud Platfrom. <br/ > After application, please put them under the hw3_backend folder and change the commented part in auth.api under hw3_backend.<br />
Related Instructions: <br />
https://console.cloud.google.com/?hl=zh-TW<br />
https://cloud.google.com/video-intelligence/docs/common/auth 

Please change the commented parts in download_comments.py and draw_map.py under hw3_backend. For example: database host, name, port, password...

Download Ruby on Rails.<br />
Instructions:<br />
https://web.stanford.edu/~ouster/cgi-bin/cs142-fall10/railsInstall.php

### Library Prerequisites
```
pip3 install pandas
pip3 install psycopg2
pip3 install pycld2
pip3 install numpy
pip3 install glob
pip3 install pyvis
pip3 install yake
```

### Instructions
You can run both backend and frontend to get a complete experience from the application; however, you can run the frontend by itself. It would show the results of using "sql injection" as the keyword. #put some markdown notice effect
<br />
Open hw3_backend folder in terminal and run:
```
python3 download_comments.py <keyword>
```
to create needed files. This process may take 5-10 min.
Please change \<keyword> to the keyword you would like to search (on YouTube).

Open hw3_frontend folder in terminal and run:
```
rails s
```
to run the frontend application.

Open
```
localhost:3000
```
on Google Chrome to demo the application

## Function
### Comment Map
Comment map 是以憑藉 pycld2 判定語言為英文的評論內容，經由 yake 找出所有評論前 30 個主要在講的主題，最後以主題出現在評論裡的次數作為 node 的大小，以主題出現於同評論為 link，透過 pyvis 繪出的圖。Comment map 的目的是希望能了解一開始查詢的 keyword 找到的影片底下的留言中主要談論的主題，以此，使用者也可以了解如果想進一步了解這個 keyword 可以往什麼方向查詢。
### Top Comments
Top Comments 的頁面是從找到的影片中，以 SQL query 找到的該影片最高讚數的評論，顯示該影片的封面圖、標題、作者以及最高讚數的評論的作者、作者頭像、評論發佈時間、評論、讚數，而使用者可以藉由點擊影片的封面圖連接到該影片的 YouTube 介面。Top comments 的目的是希望使用者能以其作為了解影片的其中一個媒介。