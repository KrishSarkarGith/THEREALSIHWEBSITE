## API Endpoints

| Endpoint         | Method | Description                                | Usage       |
|------------------|--------|--------------------------------------------|-------------|
| `/api/health`    | GET    | Check if backend server is running         | External (frontend → backend) |
| `/api/careers`   | GET    | Fetch list of careers from dataset         | External (frontend → backend) |
| `/api/assess`    | POST   | Submit quiz data → return recommendations  | External (frontend → backend) |

---

## Internal Backend Flow

- **`app.py`** → Defines API routes and handles requests.  
- **`models/recommender.py`** → ML logic (TF-IDF + cosine similarity).  
- **`models/data/careers.json`** → Dataset of careers used for recommendations.  
