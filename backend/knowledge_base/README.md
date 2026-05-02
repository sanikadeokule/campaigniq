# CampaignIQ Knowledge Base

Domain-grounded knowledge base for the CampaignIQ AI Advisor (RAG layer for `POST /advisor`).

This directory contains 12 markdown documents organized by topic. Each document is self-contained and chunkable for vector embedding. The advisor endpoint should retrieve the top-K most relevant chunks (recommended: K=3–5) and pass them as context to the LLM.

---

## Document Index

| # | File | Topic | Best For |
|---|---|---|---|
| 01 | `01_dataset_overview.md` | Dataset schema, target variable, data quality fixes, feature engineering | "What data is this based on?" |
| 02 | `02_metrics_glossary.md` | CTR, CPC, CPA, ROAS, conversion rate, bounce rate definitions + benchmarks | "What is X?" / "Is my X good?" |
| 03 | `03_channel_deep_dive.md` | Search/Social/Display/Email/Video/Affiliate revenue ranks + recommendations | "Which channel performs best?" |
| 04 | `04_region_audience_device.md` | Region/audience/device performance with counter-intuitive findings | "Where should I target?" |
| 05 | `05_model_behavior.md` | Ridge model selection, SHAP rankings, coefficient interpretation | "How does the model work?" |
| 06 | `06_bcg_matrix_tiers.md` | Star/Core/Question/Dog tier system, distribution, action plans | "What does Star tier mean?" |
| 07 | `07_success_churn_classification.md` | Success classifier, churn classifier, audience classifier (and its known failures) | "Is my campaign at risk?" |
| 08 | `08_actionable_playbooks.md` | 12 if-then playbooks for common campaign problems | "My ROAS is low, what do I do?" |
| 09 | `09_digital_marketing_fundamentals.md` | Funnel, attribution, targeting, bidding, A/B testing — general domain | "How does retargeting work?" |
| 10 | `10_optimization_strategies.md` | How to improve conversion rate, CTR, ROAS, bounce rate, Quality Score | "How do I improve X?" |
| 11 | `11_faq_qa_pairs.md` | 20+ Q&A pairs structured for direct retrieval | Direct question matching |
| 12 | `12_model_caveats_limitations.md` | Known limitations, when not to trust predictions, ethical caveats | "Can I trust this prediction?" |

---

## RAG Implementation Notes

### Recommended chunking strategy

- **Header-based chunking**: split each `.md` file on H2 (`##`) and H3 (`###`) headers. This preserves topical coherence — each chunk has a clear focus.
- **Chunk size**: aim for 400–800 tokens per chunk. Most sections in these docs are already in that range.
- **Overlap**: 50–100 token overlap between chunks helps preserve context across boundaries.

### Recommended embedding model

For English text in this domain, any of:
- `text-embedding-3-small` (OpenAI, cost-effective)
- `text-embedding-3-large` (OpenAI, higher quality)
- `sentence-transformers/all-MiniLM-L6-v2` (local, free)

### Recommended retrieval setup

- **Vector store**: ChromaDB, FAISS, or pgvector (for production with PostgreSQL).
- **Top-K**: 3–5 chunks per query. More context isn't always better — focus matters.
- **Rerank**: use a cross-encoder rerank step (e.g., `bge-reranker-base`) for higher precision.

### Suggested system prompt for the advisor

> You are CampaignIQ Advisor, an AI assistant for digital marketing campaign optimization. You have access to a knowledge base of dataset findings, model behavior, marketing fundamentals, and actionable playbooks. When answering:
>
> 1. Ground answers in the retrieved knowledge base context — cite specific numbers (revenue figures, conversion rates, model accuracy) rather than generic claims.
> 2. Lead with the direct answer, then expand with detail.
> 3. Prefer dataset-specific findings (Search ~$32.8K avg, Gen X tied with Gen Z, etc.) over generic industry advice.
> 4. End with one concrete next step the user can take.
> 5. When the model's reliability is in question, surface the relevant caveats from doc 12.
> 6. If the user asks something the knowledge base doesn't cover, say so — don't fabricate.

### Filtering hints (for hybrid retrieval)

When the user query mentions specific topics, you can pre-filter or boost relevant docs:

| User mentions | Boost |
|---|---|
| "channel", "Search", "Display", "Video", "Email", "Social", "Affiliate" | doc 03 |
| "region", "East", "West", "audience", "Gen X", "Gen Z", "device", "tablet", "mobile" | doc 04 |
| "model", "Ridge", "SHAP", "accuracy", "R²", "predict" | doc 05 |
| "tier", "Star", "Dog", "BCG", "Question Mark", "Core" | doc 06 |
| "successful", "success", "churn", "at risk", "audience classifier" | doc 07 |
| "what should I do", "how do I fix", "my ROAS is low", "playbook" | doc 08 |
| "what is", "definition", "funnel", "attribution", "retargeting" | doc 09 |
| "improve", "optimize", "increase", "reduce" | doc 10 |
| "trust", "reliable", "limitation", "wrong", "inaccurate" | doc 12 |

The FAQ doc (11) is a strong candidate for **always retrieve** in addition to topical docs, because each Q&A is a self-contained match for direct user questions.

---

## Key Numbers to Always Preserve

The previous knowledge base felt "too generic" because it lacked these specifics. Always keep them in retrieved context:

- **2,540 campaigns** in dataset, 2,504 after dedup
- **Test R² = 0.887** (model accuracy on dollar scale)
- **MAE = $5,788** (typical error, more honest than RMSE)
- **Median ROAS = 3.06x**
- **Median revenue = $8,259**
- **Success threshold = $19,096** (75th percentile)
- **Best channel: Search ~$32,800; Worst: Display ~$6,200**
- **Best audience tied: Gen X ($23K) and Gen Z ($22.8K)**
- **Best region: East ~$23,300**
- **Best device: Tablet ~$21,500**
- **Top SHAP driver: log_conversions (1.45) — 9x bigger than #2**
- **Tier distribution: 35.8% Star / 31.5% Core / 17.3% Question / 15.4% Dog**
- **Audience classifier accuracy: ~24% (broken — disclose this)**

---

## Maintenance

When the model is retrained on fresh data:
1. Update specific numbers in docs 01, 02, 03, 04, 05, 06, 07.
2. Doc 09 (general domain knowledge) usually doesn't need changes.
3. Doc 12 (caveats) should be reviewed for any new known issues.
4. Re-embed all docs after edits.

---

## Backend Integration Sketch

```python
# In backend/main.py or a new backend/rag.py

from pathlib import Path
import chromadb

KB_DIR = Path(__file__).parent / "knowledge_base"

def load_kb_chunks():
    """Load and chunk all .md files in the knowledge base."""
    chunks = []
    for md_file in sorted(KB_DIR.glob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        # Split on H2 headers, preserving the header in each chunk
        sections = re.split(r"\n## ", text)
        for i, section in enumerate(sections):
            chunk_text = ("## " + section) if i > 0 else section
            chunks.append({
                "source": md_file.name,
                "text": chunk_text.strip(),
            })
    return chunks

# Index once at startup
client = chromadb.Client()
collection = client.create_collection("campaigniq_kb")
chunks = load_kb_chunks()
collection.add(
    documents=[c["text"] for c in chunks],
    metadatas=[{"source": c["source"]} for c in chunks],
    ids=[f"chunk_{i}" for i in range(len(chunks))],
)

# At query time in /advisor endpoint
def retrieve_context(query: str, k: int = 4):
    results = collection.query(query_texts=[query], n_results=k)
    return "\n\n---\n\n".join(results["documents"][0])
```

This is a sketch — adapt to whichever vector store you choose.
