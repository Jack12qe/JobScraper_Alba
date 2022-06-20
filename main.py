import os
import csv
import requests
from bs4 import BeautifulSoup
import pprint

alba_url = "http://www.alba.co.kr"


html = requests.get(alba_url)
soup = BeautifulSoup(html.text, "html.parser")

ul = soup.select("#MainSuperBrand > .goodsBox > li")

for li in ul:
    if "appPrInfo" in li["class"] or "noInfo" in li["class"]:
        continue
    info_a = li.select_one("a.goodsBox-info")
    info_url = info_a["href"]
    # title
    info_title = info_a.select_one(".company").get_text().replace("/", "_")
    print(f"{info_title} scraping..")
    info_html = requests.get(info_url)
    info_soup = BeautifulSoup(info_html.text, "html.parser")
    tbody = info_soup.select("#NormalInfo > table > tbody > tr")
    with open(f"{info_title}.csv", "tw", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["place", "title", "time", "pay", "date"])
        for tr in tbody:
            if tr.select_one("td[align='center']") is not None:
                continue
            if "summaryView" in tr["class"]:
                continue
            # place
            place = tr.select_one(".local").get_text()
            # title
            title = tr.select_one(".title > a > .company").get_text()
            # time
            time = tr.select_one(".data").get_text()
            # pay
            pay = (
                tr.select_one(".pay span.payIcon").get_text()
                + " "
                + tr.select_one(".pay span.number").get_text()
            )
            # date
            date = tr.select_one(".regDate").get_text()
            save_obj = {
                "place": place,
                "company": title,
                "time": time,
                "pay": pay,
                "date": date,
            }
            writer = csv.writer(file)
            writer.writerow(list(save_obj.values()))
