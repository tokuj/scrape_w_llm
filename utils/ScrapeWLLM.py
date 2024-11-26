import os
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

class ScrapeWLLM:
    def __init__(self, list_url:list) -> None:
        self.list_url = list_url
    def scrape(self) -> list:
        l_result = []
        for url in self.list_url:
            result = self.fetch_html(url)
            l_result = l_result + result
        return l_result

    def fetch_html(self, url:str) -> list:
        print(url)
        try:
            response = requests.get(url)
            response.raise_for_status()
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')

            return self.call_gemini(soup)
        except requests.exceptions.RequestException as e:
            return [{"message":f"Error fetching the URL: {e}"}]
    def call_gemini(self, html_content:str) -> dict:
        model = genai.GenerativeModel(
            "gemini-1.5-flash",
            generation_config = {"response_mime_type": "application/json"}
        )
        prompt = """
下記のHTMLの中からレシピタイトル、動画URL、調理時間、費用目安、材料、手順を抽出してください。
{html_content}
Result = {{
    'recipe_title':string,
    'video_url':string,
    'cooking_time':string,
    'cost':string,
    'ingredients':list,
    'steps':list
}}
Return: list[Result]
""".format(html_content=html_content)
        response = model.generate_content(prompt)
        return json.loads(response.text)

