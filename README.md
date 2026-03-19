# DriftDater - Dating Application

![Pytest](https://img.shields.io/badge/Pytest-150%20tests-green)
![Vitest](https://img.shields.io/badge/Vitest-106%20tests-blue)
![Playwright](https://img.shields.io/badge/Playwright-74%20tests-purple)

A full-stack dating application built with Vue 3 (frontend) and Flask (backend).

## Features

### User Authentication
- Registration with email validation
- Secure login/logout with JWT tokens
- Password hashing with bcrypt

### Profile Management
- Create and edit user profiles
- Profile fields: name, age, bio, interests, gender, occupation, relationship goals
- Age preferences (min/max range)
- Profile picture upload
- Profile visibility controls (public/private)

### Matching System
- **Algorithm** with scoring criteria:
  - Age compatibility - 20 points
  - Shared interests - 20 points (max 2)
  - Relationship goal match - 20 points
  - Gender preference - 15 points
  - **Minimum score: 50 points to appear in matches**
- Browse potential matches with filters (age, interests)
- Like/Dislike/Pass functionality
- Mutual match detection
- Real-time match notifications

### Notifications
- Real-time notifications via WebSocket
- Match notifications
- Like notifications

### Messaging System
- Real-time messaging between matched users
- Conversation list with unread counts
- Message history with pagination
- Typing indicator (shows when user is typing)
- Read receipts (✓ = sent, ✓✓ = read)
- Message limit: 1000 characters
- Automatic message cleanup after 90 days

### Search & Discovery
- Search profiles by:
  - Age range
  - Interests
  - Gender
  - Relationship goal
  - Occupation
- Sort options: newest, oldest, most similar, age
- Filter applied matches
- Save favorite/bookmarked profiles
- View and manage favorites

### Email Verification
- Email verification via Mailtrap (fake SMTP)

## Tech Stack

- **Frontend:** Vue 3, Vue Router, Axios, Socket.io Client
- **Backend:** Flask, Flask-SQLAlchemy, Flask-Bcrypt, Flask-CORS, Flask-SocketIO
- **Database:** SQLite (development) / PostgreSQL (production)
- **Authentication:** JWT tokens
- **Real-time:** WebSocket (Socket.IO)
- **Testing:** Pytest (backend), Vitest (frontend), Playwright (E2E)

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

### Backend Tests (Pytest)
```bash
./run-tests.sh
# or
source .venv/bin/activate
pytest tests/ -v
```

### Frontend Tests (Vitest)
```bash
npm test
```

### E2E Tests (Playwright)
```bash
npm run test:e2e        # Chromium only
npm run test:e2e:all    # All browsers (Chromium, Firefox, WebKit, Mobile Safari)
```

### Test Coverage Summary

| Test Suite | Tests | Description |
|------------|-------|-------------|
| Backend (Pytest) | 150 | Auth, Profile, Matching, Messaging, Search |
| Frontend (Vitest) | 106 | Components, Services, Composables |
| E2E (Playwright) | 74+ | Full user flows across browsers |

### Frontend Component Coverage

| Component | Coverage |
|-----------|----------|
| BaseAvatar.vue | 100% |
| BaseBadge.vue | 100% |
| BaseButton.vue | 100% |
| BaseInput.vue | 100% |
| AppFooter.vue | 100% |
| authService.js | ~50% |

### E2E Browser Support

| Browser | Status | Tests |
|---------|--------|-------|
| Chromium | ✅ Passing | 37 |
| Firefox | ✅ Passing | 37 |
| WebKit | ✅ Passing | 37 |
| Mobile Safari | ✅ Passing | 37 |

**Note:** WebKit and Mobile Safari require system dependencies:
```bash
sudo npx playwright install-deps
# or
sudo apt-get install libicu74 libjpeg-turbo8 gstreamer1.0-libav
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

### Matches
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/matches` | Get mutual matches |
| GET | `/api/matches/potential` | Get potential matches |
| POST | `/api/matches/like/<user_id>` | Like a user |
| POST | `/api/matches/dislike/<user_id>` | Dislike a user |
| POST | `/api/matches/pass/<user_id>` | Pass on a user |
| GET | `/api/matches/score/<user_id>` | Get match score |

### Notifications
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/notifications` | Get notifications |
| GET | `/api/notifications/unread-count` | Get unread count |
| PUT | `/api/notifications/<id>/read` | Mark as read |
| PUT | `/api/notifications/read-all` | Mark all as read |

### Messages
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/messages` | Get all conversations |
| GET | `/api/messages/<user_id>` | Get message history |
| POST | `/api/messages/<user_id>` | Send message |
| PUT | `/api/messages/<message_id>/read` | Mark message as read |
| GET | `/api/messages/unread` | Get unread message count |
| POST | `/api/messages/typing/<user_id>` | Send typing status |
| POST | `/api/messages/cleanup` | Delete messages older than 90 days |

### Search & Bookmarks
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/matches/search` | Search profiles by criteria |
| GET | `/api/matches/bookmarks` | Get bookmarked profiles |
| POST | `/api/matches/bookmark/<user_id>` | Bookmark a profile |
| DELETE | `/api/matches/bookmark/<user_id>` | Remove bookmark |

## Project Structure

```
datingApp/
├── app/
│   ├── __init__.py      # Flask app factory + SocketIO
│   ├── config.py        # Configuration
│   ├── models.py        # Database models
│   ├── forms.py         # WTForms
│   ├── views.py         # Auth & Profile endpoints
│   ├── matches.py       # Matching algorithm & endpoints
│   ├── notifications.py # Notification endpoints
│   ├── messages.py      # Messaging endpoints
│   └── bookmarks.py     # Search & bookmark endpoints
├── e2e/                  # Playwright E2E tests
│   ├── auth.spec.js
│   ├── matching.spec.js
│   ├── messaging.spec.js
│   ├── navigation.spec.js
│   ├── responsive.spec.js
│   └── helpers/
├── src/
│   ├── views/           # Vue views
│   │   ├── BrowseView.vue       # Browse/swipe profiles
│   │   ├── MatchesView.vue      # Mutual matches
│   │   ├── ConversationsView.vue # Message conversations
│   │   ├── ChatView.vue         # Chat with messages
│   │   ├── SearchView.vue       # Advanced search
│   │   ├── FavoritesView.vue    # Bookmarked profiles
│   │   ├── NotificationsView.vue
│   │   └── ...
│   ├── components/      # Vue components
│   │   ├── AppHeader.vue
│   │   ├── AppFooter.vue
│   │   └── ui/          # Base UI components
│   │       ├── BaseAvatar.vue
│   │       ├── BaseBadge.vue
│   │       ├── BaseButton.vue
│   │       └── BaseInput.vue
│   ├── services/        # API services
│   │   ├── authService.js
│   │   ├── matchService.js
│   │   ├── notificationService.js
│   │   ├── messageService.js
│   │   ├── profileService.js
│   │   ├── searchService.js
│   │   └── socketService.js
│   ├── composables/     # Vue composables
│   │   └── useAuth.js
│   ├── router/          # Vue router
│   ├── __tests__/       # Vitest unit tests
│   │   ├── components/
│   │   ├── views/
│   │   └── services/
│   └── test/            # Test utilities & mocks
│       └── mocks/
├── public/
│   └── sw.js            # Service worker for push notifications
├── tests/               # Pytest backend tests
│   ├── test_api.py      # Auth & Profile tests
│   ├── test_matching.py  # Matching tests
│   ├── test_messaging.py # Messaging tests
│   ├── test_search.py    # Search & bookmark tests
│   ├── test_profile_upload.py
│   ├── test_views_utils.py
│   ├── helpers.py        # Test fixtures
│   └── conftest.py       # Pytest fixtures
├── uploads/             # Uploaded files
├── run.py               # Flask entry point
├── start.sh             # Start both servers
├── start-backend.sh     # Start backend only
├── start-frontend.sh    # Start frontend only
├── run-tests.sh         # Run backend tests
└── playwright.config.js # Playwright configuration
```

## Matching Algorithm Details

The matching score is calculated based on:

| Criterion | Max Points | Description |
|-----------|------------|-------------|
| Age | 20 | Within user's preferred age range |
| Interests | 20 | Shared interests (+10 each, max 2) |
| Relationship Goal | 20 | Same relationship goal |
| Gender Preference | 15 | Matches user's preferred gender |

Users with a score below 50 are filtered out from potential matches.

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

## WebSocket Events

Real-time notifications via Socket.IO:

| Event | Direction | Description |
|-------|-----------|-------------|
| `connect` | Client → Server | Connect to WebSocket |
| `subscribe` | Client → Server | Subscribe to user notifications |
| `new_match` | Server → Client | Mutual match occurred |
| `new_like` | Server → Client | Someone liked you |
| `notification` | Server → Client | General notification |
| `new_message` | Server → Client | New message received |
| `user_typing` | Server → Client | User is typing |
| `message_read` | Server → Client | Message was read |

## Troubleshooting

### WebKit/Safari E2E Tests Not Running
WebKit requires system dependencies. Install them with:
```bash
sudo npx playwright install-deps
```
Or manually:
```bash
sudo apt-get install libicu74 libjpeg-turbo8 gstreamer1.0-libav
```

### Database Reset
To reset the database, delete the SQLite file:
```bash
rm instance/driftdater.db
```
Then restart the backend to recreate it.

### Mailtrap Not Receiving Emails
1. Check your `.env` file has correct credentials
2. Verify Mailtrap inbox is active
3. Check spam/junk folders

### Frontend Tests Failing
Ensure all dependencies are installed:
```bash
npm install
npm test
```

### Backend Tests Failing
Ensure Python environment is activated:
```bash
source .venv/bin/activate
pytest tests/ -v
```

## License

MIT
