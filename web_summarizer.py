import os
from dotenv import load_dotenv
from openai import OpenAI
import ollama
from web_retriever import *

# ======================================================================================================================
# LLMSummarizer
# ======================================================================================================================
class LLMSummarizer:
    __title = None
    __body = None

    def __init__(self):
        pass

    def set_title(self, title):
        self.__title = title

    def set_body(self, body):
        self.__body = body

    @staticmethod
    def __generate_system_prompt():
        system_prompt = "You are an assistant that analyzes the contents of a website and provides a short summary, ignoring text that might be navigation related. Respond in markdown. Please use indonesian language to summarize"

        return system_prompt

    def __generate_user_prompt(self):
        user_prompt = f"You are looking at a website titled {self.__title}"
        user_prompt += "\nThe contents of this website is as follows; please provide a short summary of this website in markdown. If it includes news or announcements, then summarize these too.\n"
        user_prompt += "\nPlease use indonesian language to summarize"
        user_prompt += self.__body

        return user_prompt

    def generate_message(self):
        return [
            {"role": "system", "content": LLMSummarizer.__generate_system_prompt()},
            {"role": "user", "content": self.__generate_user_prompt()},
        ]

    def summarize(self):
        pass


class ChatGPTSummarizer(LLMSummarizer):
    __response = None
    __openai = None

    def __init__(self):
        super().__init__()
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        self.__openai = OpenAI()

    def summarize(self):
        self.__response = self.__openai.chat.completions.create(
            model = "gpt-4o-mini",
            messages = self.generate_message()
        )

        return self.__response.choices[0].message.content


class OllamaSummarizer(LLMSummarizer):
    __MODEL = "llama3.2"
    __response = None

    def __init__(self):
        super().__init__()

    def summarize(self):
        self.__response = ollama.chat(model=self.__MODEL, messages=self.generate_message())

        return self.__response['message']['content']


# ======================================================================================================================
# WebSummarizer
# ======================================================================================================================
class WebSummarizer:
    __url = None
    __web_retriever = None
    __llm_summarizer = None

    def __init__(self, *, url, llm_summarizer):
        self.__url = url
        self.__web_retriever = WebRetriever(url=url)
        self.__llm_summarizer = llm_summarizer

    def summarize(self):
        title, body = self.__web_retriever.retrieve()
        self.__llm_summarizer.set_title(title)
        self.__llm_summarizer.set_body(body)

        return self.__llm_summarizer.summarize()
