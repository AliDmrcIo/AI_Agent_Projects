"""
Ön Müşteri hizmetleri asistanı
Kullanıcı şikayetlerini analiz eden, kategorize eden, ilgili birimlere yönlendiren 
ve uygun yanıt veren bir sistem olacak
"""

from langchain_google_genai import ChatGoogleGenerativeAI # Gemini'yi içeri aktardık
from langchain_core.prompts import PromptTemplate # Prompt yazabilmek için
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from pydantic import BaseModel, Field # çıktıyı yapılandırmak ve ayrıştırmak için

from dotenv import load_dotenv # .env dosyamızı içeri aktarabilmek için

import os # .env dosyamızı proje içerisinde bulabilmek için

import warnings
warnings.filterwarnings("ignore") # uyarıları görmemek adına

# .env al
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# geminimizi belirleyelim ve alalım
llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash", temperature=0.2, google_api_key=gemini_api_key)

# Output şemasını tanımla (şikayet kategorisi, yönlendirme, cevap)
class Response_Schema(BaseModel):
    kategori: str = Field(description="şikayetin kategorisi. örn 'ürün kategorisi', 'Teslimat Sorunu', 'Müşteri hizmetleri'")
    yonlendirme: str = Field(description="şikayetin yönlendirileceği birim. örn 'ürün departmanı', 'lojistik departmanı', 'Müşteri hizmetleri departmanı'")
    cevap: str = Field(description="kullanıcıya verilecek cevap. örn 'şikayetiniz alınmıştır', 'en kısa sürede dönüş yapılacaktır'")

"""
Cevabın şu formatta verilmesinden:

Kategori: Teslimat Sorunu
Yönlendirme: Müşteri Hizmetleri Departmanı
Cevap: Kargonuzun gecikmesi ve müşteri hizmetlerimize ulaşamamanızla ilgili şikayetiniz alınmıştır.

bu Response_Schema yapısı sorumlu. Bunu, bu yapıyor.
"""

# LLM'in çıktısını JSON formatına çevirmek için parser yarat
parser = PydanticOutputParser(pydantic_object=Response_Schema)

# LLM'e "şu formatta cevap ver" talimatını hazırla
formatted_instructions = parser.get_format_instructions()

# Prompt Şablonu
template = PromptTemplate(
    input_variables=["sikayet"], # kullanıcının mesajı
    partial_variables={ 
        "format_instructions":formatted_instructions # format talimatı
    }, 
    template="""
        Bir kullanıcıdan şikayeti aldın. 
        Bu şikayeti anlamlandır, uygun kategoriyi belirle, yönlendirme yap ve kullanıcıya kısa bir açıklama yaz

        {format_instructions}

        Şikayet: {sikayet}
        """
)

# kullancının mesajı
sikayet = "iki gündür kargom gelmedi, müşteri hizmetlerine ulaşamıyorum"

prompt = template.format(sikayet=sikayet) # prompt mesajını oluştur

# llm'e prompt'u ver
response = llm.invoke(prompt)

result = parser.parse(response.content) # llm'in yanıtını ayrıştır

print("\n--- Şikayet Analizi ---")
print("Kategori:", result.kategori)
print("Yönlendirme:", result.yonlendirme)
print("Cevap:", result.cevap)

"""
Kullanıcının yazacağı şikayeti aldı, kategorisini belirledi, yönlendirdi ve müşteriye cevap verdi. Süper bir gerçek hayat projesi oldu
Bu gerçek bir müşteri hizmetleri projesi
"""