"""
Yapay zekadan gelen cevabı belirli bir formatta işleyeceğiz.

Json çıktısı olarak ya da liste, tablo, raporlama şeklinde olabilir bu çıktılar

Örnek senaryo: Kullanıcı bir bilgi istesin; bunu ad, kategori, fiyat ve stok durumu şeklinde ayırıp verelim
"""

from langchain_google_genai import ChatGoogleGenerativeAI   # Google Gemini chat modeli
from pydantic import BaseModel, Field                       # Structured output için

from dotenv import load_dotenv  # .env dosyasını yüklemek için

import os # proje içerisindeki tüm dosyalara ulaşabilmek için

import warnings # uyarıları görmemek için
warnings.filterwarnings("ignore") 

# .env dosyasını yükleyip içerisindeki apiyi alalım
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Modeli Tanımla
llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash", temperature=0.7, google_api_key=gemini_api_key)

# Yapılandırılmış Şemamızı - Formatımızı Tanımlayalım (Yeni yöntem: Pydantic BaseModel)
class UrunBilgisi(BaseModel):
    urun_adi: str = Field(description="urun adi")
    kategori: str = Field(description="urun kategorisi")
    fiyat: str = Field(description="urun fiyati")
    stok_durumu: str = Field(description="urun stok durumu")

# Gemini'nin native structured output özelliğini kullan (parser otomatik oluşuyor)
structured_llm = llm.with_structured_output(UrunBilgisi, method="json_schema")

soru = "Samsung galaxy s23 ultra telefonu hakkında bilgi verir misin?" # kullanıcıdan gelen soru

# prompt formatlamaya gerek yok, direkt invoke ediyoruz

# Modeli Çalıştır ve Kullanıcı mesajını ver
structured_data = structured_llm.invoke(soru)  # Direkt soru gönderdik, otomatik parse ediyor

print(structured_data)