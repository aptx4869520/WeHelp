import urllib.request
import ssl
import csv
import os
from bs4 import BeautifulSoup

# PTT Steam 版首頁
url = "https://www.ptt.cc/bbs/Steam/index.html"

try:
    # 建立 SSL 設定，避免部分電腦出現憑證錯誤
    context = ssl._create_unverified_context()

    # 用來存放所有文章資料
    data = []

    current_folder = os.path.dirname(__file__)

    csv_path = os.path.join(current_folder, "articles.csv")

    # 抓 3 頁資料：最新頁、上頁、上上頁
    for i in range(3):
        print("目前頁面：", url)

        next_url = None

        # 建立請求，加入 User-Agent 讓程式比較像一般瀏覽器
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        # 讀取列表頁 HTML
        with urllib.request.urlopen(request, context=context) as response:
            html = response.read().decode("utf-8")

        # 把 HTML 轉成 BeautifulSoup 可以解析的格式
        soup = BeautifulSoup(html, "html.parser")
        
        # 找出這一頁所有文章區塊
        articles = soup.find_all("div", class_="r-ent")

        # 找出上方的按鈕，用來取得「上頁」連結
        btns = soup.find_all("a", class_="btn wide")

        for btn in btns:
            if "上頁" in btn.text:
                next_url = "https://www.ptt.cc" + btn["href"]

        # 逐一處理每篇文章
        for article in articles:
            title = article.find("div", class_="title")
            nrec = article.find("div", class_="nrec")

            # 找文章連結
            link = title.find("a")

            # 如果文章沒有被刪除，才進入內頁抓完整時間
            if link != None:
                article_url = "https://www.ptt.cc" + link["href"]

                # 建立文章內頁請求
                article_request = urllib.request.Request(
                    article_url,
                    headers={
                        "User-Agent": "Mozilla/5.0"
                    }
                )

                # 讀取文章內頁 HTML
                with urllib.request.urlopen(article_request, context=context) as response:
                    html = response.read().decode("utf-8")

                # 解析文章內頁
                article_soup = BeautifulSoup(html, "html.parser")

                # 找出作者、看板、標題、時間等資訊
                meta_values = article_soup.find_all("span", class_="article-meta-value")

                # 第 4 筆通常是完整文章時間
                if len(meta_values) >= 4:
                    article_time = meta_values[3].text.strip()
                else:
                    article_time = ""

                # 整理成一筆文章資料
                article_data = {
                    "title": title.text.strip(),
                    "nrec": nrec.text.strip(),
                    "time": article_time
                }    

                # 加進總資料 list
                data.append(article_data)

        # 這一頁處理完後，下一輪改抓上頁
        if next_url != None:
            url = next_url        

    # 將資料寫入 CSV
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        
        # 寫入欄位名稱
        writer.writerow(["ArticleTitle", "LikeCount", "PublishTime"])
        
        # 寫入每一篇文章資料
        for item in data:
            writer.writerow([item["title"], item["nrec"], item["time"]])

    print("CSV 檔案已建立，共", len(data), "筆資料")
    print("檔案位置：", csv_path)

except Exception as e:
    print("Error occurred:")
    print(e)        