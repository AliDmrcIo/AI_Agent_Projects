# İlk Basit AI Agent Projemiz: Gemini 2.5 Flash'ı kullanarak bir tane basit soru cevap botu yapacağız

# Importlar
from langchain_google_genai import ChatGoogleGenerativeAI # Google/Gemini chat modeli
from langchain_core.messages import HumanMessage          # İnsan mesajını temsil eden sınıf

import os # dosyaları(bu projede .env) projede bulabilmek için

from dotenv import load_dotenv # .env dosyasını yüklemek için

import warnings # uyarıları görmemek için
warnings.filterwarnings("ignore")

# .env'i içeri alalım
load_dotenv() # env dosyasını yükler
gemini_api_key = os.getenv("GEMINI_API_KEY")

# chatbot modelimizi hazırlayalım
llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash", temperature=0.7, google_api_key=gemini_api_key)
# temperature: cevabın çeşitliliği (0: kararlı, 1: rastgele)

# kullanıcıdan gelen mesajı al
user_message = [HumanMessage(content="merhaba, nasılsın?")] # kullanıcının mesajını tanımla

# modeli çalıştır
response = llm.invoke(user_message) # modeli çalıştırır ve kullanıcının mesajını gönderir

# model cevabını yazdır
print(response.content) # modelin user_message'a olan cevabı
