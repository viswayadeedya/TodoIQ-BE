# TodoIQ Backend

A robust FastAPI backend with AI integration for intelligent task management. Features JWT authentication, CRUD operations, and AI-powered task generation and prioritization using OpenAI's GPT-4o-mini model.

**TodoIQ** - Smarter to-do app powered by AI.

## ✨ Features

### 🤖 AI-Powered Intelligence

- **Smart Task Generation**: Convert natural language into actionable subtasks
- **AI Re-prioritization**: Automatically reorder tasks based on importance and context
- **OpenAI Integration**: Powered by GPT-4o-mini model for intelligent AI responses
- **Contextual Understanding**: AI analyzes task relationships and dependencies

### 🔐 Authentication & Security

- **JWT Authentication**: Secure token-based authentication system
- **Password Hashing**: Bcrypt for secure password storage
- **User Management**: Registration and login with email validation
- **Protected Routes**: All endpoints require authentication

### 📋 Task Management

- **Full CRUD Operations**: Create, read, update, and delete tasks
- **Priority System**: 1-10 priority scale with intelligent categorization
- **Completion Tracking**: Mark tasks as complete with timestamps
- **User Isolation**: Each user sees only their own tasks

### 🚀 Performance & Scalability

- **FastAPI Framework**: High-performance async Python web framework
- **SQLAlchemy ORM**: Robust database operations with relationship mapping
- **Automatic API Documentation**: Interactive Swagger UI and ReDoc
- **CORS Support**: Cross-origin resource sharing for frontend integration

## 🏗️ Architecture

### Tech Stack

- **Framework**: FastAPI 0.104+
- **Database**: SQLite (development) / PostgreSQL (production)
- **ORM**: SQLAlchemy 2.0+
- **Authentication**: JWT with python-jose
- **Password Hashing**: Bcrypt
- **AI Integration**: OpenAI API with GPT-4o-mini
- **Validation**: Pydantic v2
- **Dependencies**: openai==1.58.1 for AI service integration

### Project Structure

```
Backend/
├── app/
│   ├── api/                 # API route handlers
│   │   ├── users.py        # Authentication endpoints
│   │   ├── todos.py        # Task management endpoints
│   │   └── ai.py           # AI service endpoints
│   ├── core/               # Core configuration
│   │   ├── config.py       # Environment configuration
│   │   └── security.py     # JWT and password utilities
│   ├── models/             # SQLAlchemy models
│   │   ├── user_model.py   # User database model
│   │   └── todo_model.py   # Todo database model
│   ├── schemas/            # Pydantic schemas
│   │   ├── user_schema.py  # User request/response schemas
│   │   ├── todo_schema.py  # Todo request/response schemas
│   │   └── ai_schema.py    # AI service schemas
│   ├── services/           # Business logic
│   │   └── ai_service.py   # OpenAI AI integration
│   ├── database/           # Database configuration
│   │   └── database.py     # SQLAlchemy setup
│   └── main.py            # FastAPI application entry point
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip or poetry
- OpenAI API key

### Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd Backend
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set environment variables**
   Create a `.env` file in the Backend directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./todos.db
```

5. **Run the application**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:

- **API**: `http://localhost:8000`
- **Interactive Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 📚 API Documentation

### Authentication Endpoints

#### POST `/users/signup`

Register a new user account.

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**

```json
{
  "id": 1,
  "email": "user@example.com"
}
```

#### POST `/users/login`

Authenticate user and get access token.

**Request Body:**

```json
{
  "username": "user@example.com",
  "password": "securepassword"
}
```

**Response:**

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### Task Management Endpoints

#### GET `/todos/`

Get all tasks for the authenticated user.

**Headers:** `Authorization: Bearer <token>`

**Response:**

```json
[
  {
    "id": 1,
    "title": "Complete project proposal",
    "description": "Write and submit the quarterly project proposal",
    "priority": 8,
    "created_at": "2024-01-15T10:30:00Z",
    "completed": false,
    "owner_id": 1
  }
]
```

#### POST `/todos/`

Create a new task.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**

```json
{
  "title": "New Task",
  "description": "Task description",
  "priority": 5,
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### PUT `/todos/{todo_id}`

Update an existing task.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**

```json
{
  "title": "Updated Task",
  "description": "Updated description",
  "priority": 7,
  "completed": true
}
```

#### DELETE `/todos/{todo_id}`

Delete a task.

**Headers:** `Authorization: Bearer <token>`

**Response:** `204 No Content`

### AI Service Endpoints

#### POST `/ai/suggest-subtasks`

Generate subtasks from a natural language description.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**

```json
{
  "title": "Plan a birthday party"
}
```

**Response:**

```json
[
  {
    "id": 1,
    "title": "Choose party venue",
    "description": "Research and book a suitable location for the birthday party",
    "priority": 8,
    "created_at": "2024-01-15T10:30:00Z",
    "completed": false,
    "owner_id": 1
  }
]
```

#### GET `/ai/re-prioritize-all`

Re-prioritize all user tasks using AI.

**Headers:** `Authorization: Bearer <token>`

**Response:**

```json
[
  {
    "id": 1,
    "title": "Updated Task",
    "description": "Task description",
    "priority": 9,
    "created_at": "2024-01-15T10:30:00Z",
    "completed": false,
    "owner_id": 1
  }
]
```

## 🔧 Configuration

### Environment Variables

| Variable                      | Description                    | Default              | Required |
| ----------------------------- | ------------------------------ | -------------------- | -------- |
| `OPENAI_API_KEY`              | OpenAI API key for AI services | -                    | Yes      |
| `SECRET_KEY`                  | JWT secret key                 | -                    | Yes      |
| `ALGORITHM`                   | JWT algorithm                  | HS256                | No       |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time          | 30                   | No       |
| `DATABASE_URL`                | Database connection string     | sqlite:///./todos.db | No       |

### Database Configuration

The application supports multiple database backends:

- **SQLite** (default): `sqlite:///./todos.db`
- **PostgreSQL**: `postgresql://user:password@localhost/dbname`
- **MySQL**: `mysql://user:password@localhost/dbname`

## 🤖 AI Integration

### OpenAI API Setup

1. **Get API Key**: Sign up at [platform.openai.com](https://platform.openai.com)
2. **Set Environment Variable**: Add your API key to `.env`
3. **Model Used**: `gpt-4o-mini` for optimal performance and cost-effectiveness
4. **AI Personality**: MindfulCoach - a calm but decisive planning expert that focuses on energy, dependencies, and momentum

### AI Features

#### Task Generation

The AI analyzes natural language input using GPT-4o-mini and generates:

- Specific, actionable subtasks (6-9 items per request)
- Appropriate priority levels (1-10) with no ties or gaps
- Detailed descriptions with specific actions
- Logical task ordering based on energy and dependencies
- ISO 8601 timestamps for proper scheduling

#### Smart Re-prioritization

The AI considers using GPT-4o-mini:

- Task importance and urgency
- Dependencies between tasks
- Energy levels and focus requirements
- Natural workflow patterns
- Momentum and burnout prevention

## 🛠️ Development

### Running in Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Database Migrations

The application uses SQLAlchemy with automatic table creation. For production:

```bash
# Create tables
python -c "from app.database.database import engine; from app.models import user_model, todo_model; user_model.Base.metadata.create_all(bind=engine); todo_model.Base.metadata.create_all(bind=engine)"
```

### Testing

```bash
# Run tests (if implemented)
pytest

# Run with coverage
pytest --cov=app
```

## 🔒 Security Features

### Authentication

- **JWT Tokens**: Secure, stateless authentication
- **Password Hashing**: Bcrypt with salt rounds
- **Token Expiration**: Configurable token lifetime
- **Protected Routes**: All endpoints require valid tokens

### Data Protection

- **Input Validation**: Pydantic schemas for all inputs
- **SQL Injection Prevention**: SQLAlchemy ORM protection
- **CORS Configuration**: Controlled cross-origin access
- **Error Handling**: Secure error messages without data leaks

## 📊 Performance

### Optimization Features

- **Async/Await**: Non-blocking I/O operations
- **Connection Pooling**: Efficient database connections
- **Response Caching**: Optional caching for AI responses
- **Compression**: Automatic response compression

### Monitoring

- **Health Checks**: `/health` endpoint for monitoring
- **Request Logging**: Detailed request/response logging
- **Error Tracking**: Comprehensive error logging
- **Performance Metrics**: Built-in FastAPI metrics

## 🚀 Deployment

### Production Setup

1. **Environment Configuration**

```bash
export OPENAI_API_KEY=your_production_key
export SECRET_KEY=your_secure_secret_key
export DATABASE_URL=postgresql://user:pass@host:port/db
```

2. **Install Production Dependencies**

```bash
pip install -r requirements.txt
```

3. **Run with Gunicorn**

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Cloud Deployment

- **AWS**: ECS, Lambda, or EC2
- **Google Cloud**: Cloud Run or Compute Engine
- **Azure**: Container Instances or App Service
- **Heroku**: Direct deployment with Procfile

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Getting Help

- **Documentation**: Check the API docs at `/docs`
- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions

### Common Issues

**Database Connection Error**

- Check DATABASE_URL format
- Ensure database server is running
- Verify credentials

**AI Service Error**

- Verify OPENAI_API_KEY is set
- Check API key validity
- Monitor rate limits and usage

**Authentication Error**

- Verify JWT token format
- Check token expiration
- Ensure proper headers

---

Built with ❤️ using FastAPI, Python, and AI technologies.
