# DriftDater - Dating Application

A full-stack dating application built with Vue 3 (frontend) and Flask (backend).

## Features

- **User Authentication**
  - Registration with email validation
  - Secure login/logout with JWT tokens
  - Password hashing with bcrypt

- **Profile Management**
  - Create and edit user profiles
  - Profile fields: name, age, bio, location, interests, gender, occupation, relationship goals
  - Profile picture upload
  - Profile visibility controls (public/private)

- **Email Verification**
  - Email verification via Mailtrap (fake SMTP)

## Tech Stack

- **Frontend:** Vue 3, Vue Router, Axios
- **Backend:** Flask, Flask-SQLAlchemy, Flask-Bcrypt, Flask-CORS
- **Database:** SQLite (development) / PostgreSQL (production)
- **Authentication:** JWT tokens

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Mailtrap account (for email testing)

### Setup

1. **Install Python dependencies:**
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

2. **Install Node.js dependencies:**
```bash
npm install
```

3. **Configure Mailtrap:**
Edit `.env` file with your Mailtrap credentials:
```
MAILTRAP_SMTP_USER=your_mailtrap_user
MAILTRAP_SMTP_PASS=your_mailtrap_password
```

### Running the Application

**Option 1 - Start both servers:**
```bash
./start.sh
```

**Option 2 - Start separately:**

Terminal 1 (Backend):
```bash
./start-backend.sh
# or
source .venv/bin/activate
python run.py
```

Terminal 2 (Frontend):
```bash
./start-frontend.sh
# or
npm run dev
```

### Access

- Frontend: http://localhost:5173
- Backend API: http://localhost:5000

## Testing

Run the test suite:
```bash
./run-tests.sh
# or
source .venv/bin/activate
pytest tests/ -v
```

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| GET | `/api/auth/verify/<token>` | Verify email |
| POST | `/api/auth/login` | Login |
| POST | `/api/auth/logout` | Logout |
| GET | `/api/auth/me` | Get current user |

### Profile
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/profile` | Get my profile |
| POST | `/api/profile` | Create profile |
| PUT | `/api/profile` | Update profile |
| POST | `/api/profile/picture` | Upload profile picture |
| GET | `/api/profile/<id>` | View other profile |

## Project Structure

```
datingApp/
├── app/
│   ├── __init__.py      # Flask app factory
│   ├── config.py        # Configuration
│   ├── models.py        # Database models
│   ├── forms.py        # WTForms
│   └── views.py         # API endpoints
├── src/
│   ├── views/          # Vue views
│   ├── components/     # Vue components
│   ├── services/       # API services
│   └── router/         # Vue router
├── tests/              # Test suite
├── uploads/            # Uploaded files
├── run.py              # Flask entry point
└── start.sh            # Start script
```

## Database

The application uses SQLite by default for development. To use PostgreSQL:

1. Update `.env`:
```
DATABASE_URL=postgresql://user:pass@localhost/driftdater
SQLALCHEMY_DATABASE_URI=postgresql://user:pass@localhost/driftdater
```

2. Create the database:
```bash
createdb driftdater
```

## License

MIT
