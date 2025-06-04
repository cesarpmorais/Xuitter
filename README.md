# Xuitter

## Running the project
We've used 'npm concurrently' to make the deploy process as simple as possible. To run both frontend and backend:
```
npm install -D concurrently
npm run setup-backend
npm run dev
```

## Backend
This is the backend for **Xuitter**, a minimalist Twitter-like platform built with Django and Django REST Framework. It allows users to post content, like, repost, comment, and retrieve interaction statistics.

### 1. Install Project Dependencies
`pip install -r requirements.txt`

### 2. Make Django Model Migrations
`python3 manage.py migrate`

### 3. Load initial data
`bash load_fixtures.sh`

### 4. Create Django Super user
`python3 manage.py createsuperuser`

### 5. Run Server
`python3 manage.py runserver`

### List Routes
`python manage.py show_urls --format=table`

### Run Tests
`python3 manage.py test`