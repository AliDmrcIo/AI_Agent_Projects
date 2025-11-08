# Agent: LLM + Tool + Hafıza Yapacağız. Yani önceki 3_agent dosyasına ek olarak hafıza ekleyeceğiz

"""
agenta a short-term memory ekleyelim
onceki sorulari ve cevaplari hatirlayabilsin

ornek senaryo
konusma 1: 5 ile 2 yi topla,
konusma 2: sonucu 2 ile carp - sonucu diyince sonucun önceki işlemden 7 olduğunu hatırlayacak işte
"""

# importlar
from langchain_google_genai import ChatGoogleGenerativeAI # Gemini'yi kullanabilmek için. Google/Gemini chat modeli
from langchain.agents import create_agent  # Agent oluşturmak için
from langchain_community.tools import DuckDuckGoSearchRun # langchain toolları
from langchain.tools import tool
from langgraph.checkpoint.memory import MemorySaver # Önceki koda eklenen tek şey: Konuşmaları short term memory'e kaydetmek için

import os # proje içerisindeki tüm dosyalara ulaşabilmek için

from dotenv import load_dotenv # .env dosyasını yüklemek için

import warnings # uyarıları görmemek için
warnings.filterwarnings("ignore")

import json

# .env dosyasını yükle
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY") # artık erişilebilir olan .env dosyasındaki GEMINI_API_KEY'i al

# Modeli Tanımla
llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash", temperature=0.7, google_api_key=gemini_api_key)

# Tool Kullanımı
@tool                                # tool tanımlarken böyle yapmamız gerekiyor
def toplama_toolu(input:str) -> str: # ilk toolumuz toplama işlemi yapma aracıdır. Verilen iki sayıyı toplayan tool

    """İki sayıyı toplamak için kullanılır. Girdi 'sayı1 ve sayı2' formatında olmalıdır.""" # agent buna bakacak ve ne yapacağını anlayacak

    try:
        a,b = [int(x.strip()) for x in input.split("ve")]
        return f"Toplam: {a} ve {b} = {a+b}"
    except Exception as e:
        return f"Hata: {str(e)}. Lütfen doğru formatta giriniz"
    
@tool                                
def carpma_toolu(input:str) -> str:
    """İki sayıyı çarpmak için kullanılır. Girdi 'sayı1 ve sayı2' formatında olmalıdır."""
    try:
        a,b = [int(x.strip()) for x in input.split("ve")]
        return f"Çarpım: {a} x {b} = {a*b}"
    except Exception as e:
        return f"Hata: {str(e)}. Lütfen doğru formatta giriniz"

@tool                                
def bolme_toolu(input:str) -> str:
    """İki sayıyı bölmek için kullanılır. Girdi 'sayı1 ve sayı2' formatında olmalıdır."""
    try:
        a,b = [float(x.strip()) for x in input.split("ve")]
        if b == 0:
            return "Hata: Sıfıra bölme hatası!"
        return f"Bölüm: {a} / {b} = {a/b}"
    except Exception as e:
        return f"Hata: {str(e)}. Lütfen doğru formatta giriniz"

# bunu eklemezsek eğer, model matematiksel sorular dışında hiçbirşeye cevap vermiyor, "python nedir?"" dediğimde
# Üzgünüm, bu soruya cevap veremem çünkü benim yeteneklerim matematiksel işlemleri gerçekleştirmekle sınırlıdır.
# diyor, bu sebeple ona konuşma yeteneği de veren bunu eklicez:
search_tool = DuckDuckGoSearchRun()

# tanımladığımız tüm toolları toplamalıyız böyle    
tools = [toplama_toolu, carpma_toolu, bolme_toolu, search_tool]

# short-term memory'i başlat
memory = MemorySaver()

# agentımızı başlatıyoruz
agent_executor = create_agent(model=llm, tools=tools, checkpointer=memory) # önceki koda ek olarak memory'de var
# toollarımızın ne olacağı, LLM'in ne olacağı ve ajan tipini söyleyerek başlatmalıyız agent'ı

config = {"configurable": {"thread_id": "konusma-1"}}

# Konsoldan sonsuz konuşma yapabilmek için bu yapıyı yazdık
print("Yapay Zeka ile Matematiksel işlemler yapabilirsiniz.")
while True:
    soru=input("Soru: ") # kullanıcıdan soruyu al
    if soru.lower() in ["exit", "quit", "çıkış"]:
        print("Çıkılıyor...")
        break
    else:
        try:
            yanit = agent_executor.invoke({"messages": [("user", soru)]}, config) # agent'ı çalıştır ve soruyu gönder
            print("Cevap: ", yanit['messages'][-1].content)
        except Exception as e:
            print(f"Hata: {str(e)}")