import json
import os
from typing import *

from dotenv import load_dotenv
from openai import OpenAI

from web_retriever import *

# ======================================================================================================================
# Important Link Analyzer
# ======================================================================================================================
class ImportantLinkAnalyzerAgent:
    __url: str
    __links: Set[str]

    def __init__(self, *, url: str, links: Set[str]):
        self.__url = url
        self.__links = links

    def __generate_user_prompt(self) -> str:
        user_prompt = f"Here is the list of links on the website of {self.__url} - "
        user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. Do not include Terms of Service, Privacy, email links.\n"
        user_prompt += "Links (some might be relative links):\n"
        user_prompt += "\n".join(self.__links)

        return user_prompt

    @staticmethod
    def __generate_system_prompt() -> str:
        system_prompt = "You are provided with a list of links found on a webpage. You are able to decide which of the links would be most relevant to include in a brochure about the company, such as links to an About page, or a Company page, or Careers/Jobs pages.\n"
        system_prompt += "You should respond in JSON as in this example:"
        system_prompt += """
            {
                "links": [
                    {"type": "about page", "url": "https://full.url/goes/here/about"},
                    {"type": "careers page": "url": "https://another.full.url/careers"}
                ]
            }"""

        return system_prompt

    def generate_message(self):
        _user_prompt = self.__generate_user_prompt()
        return [
            {"role": "system", "content": ImportantLinkAnalyzerAgent.__generate_system_prompt()},
            {"role": "user", "content": self.__generate_user_prompt()},
        ]

    def ask(self):
        load_dotenv()
        os.getenv('OPENAI_API_KEY')
        openai = OpenAI()
        response = openai.chat.completions.create(
            model = "gpt-4o-mini",
            messages = self.generate_message(),
            response_format={ "type": "json_object" }
        )

        return response.choices[0].message.content


# ======================================================================================================================
# Brochure Generator Agent
# ======================================================================================================================
class BrochureGeneratorAgent:
    pass


# ======================================================================================================================
# Run
# ======================================================================================================================
url_on_test = "https://www.prosigmaka.com"
# url_on_test = "https://www.detik.com"
webRetriever = WebRetriever(url=url_on_test)
webRetriever.retrieve()
links = webRetriever.generate_links()

print(links)
