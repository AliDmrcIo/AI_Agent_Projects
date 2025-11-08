# Agent: LLM + Tool 
# demiştik. Burada agentımızın eline tool vereceğiz işte. Gerçek agent yapımına başlıyoruz.
# Zero-Shut Agent kullanarak doğru agentin doğru tool seçimi yapabilmesini sağlayacağız
# Soru: "Bugün İstanbul'da hava nasıl?"  Seçim: "Hava Durumu Aracını Kullan."
# Soru: "15 ile 23'ün çarpımı kaç eder?" Seçim: "Hesap Makinesi Aracını Kullan."

# importlar
from langchain_google_genai import ChatGoogleGenerativeAI # Gemini'yi kullanabilmek için. Google/Gemini chat modeli
from langchain.agents import create_agent  # Agent oluşturmak için
from langchain_community.tools import DuckDuckGoSearchRun # langchain toolları
from langchain.tools import tool

import os # proje içerisindeki tüm dosyalara ulaşabilmek için

from dotenv import load_dotenv # .env dosyasını yüklemek için

import warnings # uyarıları görmemek için
warnings.filterwarnings("ignore")

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

# tanımladığımız tüm toolları toplamalıyız böyle    
tools = [toplama_toolu, carpma_toolu, bolme_toolu]

# agentımızı başlatıyoruz
agent_executor = create_agent(model=llm, tools=tools)
# toollarımızın ne olacağı, LLM'in ne olacağı ve ajan tipini söyleyerek başlatmalıyız agent'ı

soru = "8 sayısını 3 ile çarpıp sonucu 2 sayısına böldükten sonra 19 ile toplarsam kaç bulurum?"

"""
Sonucu doğru bir şekilde:
"Cevap: 8 sayısını 3 ile çarptığımda 24, 24'ü 2'ye böldüğümde 12 ve 12'yi 19 ile topladığımda 31 bulurum." 
diyerek buluyor. Burada toplama, çarpma ve bölme işlemlerini dosdoğru şekilde yapmayı başardık 

LLM'ler bu tür hesaplamaları eğitildikleri zaten yapıyor ancak train dataset'lerine dayanarak yapıyorlar, 
bu da zaman zaman yanlış hesaplamalara sebep olabiliyor.

Biz burada LLM'e bir hesap makinesi tool'u vererek(yani onu agent yaparak -> LLM+Tool) bu işlemleri yapmasını sağladık.
Böylece LLM, hesaplamaları "tahmin ederek" yapmak yerine, 
Python fonksiyonlarını çağırarak kesin ve hatasız sonuçlar üretiyor.

Bu yaklaşım sayesinde:
✅ Matematiksel işlemler %100 doğru yapılır
✅ LLM'in matematiksel zayıflıkları ortadan kalkar
✅ Agent, doğru tool'u seçerek Python kodunu çalıştırır
"""

# agenti ve llmi başlat ve ona sorumuzu ver
yanit = agent_executor.invoke({"messages": [("user", soru)]})

print("Cevap: ", yanit['messages'][-1].content)