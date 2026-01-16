# Late Show Management API

A Flask REST API for managing late-night show episodes, guests, and their appearances.

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Seed the database with sample data:
   ```bash
   python seed.py
   ```

3. Run the application:
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5555`

## API Endpoints

### GET /
Returns API information and available endpoints.

**Response:**
```json
{
  "message": "Late Show Management API",
  "endpoints": {
    "GET /episodes": "Get all episodes",
    "GET /episodes/<id>": "Get episode with appearances",
    "GET /guests": "Get all guests",
    "POST /appearances": "Create new appearance"
  }
}
```

### GET /episodes
Returns a JSON array of all episodes.

**Response:**
```json
[
  {
    "id": 1,
    "date": "1/11/99",
    "number": 1
  },
  {
    "id": 2,
    "date": "1/12/99",
    "number": 2
  }
]
```

### GET /episodes/<id>
Returns a single episode with nested appearances data.

**Parameters:**
- `id` (integer): Episode ID

**Response:**
```json
{
  "id": 1,
  "date": "1/11/99",
  "number": 1,
  "appearances": [
    {
      "id": 1,
      "rating": 4,
      "guest_id": 1,
      "episode_id": 1,
      "guest": {
        "id": 1,
        "name": "Michael J. Fox",
        "occupation": "actor"
      }
    }
  ]
}
```

**Error Response (404):**
```json
{
  "error": "Episode not found"
}
```

### GET /guests
Returns a JSON array of all guests.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Michael J. Fox",
    "occupation": "actor"
  },
  {
    "id": 2,
    "name": "Sandra Bernhard",
    "occupation": "Comedian"
  }
]
```

### POST /appearances
Creates a new appearance.

**Request Body:**
```json
{
  "rating": 4,
  "episode_id": 1,
  "guest_id": 1
}
```

**Response (201):**
```json
{
  "id": 1,
  "rating": 4,
  "guest_id": 1,
  "episode_id": 1,
  "guest": {
    "id": 1,
    "name": "Michael J. Fox",
    "occupation": "actor"
  },
  "episode": {
    "id": 1,
    "date": "1/11/99",
    "number": 1
  }
}
```

**Error Responses:**
- **400 Bad Request** - Missing required fields or validation errors
```json
{
  "error": "Missing required fields: rating, episode_id, guest_id"
}
```
```json
{
  "error": "Rating must be an integer between 1 and 5"
}
```
```json
{
  "error": "Episode not found"
}
```

## Database Models

### Episode
- `id` (Integer, Primary Key)
- `date` (String, Required)
- `number` (Integer, Required)
- Relationships: Has many appearances

### Guest
- `id` (Integer, Primary Key)
- `name` (String, Required)
- `occupation` (String, Optional)
- Relationships: Has many appearances

### Appearance
- `id` (Integer, Primary Key)
- `rating` (Integer, Required, 1-5)
- `episode_id` (Integer, Foreign Key)
- `guest_id` (Integer, Foreign Key)
- Relationships: Belongs to episode, belongs to guest

## Sample Data

After running the seed script, the database contains:

**Episodes:**
- Episode #1: January 11, 1999
- Episode #2: January 12, 1999

**Guests:**
- Michael J. Fox (actor)
- Sandra Bernhard (Comedian)
- Tracey Ullman (television actress)

**Appearances:**
- Michael J. Fox on Episode #1 (rating: 4)
- Tracey Ullman on Episode #2 (rating: 5)

## Testing

You can test the API using tools like Postman or curl:

```bash
# Get all episodes
curl http://localhost:5555/episodes

# Get specific episode with appearances
curl http://localhost:5555/episodes/1

# Get all guests
curl http://localhost:5555/guests

# Create a new appearance
curl -X POST http://localhost:5555/appearances \
  -H "Content-Type: application/json" \
  -d '{"rating": 3, "episode_id": 1, "guest_id": 2}'
