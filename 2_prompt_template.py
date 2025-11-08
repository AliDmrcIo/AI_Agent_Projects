# İkinci proje: Birinci projedeki(1_langchain_openai_giris.py) manuel mesaj yazma işini prompt yazmayla dinamik hale getireceğiz

# Importlar
from langchain_google_genai import ChatGoogleGenerativeAI # Google/Gemini chat modeli
from langchain_core.messages import HumanMessage          # İnsan mesajını temsil eden sınıf
from langchain_core.prompts import PromptTemplate         # modele prompt verebilmek için

import os # dosyaları(bu projede .env) projede bulabilmek için

from dotenv import load_dotenv # .env dosyasını yüklemek için

import warnings # uyarıları görmemek için
warnings.filterwarnings("ignore")

# .env'i içeri alalım
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY") # artık erişilebilir olan .env dosyasındaki GEMINI_API_KEY'i al

# modeli tanımla - modelimizi hazırlayalım
llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash", temperature=0.7, google_api_key=gemini_api_key)
# temperature: cevabın çeşitliliği (0: kararlı, 1: rastgele)

# Prompt'u hazırla
prompt = PromptTemplate(input_variables=["user_message"], # Kullanıcının gireceği mesaj
                        template="Kısa ve anlaşılır şekilde {user_message} açıkla.\nYapay Zeka: ") # prompt şablonu
konu = "Yapay zeka nedir?" # kullanıcı mesajı
prompt_message = prompt.format(user_message=konu) # kullanıcı mesajını kütüphaneye uygun formata getirip prompt olduğunu belirttik

# modeli çalıştır ve kullanıcı mesajını modele gönder
response = llm.invoke([HumanMessage(content=prompt_message)])

# LLM'in cevabını görüntüle
print(response.content)