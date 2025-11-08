"""
Dış api kullanan Agent yapıcaz
Agent'ımız dış dünya apilerine erişim sağlar

Örn: 
Soru:  Dolar kuru nedir?
İşlem: Parabirimleri sitesine gidip dolar kurunu söyler
"""

from langchain_google_genai import ChatGoogleGenerativeAI # Google Gemini chat modeli
from langchain.agents import create_agent # agent'ı başlatmak ve tipini öğrenmek için için gerekli modüller
from langchain.tools import tool
from langchain_core.messages import HumanMessage # mesaj yapısı

import requests # dış apilere istek atabileceğiz

from dotenv import load_dotenv

import os

import warnings
warnings.filterwarnings("ignore")

# .env dosyasını yükle
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# model yaratma ve seçme
llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash", temperature=0.3, google_api_key=gemini_api_key)

@tool
def doviz_kuru(input:str)->str:
    """ Döviz kuru sorgulayan tool. Örn: 'USD' veya 'EUR' """
    try:
        base_currency = input.strip().upper() # kullanıcının girdiği para birimini al
        url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
        response = requests.get(url)
        data = response.json()
        rate = data['rates']['TRY']
        return f"{base_currency} kuru: {rate} TL"
    except Exception as e:
        return f"Hata: {str(e)}, Lütfen geçerli para birimi giriniz"
    
tools = [doviz_kuru] # toolları tanımla

# agent'ı yarat
api_agent = create_agent(llm, tools)

soru = "bugün sterin ne oldu"

yanit = api_agent.invoke({ # agenta soruyu vererek çalıştır
        "messages": [
            HumanMessage(content=soru)
        ]
    })

print(f"\nCEVAP: {yanit['messages'][-1].content}") # agent'dan gelen cevabı göster