import json
from utils.ScrapeWLLM import ScrapeWLLM

urls = [
    'https://www.kurashiru.com/recipes/91b9518f-270e-4711-9b60-b49ad5bde163',
    'https://www.kurashiru.com/recipes/34a5fc6a-8411-47a3-82ad-555332eb9671',
    'https://www.kurashiru.com/recipes/287235e4-db7e-4e4c-b0a3-0008581de012'
]

if __name__ == '__main__':
    scraper = ScrapeWLLM(urls)
    result = scraper.scrape()
    with open('result/output.json', 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
