# 🇸🇪 Swedish Translation Project - AxieStudio Backend

## 📋 Översikt

Detta projekt översätter AxieStudio Backend till svenska. Vi fokuserar **ENDAST** på användarriktade strängar som visas i användargränssnittet.

## ✅ Slutförda översättningar

### 🔧 Backend Core Systems (100% klart)
- **Autentisering**: `services/auth/utils.py` - Alla felmeddelanden och statusmeddelanden
- **E-postmallar**: `services/email/service.py` - Alla e-postmallar (välkomst, återställning, verifiering)
- **API-felmeddelanden**: `api/v1/` - Alla HTTP-felmeddelanden och valideringsfel
- **Hälsokontroller**: `api/health_check_router.py` - Systemstatusmeddelanden
- **Schema**: `schema/message.py`, `schema/content_types.py` - Valideringsmeddelanden
- **Prenumerationer**: `api/v1/subscriptions.py` - Stripe-relaterade meddelanden
- **Konstanter**: `initial_setup/`, `services/utils.py` - Konfigurationsmeddelanden
- **Verifieringssystem**: `services/automated_verification_system.py` - Alla användarmeddelanden

### 🤖 AI/LLM-komponenter (Slutförda)
- **OpenAI**: `components/openai/openai.py` - Alla fält och beskrivningar
- **Anthropic**: `components/anthropic/anthropic.py` - Alla fält och felmeddelanden
- **Google Generative AI**: `components/google/google_generative_ai.py` - Komplett översättning
- **Groq**: `components/groq/groq.py` - Alla användarfält
- **Mistral**: `components/mistral/mistral.py` - Komplett översättning
- **Perplexity**: `components/perplexity/perplexity.py` - Alla fält

### 🗂️ Input/Output-komponenter (Slutförda)
- **Chat Input/Output**: `components/input_output/chat.py`, `chat_output.py` - Alla fält
- **Text Input/Output**: `components/input_output/text.py`, `text_output.py` - Komplett

### ⚙️ Processing-komponenter (Delvis slutförda)
- **Split Text**: `components/processing/split_text.py` - Komplett
- **Combine Text**: `components/processing/combine_text.py` - Komplett
- **Prompt Template**: `components/processing/prompt.py` - Komplett
- **Filter Data**: `components/processing/filter_data.py` - Komplett
- **Update Data**: `components/processing/update_data.py` - Komplett
- **Create Data**: `components/processing/create_data.py` - Komplett

### 🗄️ Vectorstore-komponenter (Delvis slutförda)
- **Chroma DB**: `components/vectorstores/chroma.py` - Komplett
- **Pinecone**: `components/vectorstores/pinecone.py` - Komplett
- **Qdrant**: `components/vectorstores/qdrant.py` - Komplett

### 🛠️ Tools-komponenter (Delvis slutförda)
- **Python REPL**: `components/tools/python_repl.py` - Komplett
- **Calculator**: `components/tools/calculator.py` - Komplett
- **Wikipedia API**: `components/tools/wikipedia_api.py` - Komplett

### 🧠 Memory/Logic-komponenter (Delvis slutförda)
- **Memory**: `components/helpers/memory.py` - Komplett
- **If-Else Router**: `components/logic/conditional_router.py` - Komplett
- **Agent**: `components/agents/agent.py` - Delvis

### 📊 Data-komponenter (Delvis slutförda)
- **API Request**: `components/data/api_request.py` - Delvis
- **File**: `components/data/file.py` - Delvis

### 🔗 Embeddings & Retrieval (Delvis slutförda)
- **Text Embedder**: `components/embeddings/text_embedder.py` - Komplett
- **Retrieval QA**: `components/langchain_utilities/retrieval_qa.py` - Komplett

## ❌ Återstående översättningar

### 🎯 Hög prioritet
1. **AI/LLM-leverantörer** (många kvar):
   - Cohere, Hugging Face, Azure OpenAI, Ollama, LM Studio
   - Vertex AI, AWS Bedrock, IBM Watson, Cloudflare
   - DeepSeek, Maritalk, XAI, Novita, SambaNova

2. **Vectorstores** (många kvar):
   - FAISS, Weaviate, MongoDB Atlas, Elasticsearch
   - Redis, Supabase, Upstash, AstraDB, Cassandra
   - Milvus, PGVector, ClickHouse, Couchbase

3. **Data Sources** (många kvar):
   - Directory, URL, CSV to Data, JSON to Data
   - SQL Executor, Web Search, RSS, News Search
   - Webhook

### 🔧 Medel prioritet
4. **Tools** (många kvar):
   - Google Search, SerpAPI, Tavily Search
   - Yahoo Finance, Wikidata, SearXNG

5. **Processing** (många kvar):
   - Parse Data, Extract Key, JSON Cleaner
   - Regex, Save File, Structured Output, Parser

6. **Specialiserade tjänster**:
   - **Notion**: Add Content, Create Page, List Pages
   - **YouTube**: Search, Transcripts, Comments
   - **Google**: Gmail, Drive, Calendar, Search
   - **Composio**: GitHub, Slack, Outlook
   - **Firecrawl**: Scrape, Crawl, Extract

### 📝 Låg prioritet
7. **Text Splitters**: Character, Recursive Character, Language
8. **Output Parsers**: Alla output parsers
9. **Nischade tjänster**: AssemblyAI, TwelveLabs, Unstructured

## 📋 Översättningsriktlinjer

### ✅ VAD SOM SKA ÖVERSÄTTAS
- `display_name` - Komponentnamn som visas i UI
- `description` - Komponentbeskrivningar
- `info` - Hjälptexter för fält
- Felmeddelanden som visas för användare
- Statusmeddelanden
- E-postmallar och användarmeddelanden

### ❌ VAD SOM INTE SKA ÖVERSÄTTAS
- `name` - Tekniska komponentnamn (används internt)
- API-endpoints och URL:er
- Tekniska konstanter och enum-värden
- Databasfältnamn
- Funktionsnamn och variabelnamn
- Tekniska termer som "API", "JSON", "HTTP", "gRPC"
- Programmeringsspråk och biblioteksnamn

### 🎯 Kvalitetsstandarder
- **Naturlig svenska**: Använd idiomatisk svenska, inte ordagrann översättning
- **Konsistent terminologi**: Använd samma svenska termer genomgående
- **Teknisk precision**: Behåll teknisk korrekthet
- **Användarfokus**: Tänk på slutanvändarens perspektiv

### 📝 Exempel på korrekt översättning
```python
# ✅ KORREKT
display_name="Textinmatning"
info="Ange den text som ska bearbetas."

# ❌ FEL - översätt inte tekniska namn
name="text_input"  # Behåll som original
```

## 🚀 Nästa steg

1. **Fortsätt med hög prioritet**: AI/LLM-leverantörer och Vectorstores
2. **Systematisk genomgång**: En kategori i taget
3. **Kvalitetskontroll**: Granska översättningar för konsistens
4. **Testning**: Verifiera att UI fungerar korrekt med svenska texter

## 📊 Framsteg

- **Backend Core**: 100% ✅
- **Komponenter**: ~35% ✅
- **Totalt projekt**: ~60% ✅

---

*Senast uppdaterad: 2025-01-26*
*Branch: swedishbackend*
