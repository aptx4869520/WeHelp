import urllib.request
import ssl
import json
import csv

chinese_url = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
english_url = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"

try:
    context = ssl._create_unverified_context()

    # 抓中文資料
    with urllib.request.urlopen(chinese_url, context=context) as response:
        chinese_data = response.read().decode("utf-8")

    # 抓英文資料
    with urllib.request.urlopen(english_url, context=context) as response:
        english_data = response.read().decode("utf-8")    

    # 把 JSON 文字轉成 Python 資料
    chinese_hotel_data = json.loads(chinese_data)
    english_hotel_data = json.loads(english_data)

    # 取出真正的旅館列表
    chinese_hotel_list = chinese_hotel_data["list"]
    english_hotel_list = english_hotel_data["list"]

    # 建立英文資料查找表：用 _id 找英文旅館資料
    english_dict = {}

    for hotel in english_hotel_list:
        hotel_id = hotel["_id"]
        english_dict[hotel_id] = hotel

    # 輸出 hotels.csv
    with open("hotels.csv", "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "ChineseName",
            "EnglishName",
            "ChineseAddress",
            "EnglishAddress",
            "Phone",
            "RoomCount"
        ])

        for chinese_hotel in chinese_hotel_list:
            hotel_id = chinese_hotel["_id"]

            english_hotel = english_dict[hotel_id]

            chinese_name = chinese_hotel["旅宿名稱"]
            english_name = english_hotel["hotel name"]

            chinese_address = chinese_hotel["地址"]
            english_address = english_hotel["address"]

            phone = chinese_hotel["電話或手機號碼"]
            room_count = chinese_hotel["房間數"]

            writer.writerow([
                chinese_name,
                english_name,
                chinese_address,
                english_address,
                phone,
                room_count
            ])

    print("hotels.csv 已經建立完成")

    # 建立行政區統計資料
    districts = {}

    for hotel in chinese_hotel_list:
        address = hotel["地址"]
        district = address[3:6]
        room_count = int(hotel["房間數"])

        if district not in districts:
            districts[district] = {
                "hotel_count": 0,
                "room_count": 0
            }

        districts[district]["hotel_count"] += 1
        districts[district]["room_count"] += room_count

    # 輸出 districts.csv
    with open("districts.csv", "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["DistrictName", "HotelCount", "RoomCount"])

        for district_name in districts:
            hotel_count = districts[district_name]["hotel_count"]
            room_count = districts[district_name]["room_count"]

            writer.writerow([district_name, hotel_count, room_count])

    print("districts.csv 已經建立完成")

except Exception as e:
    print("發生錯誤：")
    print(e)