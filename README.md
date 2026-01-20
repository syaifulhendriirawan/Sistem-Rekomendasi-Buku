# 📚 Book Recommendation System

A production-ready book recommendation engine using **collaborative filtering** with K-Nearest Neighbors. Built with **React** frontend and **FastAPI** backend, demonstrating modern full-stack architecture patterns.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18+-61DAFB?logo=react&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎯 The Problem

> **"How do you make personalized recommendations when you have millions of user-book interactions but limited compute resources?"**

This project tackles a real-world challenge faced by platforms like Goodreads, Amazon, and Netflix: finding the right balance between **recommendation quality**, **computational efficiency**, and **system maintainability**.

---

## ⚡ Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) and start exploring!

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   React     │  │   Zustand   │  │ React Router│         │
│  │ Components  │  │    Store    │  │   Routing   │         │
│  └──────┬──────┘  └──────┬──────┘  └─────────────┘         │
│         │                │                                   │
│         └────────┬───────┘                                   │
│                  ▼                                           │
│         ┌───────────────┐                                   │
│         │  API Client   │                                   │
│         └───────┬───────┘                                   │
└─────────────────┼───────────────────────────────────────────┘
                  │ REST API
┌─────────────────┼───────────────────────────────────────────┐
│                 ▼              Backend                       │
│         ┌───────────────┐                                   │
│         │   FastAPI     │                                   │
│         │   Routes      │                                   │
│         └───────┬───────┘                                   │
│                 ▼                                            │
│         ┌───────────────┐                                   │
│         │   Services    │                                   │
│         │    Layer      │                                   │
│         └───────┬───────┘                                   │
│                 ▼                                            │
│  ┌──────────────────────────────────────────────┐          │
│  │              ML Pipeline                      │          │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ │          │
│  │  │Ingest  │→│Validate│→│Transform│→│ Train │ │          │
│  │  └────────┘ └────────┘ └────────┘ └────────┘ │          │
│  └──────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

### Tech Stack

| Layer | Technology | Why |
|-------|------------|-----|
| **Frontend** | React + Vite | Fast HMR, modern build tooling |
| **State** | Zustand | Lightweight, simple API (vs Redux) |
| **Backend** | FastAPI | Async, auto-docs, type validation |
| **ML** | scikit-learn KNN | Fast inference, interpretable |
| **Data** | Pandas + SciPy sparse | Memory-efficient for large matrices |

---

## 🧠 Key Engineering Decisions

### 1. Why KNN Over Deep Learning?

| Approach | Inference Time | Memory | Interpretability |
|----------|---------------|--------|------------------|
| Neural Collaborative Filtering | ~200-500ms | High (GPU) | Low |
| Matrix Factorization (SVD) | ~100ms | High | Medium |
| **K-Nearest Neighbors** ✓ | **~50ms** | **Low** | **High** |

**Decision**: KNN with cosine similarity delivers sub-100ms inference while remaining interpretable. When a recommendation seems wrong, I can trace exactly which books influenced it—impossible with neural networks.

**Trade-off accepted**: KNN may miss complex patterns (e.g., "users who liked A and B but not C tend to like D"). For this scale, the trade-off is acceptable.

### 2. Layered Pipeline vs Monolithic Script

Instead of a single `train.py` script, I implemented a **4-stage pipeline**:

```
DataIngestion → DataValidation → DataTransformation → ModelTrainer
```

**Benefits**:

- **Testable**: Can test validation without downloading data
- **Resumable**: If transformation fails, don't re-download 100MB
- **Configurable**: Change parameters via config, not code
- **Observable**: Each stage logs independently

### 3. API-First Architecture

**Before** (Streamlit): UI and ML logic tightly coupled

```python
if st.button('Recommend'):
    model = pickle.load(...)  # ❌ Loading in UI code
    results = model.kneighbors(...)
```

**After** (React + FastAPI): Clean separation

```
Frontend (React) ←→ REST API ←→ Backend (FastAPI) ←→ ML Model
```

**Why it matters**:

- Independent scaling (API handles 1000 req/s, frontend is CDN-cached)
- Team parallelization (frontend/backend can develop independently)
- Mobile-ready (same API powers iOS/Android)
- Testable (API tested without rendering UI)

---

## 📁 Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── config.py            # Pydantic settings
│   │   ├── api/routes/          # API endpoints
│   │   ├── services/            # Business logic
│   │   ├── models/              # Pydantic schemas
│   │   └── utils/               # Logging, exceptions
│   ├── artifacts/               # ML model & data
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/          # Reusable UI (BookCard, etc.)
│   │   ├── features/            # Feature modules
│   │   ├── stores/              # Zustand state
│   │   └── lib/                 # API client, utils
│   └── package.json
│
└── notebook/                    # Original Jupyter analysis
```

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/books` | GET | List all 700+ book titles |
| `/api/books/search?q=` | GET | Search books by title |
| `/api/recommendations?book=` | GET | Get 5 similar books |
| `/health` | GET | Health check with model status |

### Example Response

```json
GET /api/recommendations?book=1984&n=5

{
  "query_book": "1984",
  "recommendations": [
    {
      "title": "Animal Farm",
      "image_url": "https://...",
      "distance": 0.1523
    },
    ...
  ]
}
```

---

## 📊 Dataset

- **Source**: [Book-Crossing Dataset](http://www2.informatik.uni-freiburg.de/~cziegler/BX/)
- **Scale**: 1M+ ratings from 278K users on 271K books
- **Preprocessing**:
  - Users with <200 ratings filtered out
  - Books with <50 ratings filtered out
  - Final: ~700 books with dense rating patterns

---

## 🚀 Performance

| Metric | Value |
|--------|-------|
| API Response Time | <100ms (p99) |
| Model Inference | ~50ms |
| Frontend Bundle | ~150KB gzipped |
| Startup Time | ~3s (model loading) |

---

## 🛠️ Development

### Run Tests

```bash
cd backend
pytest tests/ -v
```

### Build Production

```bash
# Backend
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm run build
npm run preview
```

---

## 📝 What I Learned

1. **Simplicity wins**: KNN outperforms complex models for this use case
2. **Separation pays off**: API-first made testing and iteration 10x faster
3. **Pipelines > Scripts**: Modular ML code is debuggable ML code
4. **Type hints matter**: Pydantic caught bugs before they hit production

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

<p align="center">
  Built with ❤️ by <a href="https://github.com/syaifulhendriirawan">Syaiful Hendri Irawan</a>
</p>
