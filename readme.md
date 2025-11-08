## TR:
# LangChain ile Adım Adım AI Agent Geliştirme

Bu repository, LangChain kütüphanesini kullanarak yapay zeka (AI) agent'ları oluşturma sürecini temel seviyeden ileri seviyeye taşıyan bir dizi Python projesi içermektedir. Projeler, en basit LLM çağrısından başlayarak, araç kullanımı, hafıza yönetimi, yapılandırılmış çıktı, RAG (Retrieval-Augmented Generation) ve yerel (on-premise) model kullanımı gibi modern AI konseptlerini adım adım öğretmeyi amaçlamaktadır.

## Kapsanan Ana Konular

- **Temel LLM Entegrasyonu**: LangChain ile Google Gemini modelini kullanma.
- **Prompt Şablonları (Prompt Templating)**: Dinamik ve yeniden kullanılabilir prompt'lar oluşturma.
- **Agent ve Araç (Tool) Kullanımı**: LLM'lere hesap makinesi gibi harici yetenekler kazandırma.
- **Hafıza (Memory)**: Agent'lara konuşma geçmişini hatırlama yeteneği ekleme.
- **Çıktı Ayrıştırıcıları (Output Parsers)**: LLM'den gelen yanıtları yapılandırılmış (JSON gibi) formatlara dönüştürme.
- **API Entegrasyonu**: Agent'ların dış dünya API'lerine (döviz kuru gibi) bağlanması.
- **RAG (Retrieval-Augmented Generation)**:
    - Metin (`.txt`) dosyasından bilgi alarak yanıt üretme.
    - Veritabanından (`SQLite`) bilgi alarak yanıt üretme.
- **Yerel LLM Kullanımı**: Gemini gibi bulut tabanlı modeller yerine, bilgisayarınızda çalışan LLaMA (Ollama aracılığıyla) gibi yerel modelleri kullanma.
- **Gerçek Hayat Projesi**: Müşteri şikayetlerini sınıflandıran, ilgili departmana yönlendiren, RAG ile bilgi bankasından destek alarak yanıt üreten ve sonuçları Excel'e raporlayan bir sistem geliştirme.

## Kurulum ve Başlangıç

Projeleri çalıştırmak için aşağıdaki adımları izleyin:

1.  **Repository'yi Klonlayın:**
    ```bash
    git clone https://github.com/AliDmrcIo/AI_Agent_Projects.git
    cd AI_Agent_Projects
    ```

2.  **Sanal Ortamı Aktif Edin:**
    Bu proje bir `venv` sanal ortamı içermektedir. Öncelikle bu ortamı aktif edin.
    ```bash
    # Windows için
    .\venv\Scripts\activate
    ```

3.  **Bağımlılıkları Yükleyin (veya `requirements.txt` Oluşturun):**
    Projenizi paylaşmadan önce, başkalarının da kolayca kurulum yapabilmesi için `requirements.txt` dosyası oluşturmanız önerilir. Sanal ortamınız aktifken aşağıdaki komutu çalıştırarak bu dosyayı oluşturabilirsiniz:
    ```bash
    pip freeze > requirements.txt
    ```
    Daha sonra projeyi klonlayan herkes aşağıdaki komutla tüm kütüphaneleri kurabilir:
    ```bash
    pip install -r requirements.txt
    ```

4.  **.env Dosyanızı Oluşturun:**
    Proje ana dizininde `.env` adında bir dosya oluşturun. İçine Gemini API anahtarınızı aşağıdaki formatta ekleyin:
    ```
    GEMINI_API_KEY="AIzaSy...SİZİN_API_ANAHTARINIZ"
    ```

5.  **Veritabanını Oluşturun:**
    12. ve 13. projeler için SQLite veritabanını oluşturmak üzere aşağıdaki betiği çalıştırın:
    ```bash
    python 12_db.py
    ```

6.  **Yerel LLM için Ollama Kurulumu:**
    `13_sikayet_siniflandirma_ve_rag_db_LLaMA.py` projesini çalıştırmak için sisteminizde [Ollama](https://ollama.com/)'nın kurulu olması ve `llama3.2:3b` modelinin indirilmiş olması gerekmektedir.
    ```bash
    ollama pull llama3.2:3b
    ```

## Proje Dosyaları ve Açıklamaları

---

### Bölüm 1: LangChain Temelleri

-   **`1_langchain_openai_giris.py`**: LangChain ve Gemini ile en temel "Merhaba Dünya" uygulaması. Bir LLM'e nasıl soru sorulacağını ve cevap alınacağını gösterir.
-   **`2_prompt_template.py`**: `PromptTemplate` kullanarak kullanıcı girdisini dinamik olarak bir şablona yerleştirmeyi öğretir.
-   **`5_output_parser.py`**: LLM'den gelen metin tabanlı cevabı, `Pydantic` kullanarak yapılandırılmış bir JSON nesnesine (ürün adı, fiyat, kategori vb.) nasıl dönüştüreceğimizi gösterir.

### Bölüm 2: Agent'lar ve Araçlar

-   **`3_agent_tool_kullanimi.py`**: Agent kavramına giriş. LLM'e matematiksel işlemler yapabilmesi için `toplama`, `çarpma` ve `bölme` araçları (tool) verilir. Agent, gelen soruya göre doğru aracı seçip kullanır.
-   **`4_agent_memory.py`**: Önceki projeye **hafıza** eklenir. Agent artık "bir önceki işlemin sonucunu 5 ile çarp" gibi komutları anlayabilir, çünkü konuşma geçmişini hatırlar.
-   **`6_langchain_agent_comparison.py`**: Farklı Agent davranışlarını (ReAct vs. Structured) model ve `temperature` ayarlarıyla nasıl taklit edebileceğimizi karşılaştırır.
-   **`7_agent_with_api.py`**: Agent'a dış dünya ile iletişim kurma yeteneği kazandırılır. Gerçek zamanlı döviz kurunu bir API'den çekerek yanıt veren bir tool oluşturulur.
-   **`8_multi_step_agents.py`**: **(Eski Sürüm Uyumsuzluğu)** Çok adımlı görevler için "Planla ve Uygula" (Plan and Execute) agent yapısını tanıtır. Not: Bu betik güncel LangChain sürümleriyle uyumsuzluk nedeniyle çalışmayabilir, ancak konsepti göstermek için eklenmiştir.

### Bölüm 3: Müşteri Şikayet Yönetimi Projesi (Adım Adım Geliştirme)

Bu bölüm, tek bir proje fikrinin nasıl adım adım daha yetenekli hale getirildiğini gösterir.

-   **`9_sikayet_siniflandirma_projesi.py`**: Projenin ilk adımı. Kullanıcıdan gelen bir şikayeti alır, LLM kullanarak `kategori`, `yönlendirilecek birim` ve `müşteriye verilecek cevap` olarak sınıflandırır.
-   **`10_sikayet_siniflandirma_2.py`**: 9. projeye **Excel'e raporlama** özelliği eklenir. Her şikayet, zaman damgasıyla birlikte bir `sikayet_raporu.xlsx` dosyasına kaydedilir.
-   **`11_sikayet_siniflandirma_ve_rag.py`**: Projeye **RAG (Retrieval-Augmented Generation)** eklenir. Agent artık müşteriye cevap verirken `11_icin_rag_veriler.txt` dosyasındaki bilgi bankasından faydalanır. Böylece daha doğru ve bağlama uygun cevaplar üretir.
-   **`12_sikayet_siniflandirma_ve_rag_db.py`**: RAG'ın veri kaynağı `.txt` dosyasından **SQLite veritabanına** taşınır. Bu, daha ölçeklenebilir ve yönetilebilir bir bilgi bankası sağlar. `12_db.py` betiği bu veritabanını oluşturur.
-   **`13_sikayet_siniflandirma_ve_rag_db_LLaMA.py`**: Projenin son hali. Tüm sistem, bulut tabanlı Gemini yerine, **yerel (on-premise) LLaMA modeli** ile çalışacak şekilde güncellenir. Bu sayede veri gizliliği sağlanır ve API maliyetleri ortadan kalkar.


## ENG:
# Step-by-Step AI Agent Development with LangChain

This repository contains a series of Python projects that guide you from the basics to advanced levels of creating AI agents using the LangChain library. The projects start with a simple LLM call and progressively introduce modern AI concepts such as tool usage, memory management, structured outputs, Retrieval-Augmented Generation (RAG), and using local (on-premise) models.

## Core Concepts Covered

- **Basic LLM Integration**: Using the Google Gemini model with LangChain.
- **Prompt Templating**: Creating dynamic and reusable prompts.
- **Agents and Tool Usage**: Giving LLMs external capabilities, like a calculator.
- **Memory**: Adding the ability for agents to remember conversation history.
- **Output Parsers**: Converting responses from LLMs into structured formats like JSON.
- **API Integration**: Connecting agents to external world APIs (e.g., for currency exchange rates).
- **Retrieval-Augmented Generation (RAG)**:
    - Generating responses by retrieving information from a text (`.txt`) file.
    - Generating responses by retrieving information from a database (`SQLite`).
- **Local LLM Usage**: Using local models like LLaMA (via Ollama) on your own machine instead of cloud-based models like Gemini.
- **Real-World Project**: Developing a system that classifies customer complaints, routes them to the appropriate department, generates responses using a RAG-powered knowledge base, and reports the results to an Excel file.

## Setup and Getting Started

Follow these steps to run the projects:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/AliDmrcIo/AI_Agent_Projects.git
    cd AI_Agent_Projects
    ```

2.  **Activate the Virtual Environment:**
    This project includes a `venv` virtual environment. First, activate this environment.
    ```bash
    # For Windows
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies (or Create `requirements.txt`):**
    Before sharing your project, it is recommended to create a `requirements.txt` file so others can easily install the dependencies. You can create this file by running the following command while your virtual environment is active:
    ```bash
    pip freeze > requirements.txt
    ```
    After that, anyone who clones the project can install all the libraries with the following command:
    ```bash
    pip install -r requirements.txt
    ```
    
4.  **Create Your `.env` File:**
    Create a file named `.env` in the project's root directory. Add your Gemini API key in the following format:
    ```
    GEMINI_API_KEY="AIzaSy...YOUR_API_KEY"
    ```

5.  **Create the Database:**
    To create the SQLite database for projects 12 and 13, run the following script:
    ```bash
    python 12_db.py
    ```

6.  **Install Ollama for Local LLM:**
    To run the `13_sikayet_siniflandirma_ve_rag_db_LLaMA.py` project, you need to have [Ollama](https://ollama.com/) installed on your system and the `llama3.2:3b` model downloaded.
    ```bash
    ollama pull llama3.2:3b
    ```

## Project Files and Descriptions

---

### Part 1: LangChain Fundamentals

-   **`1_langchain_openai_giris.py`**: The most basic "Hello World" application with LangChain and Gemini. It shows how to ask a question to an LLM and get a response.
-   **`2_prompt_template.py`**: Teaches how to dynamically insert user input into a template using `PromptTemplate`.
-   **`5_output_parser.py`**: Shows how to convert a text-based response from an LLM into a structured JSON object (e.g., product name, price, category) using `Pydantic`.

### Part 2: Agents and Tools

-   **`3_agent_tool_kullanimi.py`**: An introduction to the concept of agents. The LLM is given `addition`, `multiplication`, and `division` tools to perform mathematical operations. The agent selects and uses the correct tool based on the user's question.
-   **`4_agent_memory.py`**: Adds **memory** to the previous project. The agent can now understand commands like "multiply the result of the previous operation by 5" because it remembers the conversation history.
-   **`6_langchain_agent_comparison.py`**: Compares how different Agent behaviors (ReAct vs. Structured) can be simulated by changing the model and `temperature` settings.
-   **`7_agent_with_api.py`**: Gives the agent the ability to communicate with the outside world. A tool is created that fetches real-time currency exchange rates from an API to provide an answer.
-   **`8_multi_step_agents.py`**: **(Legacy Version Incompatibility)** Introduces the "Plan and Execute" agent structure for multi-step tasks. Note: This script may not work due to incompatibilities with recent LangChain versions but is included to demonstrate the concept.

### Part 3: Customer Complaint Management Project (Step-by-Step Development)

This section demonstrates how a single project idea is progressively enhanced with more capabilities.

-   **`9_sikayet_siniflandirma_projesi.py`**: The first step of the project. It takes a user complaint and uses an LLM to classify it into a `category`, the `unit to be routed to`, and a `response to the customer`.
-   **`10_sikayet_siniflandirma_2.py`**: Adds **Excel reporting** functionality to project 9. Each complaint is saved to an `sikayet_raporu.xlsx` file with a timestamp.
-   **`11_sikayet_siniflandirma_ve_rag.py`**: Adds **RAG (Retrieval-Augmented Generation)** to the project. The agent now utilizes a knowledge base from the `11_icin_rag_veriler.txt` file when responding to the customer, resulting in more accurate and context-aware answers.
-   **`12_sikayet_siniflandirma_ve_rag_db.py`**: The RAG's data source is moved from a `.txt` file to an **SQLite database**. This provides a more scalable and manageable knowledge base. The `12_db.py` script creates this database.
-   **`13_sikayet_siniflandirma_ve_rag_db_LLaMA.py`**: The final version of the project. The entire system is updated to run with a **local (on-premise) LLaMA model** instead of the cloud-based Gemini, ensuring data privacy and eliminating API costs.
