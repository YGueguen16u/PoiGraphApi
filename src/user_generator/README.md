# User Generator API

Une API FastAPI pour générer des faux utilisateurs pour une application de recommandation de POI.


## Installation

1. Clonez le dépôt
2. Installez les dépendances :
   ```
   pip install -r requirements.txt
   ```
3. Lancez le serveur :
   ```
   uvicorn main:app --reload
   ```

## Utilisation

L'API est disponible à l'adresse : `http://localhost:8000`

### Endpoints

- `GET /` : Page d'accueil avec la liste des endpoints disponibles
- `POST /users/generate/` : Génère des utilisateurs aléatoires
  - Paramètres (JSON) :


## Exemple de requête

```bash
curl -X 'POST' \
  'http://localhost:8000/users/generate/' \
  -H 'Content-Type: application/json' \
  -d '{
    "count": 3
  }'
```
