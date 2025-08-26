# 🔧 Git Instructions för Swedish Translation

## 📋 Steg för att skapa branch och pusha ändringar

### 1. Öppna Command Prompt som vanlig användare (INTE admin)

### 2. Navigera till projektmappen
```cmd
cd C:\Users\mist24lk\Downloads\Backend
```

### 3. Kontrollera git status
```cmd
git status
```

### 4. Skapa och växla till ny branch
```cmd
git checkout -b swedishbackend
```

### 5. Lägg till alla ändrade filer
```cmd
git add .
```

### 6. Committa ändringarna
```cmd
git commit -m "feat: Add Swedish translation for backend core systems and components

- Translate all backend core systems (100% complete)
- Translate AI/LLM components: OpenAI, Anthropic, Google, Groq, Mistral, Perplexity
- Translate Input/Output components: Chat, Text
- Translate Processing components: Split Text, Combine Text, Prompt, Filter Data, etc.
- Translate Vectorstore components: Chroma, Pinecone, Qdrant
- Translate Tools: Python REPL, Calculator, Wikipedia API
- Translate Memory/Logic components
- Add comprehensive README with translation guidelines
- Focus on user-facing strings only, preserve technical terms"
```

### 7. Pusha till remote repository
```cmd
git push origin swedishbackend
```

### 8. Sätt upstream för framtida pushes
```cmd
git push --set-upstream origin swedishbackend
```

## 🔍 Verifiering

### Kontrollera att branch skapades
```cmd
git branch
```

### Kontrollera remote branches
```cmd
git branch -r
```

### Kontrollera commit history
```cmd
git log --oneline -5
```

## 📝 Viktiga filer som inkluderas

### Backend Core Systems
- `services/auth/utils.py`
- `services/email/service.py`
- `api/v1/*.py`
- `schema/*.py`
- `initial_setup/*.py`

### Komponenter
- `components/openai/openai.py`
- `components/anthropic/anthropic.py`
- `components/google/google_generative_ai.py`
- `components/groq/groq.py`
- `components/mistral/mistral.py`
- `components/perplexity/perplexity.py`
- `components/input_output/*.py`
- `components/processing/*.py`
- `components/vectorstores/chroma.py`
- `components/vectorstores/pinecone.py`
- `components/vectorstores/qdrant.py`
- `components/tools/*.py`
- `components/helpers/memory.py`
- `components/logic/conditional_router.py`
- `components/agents/agent.py`
- `components/data/*.py`
- `components/embeddings/text_embedder.py`
- `components/langchain_utilities/retrieval_qa.py`

### Dokumentation
- `README_SWEDISH_TRANSLATION.md`
- `GIT_INSTRUCTIONS.md`

## 🚨 Felsökning

### Om git inte hittas
```cmd
where git
```

### Om du behöver konfigurera git
```cmd
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Om remote inte är konfigurerad
```cmd
git remote add origin https://github.com/axiestudio/axiestudio.git
```

### Kontrollera remote URL
```cmd
git remote -v
```

---

*Kör dessa kommandon från vanlig Command Prompt (inte admin)*
