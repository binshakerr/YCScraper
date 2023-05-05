import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import pandas as pd
import string

load_dotenv()
PROXY = os.getenv("PROXY")
proxies = {
    "http": PROXY,
    "https": PROXY
}

headers = {
    'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Origin': 'https://www.ycombinator.com',
    'Referer': 'https://www.ycombinator.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'accept': 'application/json',
    'content-type': 'application/x-www-form-urlencoded',
    'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

params = {
    "x-algolia-agent": "Algolia for JavaScript (3.35.1); Browser; JS Helper (3.11.3)",
    "x-algolia-application-id": "45BWZJ1SGC",
    "x-algolia-api-key": "Zjk5ZmFjMzg2NmQxNTA0NGM5OGNiNWY4MzQ0NDUyNTg0MDZjMzdmMWY1NTU2YzZkZGVmYjg1ZGZjMGJlYjhkN3Jlc3RyaWN0SW5kaWNlcz1ZQ0NvbXBhbnlfcHJvZHVjdGlvbiZ0YWdGaWx0ZXJzPSU1QiUyMnljZGNfcHVibGljJTIyJTVEJmFuYWx5dGljc1RhZ3M9JTVCJTIyeWNkYyUyMiU1RA=="
}


results = []
for i in list(string.ascii_letters):
    data = '{"requests":[{"indexName":"YCCompany_production","params":"facets=%5B%22top_company%22%2C%22isHiring%22%2C%22nonprofit%22%2C%22highlight_black%22%2C%22highlight_latinx%22%2C%22highlight_women%22%2C%22batch%22%2C%22industries%22%2C%22subindustry%22%2C%22regions%22%2C%22tags_highlighted%22%2C%22tags%22%2C%22status%22%2C%22app_video_public%22%2C%22demo_day_video_public%22%2C%22app_answers%22%2C%22question_answers%22%5D&hitsPerPage=1000&maxValuesPerFacet=1000&page=0&query='+i+'&tagFilters="}]}'

    response = requests.post(
        'https://45bwzj1sgc-dsn.algolia.net/1/indexes/*/queries',
        headers=headers,
        data=data,
        params=params
    )
    results += response.json()["results"][0]["hits"]

df = pd.DataFrame(results)
df = df.drop_duplicates(subset=['slug'])
df.to_csv("yc_scraper.csv")
