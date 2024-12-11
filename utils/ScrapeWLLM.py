import os
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import google.generativeai as genai
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

class ScrapeWLLM:
    def __init__(self, list_url:list) -> None:
        self.list_url = list_url
        self.model = genai.GenerativeModel(
            "gemini-1.5-flash",
            generation_config = {"response_mime_type": "application/json"} 
        )
        self.session = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

    def scrape(self) -> list:
        l_result = []
        for url in self.list_url:
            result = self.fetch_html(url)
            l_result.append(result)
        return l_result

    def fetch_html(self, url:str) -> dict:
        print(f"Fetching URL: {url}")
        try:
            response = self.session.get(url)
            response.raise_for_status()
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')

            return self.call_gemini(soup)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the URL: {e}")
            return [{"message":f"Error fetching the URL: {e}"}]
    def call_gemini(self, html_content:str) -> dict:
        prompt = """
下記のHTMLの中から.webmの動画URL、サムネイルURL、レシピタイトル、説明文、調理時間、費用目安、材料名、分量、手順、ポイントを抽出してください。
{html_content}
Result = {{
    'videoLink':string,
    'thumbnail':string,
    'recipe_title':string,
    'description':string,
    'cooking_time':numer,
    'cost':number,
    'ingredients':list,
    'instruction':list,
    'point':string,
    'review':list,
}}
Return: list[Result]
""".format(html_content=html_content)
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            return [{"message": "Invalid JSON response from Gemini"}]
        except Exception as e:
            print(f"Error calling Gemini: {e}")
            return [{"message": f"Error calling Gemini: {e}"}]
