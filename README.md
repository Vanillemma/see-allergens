#  See Allergy — Food Allergen Explorer
 
> A Big Data web application for browsing, filtering, and analyzing food product catalogs with allergen detection and personalized allergy profiling.
 
**Academic project** — Master 2 Econometrics & Statistics (Data & Cybersecurity track)  
**Date:** December 2025
 
---
 
##  Live Demo
 
🔗 **[https://seeallergy-production.up.railway.app](https://seeallergy-production.up.railway.app)**
 
> ⚠️ Hosted on Railway's free tier. Initial load may be slow due to cold start. Available until January 4, 2026.
 
---
 
##  Overview
 
See Allergy is a full-stack web application built to tackle a real-world problem: helping people with food allergies navigate large product catalogs quickly and safely. The app allows users to search and filter a dataset of ~12 million food products (≈1 GB), identify allergens across products, visualize global allergen statistics, and evaluate a personalized shopping basket against a custom allergy profile.
 
The project was developed as part of a Big Data course, with a focus on handling large-scale data through efficient indexing, server-side pagination, caching, and aggregation pipelines.
 
---
 
##  Features
 
### Product Catalog Explorer
- Full-text search across product fields, backed by a MongoDB text index
- Multi-criteria filters: supplier, main ingredient, sweetener, fat/oil, seasoning, allergens
- Dynamic sorting and server-side pagination (default page size: 12)
- Card and table display modes
### Thematic Index Navigation
- Browse products grouped by allergen, ingredient type, sweetener, fat, or seasoning
- Index values pre-computed server-side and cached for fast retrieval
### Analytics Dashboard
- Interactive charts built with **Chart.js** and **D3.js**
- Visualizations include: top allergens, allergen co-occurrence graph, distribution by ingredient, safe vs. allergen-containing product ratio, most frequent ingredients
### Allergy-Aware Basket
- Add products to a personal basket
- Define a custom allergy profile
- Automatic compatibility check for each product
- Global allergen summary across the entire basket
---
 
##  Tech Stack
 
| Layer | Technology |
|---|---|
| **Backend** | Python, Flask, PyMongo |
| **Database** | MongoDB (hosted on MongoDB Atlas) |
| **Frontend** | HTML, CSS, Vanilla JavaScript |
| **Data Visualization** | Chart.js, D3.js |
| **CSV Parsing** | PapaParse |
| **Deployment** | Railway + GitHub |
| **Data Generation** | Custom Python script (`Randomisation.py`) |
 
---
 
##  Project Structure
 
```
See_Allergy/
│
├── backend/
│   ├── app.py               # Main Flask API
│   ├── index.html           # Single-page frontend (served by Flask)
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Environment variables (MongoDB URI, config)
│
├── bench_all/               # Benchmark scripts (Python)
├── bench_results/           # Raw benchmark output (CSV)
├── bench_summary/           # Aggregated benchmark summaries
│
└── data/
    ├── Randomisation.py         # Generates ~1 GB dataset (12M products)
    ├── Randomisation10k.py      # Generates 10,000-product sample
    ├── create_indexes.py        # Creates MongoDB indexes
    ├── migrate_allergens_to_array.py  # Data cleanup script
    ├── allergens_clean.csv      # Cleaned allergen data (from Kaggle)
    └── allergens_demo.csv       # Reduced demo dataset (10k products)
```
 
---
 
##  Dataset
 
The original source dataset was only a few kilobytes — far too small for a Big Data context. A custom Python script (`Randomisation.py`) was developed to generate a synthetic dataset of ~12 million unique food products (~1 GB).
 
**Generation logic:**
- Each product is a unique combination of: **Food name × Store prefix × Commercial suffix**
- A mathematical permutation system (using a coprime coefficient) guarantees no duplicates across all combinations
- Additional attributes are randomized per product: main ingredient, sweetener, fat/oil, seasoning, and 0–3 allergens (drawn from a controlled probability distribution)
This approach produces a large, coherent, realistic dataset suitable for Big Data workloads while remaining entirely synthetic.
 
---
 
##  API Quickstart
 
Base URL: `https://seeallergy-production.up.railway.app`  
All API routes are prefixed with `/api`. Responses follow a consistent JSON structure with a success flag, optional message, and data payload. Standard HTTP error codes are used (400, 404, 500…).
 
### Endpoints Overview
 
#### `GET /api/products`
Returns a paginated, filterable list of products.
 
**Query parameters:**
 
| Parameter | Description |
|---|---|
| `page` | Page number (default: 1) |
| `size` | Page size (default: 12) |
| `sort` | Field to sort by |
| `search` | Full-text search term |
| `allergen` | Filter by allergen name |
| `ingredient` | Filter by main ingredient |
| `supplier` | Filter by supplier/prefix |
 
**Example:**
```
GET /api/products?page=1&size=12&search=organic&allergen=gluten
```
 
#### `POST /api/products`
Add a new product to the catalog (JSON body required).
 
#### `PUT /api/products/<id>`
Update an existing product by ID.
 
#### `DELETE /api/products/<id>`
Delete a product by ID.
 
---
 
#### `POST /api/import/csv`
Upload and import a CSV file into MongoDB. The file must follow the project's data schema (see `allergens_clean.csv` for reference).
 
#### `GET /api/export/csv`
Export the current product catalog as a downloadable CSV file.
 
---
 
#### `GET /api/stats/indexes`
Returns pre-computed thematic indexes grouped by allergen, ingredient, sweetener, fat, and seasoning. Results are cached server-side after the first request.
 
#### `GET /api/stats/analytics`
Returns advanced analytics: top allergens, co-occurrence matrix, ingredient distributions, safe vs. unsafe product ratios. Computed in Python over the full dataset — first call is slow, subsequent calls use cache.
 
---
 
## Local Installation
 
### Prerequisites
- Python 3.9+
- MongoDB instance (local or MongoDB Atlas)
- Git
### Steps
 
```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/see-allergy.git
cd see-allergy/backend
 
# 2. Create a virtual environment and activate it
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
 
# 3. Install dependencies
pip install -r requirements.txt
 
# 4. Configure environment variables
# Create a .env file in /backend with:
# MONGODB_URI=mongodb+srv://<user>:<password>@cluster.mongodb.net/see_allergy
# FLASK_ENV=development
 
# 5. Generate a demo dataset (optional)
cd ../data
python Randomisation10k.py
 
# 6. Create MongoDB indexes
python create_indexes.py
 
# 7. Run the Flask app
cd ../backend
flask run
```
 
The app will be available at `http://localhost:5000`.
 
---
 
##  Deployment
 
The application is deployed on **[Railway](https://railway.app)** using the following setup:
 
- **Root directory:** `backend/`
- **Install command:** `pip install -r requirements.txt`
- **Start command:** `gunicorn app:app`
- **Environment variables:** `MONGODB_URI` and any other secrets are stored directly in Railway (not committed to the repo)
- **Database:** MongoDB Atlas (cloud-hosted)
The deployed URL serves both the frontend (`index.html`) and the REST API from the same Flask process.
 
---
 
##  Performance & Benchmarks
 
All benchmarks were run against the full ~1 GB dataset (12M+ products). The test suite measured: average latency, P95 latency, throughput (req/s), pagination impact, and cache effects — at concurrency levels of 1, 5, 10, and 20 threads.
 
### Key Findings
 
| Metric | Observation |
|---|---|
| **Throughput** | Scales from ~0.36 req/s (1 thread) to ~1.47 req/s (10+ threads), then plateaus |
| **Latency** | Remains stable at low concurrency; degrades under 10–20 simultaneous requests |
| **Pagination** | Page size 12 is the optimal trade-off between speed and data volume |
| **P95 latency** | Grows significantly with large page sizes (200 items); much more stable at size 12 |
| **Cache (cold)** | Analytics and index endpoints are slow on first call due to heavy aggregations |
| **Cache (warm)** | Response time drops drastically once cache is populated — essential for analytics |
| **Text search** | Higher latency than standard browsing, but manageable thanks to MongoDB text indexes |
 
> Flask's single-process architecture naturally caps throughput. It handles standard interactive usage well, but is not suited for high-concurrency production loads without additional infrastructure (e.g., Gunicorn workers, load balancing).
 
---
 
##  Known Limitations
 
- **No authentication:** The API and admin operations (POST, PUT, DELETE) are publicly accessible. No user roles or session management.
- **Analytics cost:** Global statistics are computed on-demand over millions of documents. Without caching, cold calls can be very slow.
- **Flask concurrency ceiling:** Throughput plateaus around 1.47 req/s, which is adequate for academic/demo use but insufficient for production-scale traffic.
- **No distributed caching:** The current in-memory cache is local to the process and resets on restart. A Redis-based cache would be more robust.
- **Dataset is synthetic:** The 12M-product dataset is artificially generated. Real-world product data would have different distributions and edge cases.
---
 
##  Possible Improvements
 
- **Pre-computed analytics:** Schedule background jobs to refresh analytics endpoints rather than computing on every cold request
- **Authentication & roles:** Add user accounts with JWT or session-based auth, with separate read/write/admin permissions
- **Distributed cache:** Replace in-memory caching with Redis for persistence and multi-worker support
- **Async workers:** Replace or supplement Flask with an async framework (e.g., FastAPI + async MongoDB) to handle higher concurrency
- **Real product data:** Integrate actual open food databases (e.g., Open Food Facts) for more realistic content
- **Mobile-first UI:** Improve responsiveness and accessibility of the frontend interface
---
 
 
##  Key References
 
- [Flask Documentation](https://flask.palletsprojects.com/)
- [MongoDB Manual](https://www.mongodb.com/docs/manual/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [Chart.js Documentation](https://www.chartjs.org/docs/latest/)
- [D3.js Reference](https://d3js.org/)
- Fielding, R. T. (2000). *Architectural Styles and the Design of Network-based Software Architectures*. UC Irvine.
- Gandomi, A. & Haider, M. (2015). Beyond the hype: Big data concepts, methods, and analytics. *IJIM, 35*(2), 137–144.
---
 
*This project was developed for academic purposes as part of a Big Data & Web Development course. It is not intended for production deployment.*
