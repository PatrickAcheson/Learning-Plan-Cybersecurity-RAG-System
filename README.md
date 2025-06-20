# Intern Plan: Cybersecurity RAG System using LLMs & Embeddings

This plan will outline a 9-week structured mentorship plan for an introduction to Retrieval-Augmented Generation (RAG) and Large Language Models. Aimed practical learning for vector search, backend development, and LLM/RAG application in InfoSec.

---

## Week-by-Week Plan

### Week 1 – Foundations of LLMs & RAG

**Goals:**
- Understand what LLMs are and how they work
- Learn about basics of transformers, embeddings, and RAG basics
- Find what llm can run on cpu

**Topics:**
- What are LLMs? (GPT, Mistral, LLaMA)
- Tokenization and embeddings
- What is RAG and why it matters in InfoSec
  
**Other things to learn basic of**
- Git & GitHub	Version control for your project repo	GitHub Docs > Hello World
- Python Basics	All glue code, APIs, and scripts will be in Python	> w3schools Python or RealPython
- Virtual Environments	> Keep packages clean for Python projects	python -m venv tutorial or [RealPython guide](https://realpython.com/python-virtual-environments-a-primer/)
- Using APIs (REST)	Understand how FastAPI and HTTP requests work	> Intro to APIs or FastAPI crash course ([link](https://documenter.getpostman.com/view/664302/S1ENwy59))
- What is JSON?	Work with ticket data and APIs	> [JSON Crash Course](https://dev.to/talibackend/json-crash-course-4pof)

**Resources:**
- Hugging Face [NLP Course](https://huggingface.co/learn/nlp-course/chapter1)
- "Transformer Language Model" [Link](https://www.youtube.com/watch?v=-QH8fRhqFHM)
- “Retrieval-Augmented Generation Explained” [RAG Video](https://youtu.be/5Y3a61o0jFQ?feature=shared)
- Basic RAG: [link](https://docs.mistral.ai/guides/rag/)

---
## Week 2 - Pratical creation of Vectors

### Monday - Tuesday (not hard deadline)

**Goals:**
- Finish HuggingFace Course and Watch Intro videos for above.
- Complete RAG course using (wine data first, then security one).
- Create persistant vector store (no using in memory) & Find method of visualising the vector store

**Tasks**
- Install Github desktop
- Create virtual enviroment (example. python -m venv myenv)
- Initialise Repo with (.gitignore)
- Install Juypter notebook, and git clone course ( [link](https://github.com/alfredodeza/learn-retrieval-augmented-generation/tree/main)) **note** add your own LLM into the part that talks about APIs
- Work through Juypter notebooks and comment them (make commits often)
- Use dataset and vectorise the sample security tickets and do some testing. [link](https://github.com/PatrickAcheson/Learning-Plan-Cybersecurity-RAG-System/blob/main/Ticket%20Details.xlsx)
- Visualise the vectorstore [link](https://medium.com/@sarmadafzalj/visualize-vector-embeddings-in-a-rag-system-89d0c44a3be4)

**Extra**

1. Comment codebase and explain decisions made during design changes.
2. Build clean CLI chat back and forward.
3. Start beblow tasks (goal here is that he user could ask about a CVE and it could either find the vector that has the CVE make API call command:


================================================================================================================

Gather theat intelligence and vuln data from free APIs, efficently add new data to a new collection or vector
  - NVD API [link](https://nvd.nist.gov/developers/vulnerabilities)
  - CVE API by CIRCL [link](https://cve.circl.lu/api/)
  - CISA KEV Catalog [link](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
  - GreyNoise [link](https://docs.greynoise.io/reference/get_v3-community-ip)
    
What to vectorize:
  - CVE ID, description, CVSS score
  - Affected vendors/products
  - Attack vector, privileges required, impact
  - Fix status / remediation
  - CISA "known exploited" tag

### Attempt to enrich results or find details and steps to mitigation for CVE identified in ticket data.

- seperate api data collection in scheduled process. (cron job every 4 hours)
- token streaming?

**Harder**
Attempt to create actions with the LLM, where key works or arguments for example (/search-software) creates a call to an API and brings results into LLM context window (or vectorizes it)
  - Virus Total API [link](https://docs.virustotal.com/reference/overview)
  - Hybrid Analysis [link](https://www.hybrid-analysis.com/docs/api/v2)


...**more to be added here**

### Week 10 - Goal - Prototype

![image](https://github.com/user-attachments/assets/cbedec45-a711-4965-bd49-839017ebb7f8)
