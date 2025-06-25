
# Intern Plan: Cybersecurity RAG System using LLMs & Embeddings

This condensed 4-week sprint covers the essentials of RAG, vector stores, GUI, RBAC, and model selection—optimized for a single-PC, internal setup.

---

## Week 1 – Introduction & Foundations

**Goals:**
- Understand what LLMs are and how they work  
- Learn the basics of transformers, embeddings, and RAG  
- Identify which LLMs can run on CPU  

**Topics & Tasks:**
1. **LLM & RAG Primer**  
   - What are LLMs? (GPT, Mistral, LLaMA)  
   - Tokenization and embeddings  
   - What is RAG and why it matters in InfoSec  
   - Watch “Transformer Language Model” [video](https://www.youtube.com/watch?v=-QH8fRhqFHM) and “Retrieval-Augmented Generation Explained” [RAG Video](https://youtu.be/5Y3a61o0jFQ?feature=shared)  
2. **Environment Setup**  
   - Install Git & GitHub Desktop; initialize repo with `.gitignore` (GitHub Docs > Hello World)  
   - Create a Python venv:  
     ```bash
     python -m venv tutorial
     ```  
     – [RealPython guide](https://realpython.com/python-virtual-environments-a-primer/)  
   - Install Jupyter Notebook; clone the RAG course repo:  
     https://github.com/alfredodeza/learn-retrieval-augmented-generation/tree/main  
3. **APIs & JSON Refresher**  
   - Learn REST/JSON basics: FastAPI crash course ([link](https://documenter.getpostman.com/view/664302/S1ENwy59))  
   - Do a JSON crash course: [JSON Crash Course](https://dev.to/talibackend/json-crash-course-4pof)  
   - Test simple HTTP calls in Python to a public API (e.g., JSONPlaceholder)

**Resources:**
- Hugging Face [NLP Course](https://huggingface.co/learn/nlp-course/chapter1)  
- Basic RAG guide: [Mistral Docs](https://docs.mistral.ai/guides/rag/)  

---

## Week 2 – Vector Store & RAG Prototype

### Monday – Tuesday (no hard deadline)

**Goals:**
- Finish the Hugging Face NLP course and intro videos  
- Complete the RAG course (wine data, then security data)  
- Create a persistent vector store (on-disk) and visualize it  

**Tasks:**
1. Install GitHub Desktop  
2. Create virtual environment:  
   ```bash
   python -m venv myenv

3. Initialize repo with `.gitignore`
4. Install Jupyter Notebook; clone the course repo
   ([alfredodeza/learn-retrieval-augmented-generation](https://github.com/alfredodeza/learn-retrieval-augmented-generation/tree/main))

   > **Note:** integrate your own LLM into the API sections
5. Work through the notebooks, commenting and committing often
6. Vectorize the sample security tickets:
   [Ticket Details.xlsx](https://github.com/PatrickAcheson/Learning-Plan-Cybersecurity-RAG-System/blob/main/Ticket%20Details.xlsx)
7. Visualize the vector store:
   [Visualize embeddings guide](https://medium.com/@sarmadafzalj/visualize-vector-embeddings-in-a-rag-system-89d0c44a3be4)

**Extra:**

1. Comment the codebase and document design decisions
2. Build a clean CLI for two-way chat
3. Start vulnerability-data ingestion:

   * NVD API ([link](https://nvd.nist.gov/developers/vulnerabilities))
   * CIRCL CVE API ([link](https://cve.circl.lu/api/))
   * CISA KEV Catalog ([link](https://www.cisa.gov/known-exploited-vulnerabilities-catalog))
   * GreyNoise ([link](https://docs.greynoise.io/reference/get_v3-community-ip))

**What to vectorize:**

* CVE ID, description, CVSS score
* Affected vendors/products
* Attack vector, privileges required, impact
* Fix status / remediation
* CISA “known exploited” tag

**Automation:**

* Schedule a cron job (every 4 hours) to refresh embeddings from API sources
* Experiment with token streaming

---

## Week 3 – Advanced RAG Extensions & Integrations

**Goals:**

* Automate ingestion of external vulnerability data
* Add slash-command style actions

**Tasks:**

1. **Automated Data Ingestion**

   * Scripts to pull from [NVD](https://nvd.nist.gov/developers/vulnerabilities), [CIRCL](https://cve.circl.lu/api/), CISA KEV, GreyNoise APIs every 4 hours ([cron](https://cronitor.io/guides/python-cron-jobs))
2. **Slash-Command Actions**

   * Define commands (e.g., `/search-cve CVE-2021-1234`)
   * Handlers to call VirusTotal ([link](https://docs.virustotal.com/reference/overview)) or Hybrid Analysis ([link](https://www.hybrid-analysis.com/docs/api/v2)) and vectorize results
3. **Error Handling & Logging**

   * Implement retries, rate-limit handling, and log to SQLite
4. **UX Prep**

   * Sketch wireframes for future GUI tabs (Chat, Admin) .ie [MIRO](https://miro.com/app/)
   * Draft JSON schemas for model config and user roles

---

## Week 4 – Test & Choose: Gradio vs. Streamlit GUI with RBAC & Model Selection

**Goals:**
- Spin up both Gradio and Streamlit versions of your RAG interface  
- Compare ease-of-use, feature support, and performance  
- Decide on the best framework for ongoing development  

**Tasks:**

1. **Prototype A – Gradio**  
   - `pip install gradio`  
   - Build a chat + model-selector UI:  
     - Chat input/output tied to your RAG backend  
     - Dropdown for LLMs (GPT-3.5, Mistral, LLaMA) sourced from JSON/YAML  
   - Implement lightweight RBAC:  
     - SQLite “users” table + simple login prompt  
     - Hide “Admin” tab unless `role == "admin"`  
   - Use Gradio’s `Tabs` for **Chat** vs. **Admin**, and `Dataframe` for vector-store stats  
   - Run on `localhost:7860` (optionally bind `0.0.0.0` for LAN)  

2. **Prototype B – Streamlit**  
   - `pip install streamlit`  
   - Create a Streamlit app with:  
     - Text input for chat, output area for model replies  
     - `st.selectbox` for model selection (same JSON/YAML config)  
   - Add RBAC:  
     - On first run, prompt for credentials via `st.sidebar` form  
     - Store session state role; show an “Admin” section only if `role == "admin"`  
   - Use Streamlit layout primitives (`st.tabs`, `st.sidebar`) to separate Chat/Admin  
   - Display vector-store stats via `st.dataframe` and any required plots  

3. **Compare & Evaluate**  
   - **Setup time**: how quickly did each prototype go from zero to chat?  
   - **Feature fit**: ease of dropdown, tabs, dataframes, streaming outputs  
   - **Customization**: flexibility of theming and layout  
   - **Performance**: responsiveness under typical query load  
   - **Deployment simplicity**: one-command launch, port binding, dependency footprint  

4. **Decision & Next Steps**  
   - Document your findings in a short table or bullet list in the repo README  
   - Agree on the framework to continue with for full integration  
   - Archive or remove the unused prototype  

**Resources:**
- Gradio Quickstart: https://gradio.app/get_started  
- Gradio + FastAPI: https://gradio.app/docs/#fastapi-integration  
- Streamlit Docs: https://docs.streamlit.io  
- Streamlit Authentication Patterns: https://discuss.streamlit.io/t/basic-authentication-patterns/6593  

**More to come here**

```
```
