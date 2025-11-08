"""
Langchain'de bulunan Agentların karşılaştırmasını yapacağız - Agent Comparison yapacağız

Langchain Agent type karşılaştırma

2 tool kullanacağız:
- zero-shot-react-description
- structured-chat
"""

from langchain_google_genai import ChatGoogleGenerativeAI # Google Gemini chat modeli
from langchain.agents import create_agent # agent'ı başlatmak ve tipini öğrenmek için için gerekli modüller
from langchain.tools import tool
from langchain_core.messages import HumanMessage # mesaj yapısı

from dotenv import load_dotenv

import os

import warnings
warnings.filterwarnings("ignore")

# .env dosyasını yükle
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# agent'ın kullnacağı tool'u tanımlama
@tool
def toplam_araci(input:str)->str:
    """Verilen iki sayıyı toplayan tool. Örneğin 5 ve 8 = 5+8 = 13"""
    try:
        a,b = [int(x.strip()) for x in input.split("ve")]
        return f"Toplam {a} ve {b} = {a+b}"
    except Exception as e:
        return f"Hata: {str(e)}. Lütfen iki sayıyı 5 ve 8 formatında giriniz"

@tool
def carpma_araci(input:str)->str:
    """İki sayıyı çarpan tool. Örneğin 5 çarpı 8 = 40"""
    try:
        input_clean = input.replace("çarpı", "*").replace("x", "*")
        a,b = [int(x.strip()) for x in input_clean.split("*")]
        return f"Çarpım {a} * {b} = {a*b}"
    except Exception as e:
        return f"Hata: {str(e)}"
    
tools = [toplam_araci, carpma_araci]

# test soruları
sorular = [
    "5 ve 8 sayılarını topla",
    "12 çarpı 3 kaç eder?",
    "4 ve 7'yi topla"
]

print("="*80)
print("LANGCHAIN AGENT KARŞILAŞTIRMASI")
print("="*80)

# ========================================
# YAKLAŞIM 1: "ReAct Tarzı" (zero-shot-react-description benzeri)
# ========================================
print("\n" + "="*80)
print("1. ReAct Tarzı Agent (Detaylı Düşünme - zero-shot-react benzeri)")
print("="*80)

# model yaratma ve seçme
llm_react = ChatGoogleGenerativeAI(model = "gemini-2.5-flash", temperature=0.7, google_api_key=gemini_api_key)
# daha yaratıcı düşünme için temperature=0.7 yaptık. birazdan zaten bunu kıyaslıyacağız

# ReAct Agent (zero-shot-react-description benzeri)
agent_react = create_agent(llm_react, tools) # agenti oluşturuyoruz

sonuclar_react = []

for i, soru in enumerate(sorular, 1):
    print(f"\n{'─'*80}")
    print(f"SORU {i}: {soru}")
    print('─'*80)
    
    result_react = agent_react.invoke({
        "messages": [
            HumanMessage(content=soru)
        ]
    })
    
    print(f"\n📝 SORU: {soru}")
    print(f"\n🤔 Agent Süreci:")
    for j, msg in enumerate(result_react['messages'], 1):
        msg_type = type(msg).__name__
        print(f"   {j}. {msg_type}: {msg.content[:80]}...")
    
    print(f"\n✅ SON CEVAP: {result_react['messages'][-1].content}")
    
    sonuclar_react.append({
        'soru': soru,
        'adim': len(result_react['messages']),
        'cevap': result_react['messages'][-1].content
    })

# ========================================
# YAKLAŞIM 2: "Structured Tarzı" (structured-chat benzeri)
# ========================================
print("\n\n" + "="*80)
print("2. Structured Tarzı Agent (Hızlı ve Öz - structured-chat benzeri)")
print("="*80)

llm_structured = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0.0, google_api_key=gemini_api_key)
# temperature=0.0 olan karşılaştırılacak diğer agentımız oldu bu da

agent_structured = create_agent(llm_structured, tools) # agenti oluşturuyoruz. 

sonuclar_structured = []

for i, soru in enumerate(sorular, 1):
    print(f"\n{'─'*80}")
    print(f"SORU {i}: {soru}")
    print('─'*80)
    
    result_structured = agent_structured.invoke({
        "messages": [
            HumanMessage(content=soru)
        ]
    })
    
    print(f"\n📝 SORU: {soru}")
    print(f"\n⚡ Agent Süreci:")
    for j, msg in enumerate(result_structured['messages'], 1):
        msg_type = type(msg).__name__
        print(f"   {j}. {msg_type}: {msg.content[:80]}...")
    
    print(f"\n✅ SON CEVAP: {result_structured['messages'][-1].content}")
    
    sonuclar_structured.append({
        'soru': soru,
        'adim': len(result_structured['messages']),
        'cevap': result_structured['messages'][-1].content
    })

# ========================================
# KARŞILAŞTIRMA
# ========================================
print("\n\n" + "="*80)
print("DETAYLI KARŞILAŞTIRMA TABLOSU")
print("="*80)

for i in range(len(sorular)):
    print(f"\n📌 SORU {i+1}: {sorular[i]}")
    print(f"┌─────────────────────┬──────────────────────┬──────────────────────┐")
    print(f"│ ÖZELLİK             │ ReAct Tarzı          │ Structured Tarzı     │")
    print(f"├─────────────────────┼──────────────────────┼──────────────────────┤")
    print(f"│ Adım Sayısı         │ {sonuclar_react[i]['adim']:^20} │ {sonuclar_structured[i]['adim']:^20} │")
    print(f"│ Cevap Uzunluğu      │ {len(sonuclar_react[i]['cevap']):^20} │ {len(sonuclar_structured[i]['cevap']):^20} │")
    print(f"└─────────────────────┴──────────────────────┴──────────────────────┘")

print("\n\n" + "="*80)
print("GENEL KARŞILAŞTIRMA TABLOSU")
print("="*80)

avg_steps_react = sum(s['adim'] for s in sonuclar_react) / len(sonuclar_react)
avg_steps_structured = sum(s['adim'] for s in sonuclar_structured) / len(sonuclar_structured)

print(f"""
┌────────────────────────────┬─────────────────────┬──────────────────────┐
│ ÖZELLİK                    │ ReAct Tarzı         │ Structured Tarzı     │
├────────────────────────────┼─────────────────────┼──────────────────────┤
│ Eski Agent Tipi Karşılığı  │ ZERO_SHOT_REACT     │ STRUCTURED_CHAT      │
│ Model                      │ gemini-2.5-flash    │ gemini-2.0-flash     │
│ Temperature                │ 0.7 (Yaratıcı)      │ 0.0 (Deterministik)  │
│ Ortalama Adım Sayısı       │ {avg_steps_react:^19.1f} │ {avg_steps_structured:^20.1f} │
│ Detay Seviyesi             │ Yüksek              │ Düşük                │
│ Hız                        │ Yavaş               │ Hızlı                │
│ Kullanım Amacı             │ Eğitim/Debug        │ Production           │
└────────────────────────────┴─────────────────────┴──────────────────────┘
""")

print("\n💡 SONUÇ:")
print("   Yeni versiyonda AgentType parametresi YOK.")
print("   Bunun yerine: Temperature ve Model değiştirerek")
print("   farklı davranışlar elde ediyoruz.")


"""
Eski versiyonları kullanamadığımız, AgentType kullanamadığımız için tam olarak zero-shot ve structured karşlaştırması yapamadık. 
ona benzer olan farklı yöntemle yaptık. normalde:

Zero-Shot-React-Description: LLM'den gelen yanıt, natural language reasoning içerir. Yani ne düşündüğü anlaşılır, hangi toolu kullanacağını söyler.
Artıları: açıklamalı, adım adım reasoning gösterir, debug'ı kolay. Herhangi bir LLM ile çalışabilir. function calling şart değil
Eksileri: Parsing hatası riski var. tool gerekmeyen mesajlarda da boş bırakabilir. 

Structured-Chat: LLM toolları birer fonksiyon olarak görür ve doğrudan json formatını çağırır. langchain ekstra bir parsing yapmıyor çünkü llm zaten yapr
Artıları: parsing hata riski yok, gerçek apiler çalışırken uyumlu olur
Eksileri: sadece function calling destekleyen modellerde çalışır. gpt 3.5 turbo, gpt 4 gibi.

Sonuç: OpenAI hariç genelde zero shot description kullanmakta fayda var.

Tüm agent tipleri:
1) Chat-zero-shot: chat modelleriyle daha doğal konuşmalar yapılır
2) structured-chat-zero-shut: daha kontrollü tool charları yapmamızı sağlar
3) plan-and-execute: önce plan sonra tool execution yapar. çok adımlı görev zincirleri için gerçekleştirilir
4) Zero-Shot-React-Description: şimdi kullandık

"""