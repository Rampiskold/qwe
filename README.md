# SGR Agent Core - Tool Search Context Compression

Advanced LLM agent framework with SQL analytics, web research, and schema-guided reasoning capabilities.

## 🎯 Overview

This project contains:
1. **SGR Agent Core** - LLM agent framework with tool calling and reasoning
2. **SQL Database Agent** - Natural language to SQL analytics agent
3. **PostgreSQL API** - FastAPI backend for database access
4. **Research Agent** - Web search and content extraction agent

## 📁 Project Structure

```
sgr-agetn-core-tool-search-context-compression/
│
└── sgr-agent-core/                     # Main agent framework
    ├── sgr_agent_core/                 # Core agent implementation
    │   ├── agents/                     # Agent implementations
    │   ├── tools/                      # Agent tools
    │   │   └── sql_agent/             # SQL agent tools
    │   ├── prompts/                    # System prompts
    │   └── services/                   # Agent services
    │
    ├── postgres-adminer-setup/         # PostgreSQL + API setup
    │   ├── api/                        # FastAPI implementation
    │   │   ├── main.py                 # API endpoints
    │   │   ├── database.py             # Database operations
    │   │   └── config.py               # Configuration
    │   │
    │   ├── docker-compose.yml          # Docker setup
    │   ├── init_db.sql                 # Database schema
    │   └── requirements.txt            # Python dependencies
    │
    ├── agent_visualizer/               # Streamlit visualizer
    ├── agents.yaml                     # Agent configurations
    ├── config.yaml                     # Global config
    └── run_agent.py                    # Agent runner
```

## 🚀 Quick Start

### 1. Start PostgreSQL and API

```bash
cd sgr-agent-core/postgres-adminer-setup
docker compose up -d
```

Services:
- PostgreSQL: `localhost:18788`
- Adminer: `http://localhost:18789`
- FastAPI: `http://localhost:18790`

### 2. Setup Python Environment

```bash
cd sgr-agent-core
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

### 3. Run SQL Agent

```bash
cd sgr-agent-core
uv run python run_agent.py sql_database_agent "Show me all tables in the database"
```

### 4. Run Agent Visualizer

```bash
cd sgr-agent-core/agent_visualizer
streamlit run app.py --server.port 12139
```

## 🤖 Available Agents

### 1. SQL Database Agent

**Purpose**: Analyze PostgreSQL databases using natural language

**Example queries**:
```bash
# Simple exploration
uv run python run_agent.py sql_database_agent "What tables are in the database?"

# Analytics
uv run python run_agent.py sql_database_agent "Which tribe has the highest budget?"

# Complex analysis
uv run python run_agent.py sql_database_agent "Compare October vs September OPEX spending"
```

**Tools**:
- `SQLDatabaseGetTablesTool` - List database tables
- `SQLTableGetSchemaTool` - Get table schema
- `SQLDatabaseExecuteQueryTool` - Execute SQL queries
- `WebSearchTool` - Search PostgreSQL documentation
- `ExtractPageContentTool` - Extract documentation content

### 2. Russian Deep Research Agent

**Purpose**: Deep web research with Russian language support

**Example queries**:
```bash
uv run python run_agent.py russian_deep_research_agent "Кто победил на Олимпиаде 2024 в плавании?"
```

**Tools**:
- `WebSearchTool` - Web search
- `ExtractPageContentTool` - Extract page content
- `ReasoningTool` - Reasoning and planning
- `FinalAnswerTool` - Generate final answer

## 📊 PostgreSQL API

### Endpoints

#### GET `/api/tables`
Get database tables with pagination and comments

```bash
curl "http://localhost:18790/api/tables?page=1&page_size=10"
```

#### GET `/api/tables/{table_name}/schema`
Get detailed table schema with column types and comments

```bash
curl "http://localhost:18790/api/tables/budget_actuals/schema"
```

#### POST `/api/query`
Execute SQL SELECT query (JSON response)

```bash
curl -X POST "http://localhost:18790/api/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT * FROM dict_currencies LIMIT 5"}'
```

#### POST `/api/query/markdown`
Execute SQL SELECT query (Markdown response)

```bash
curl -X POST "http://localhost:18790/api/query/markdown" \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT * FROM dict_currencies LIMIT 5"}'
```

### API Documentation

- **Swagger UI**: `http://localhost:18790/docs`
- **ReDoc**: `http://localhost:18790/redoc`

## 🔧 Configuration

### Agent Configuration (`sgr-agent-core/agents.yaml`)

```yaml
sql_database_agent:
  llm:
    model: "qwen3-30b-a3b-instruct-2507"  # or "gpt-4", "claude-3-opus"
    temperature: 0.2
    max_tokens: 8000
  
  tools:
    - SQLDatabaseGetTablesTool
    - SQLTableGetSchemaTool
    - SQLDatabaseExecuteQueryTool
    - WebSearchTool
    - ExtractPageContentTool
    - FinalAnswerTool
    - ReasoningTool
```

### Database Configuration (`postgres-adminer-setup/api/.env`)

```env
DATABASE_HOST=postgres
DATABASE_PORT=18788
DATABASE_NAME=sgr_memory_vault
DATABASE_USER=admin
DATABASE_PASSWORD=Lol770905!
```

## 🛠️ Development

### Hot Reload

API code is mounted as volume - changes apply automatically:

```bash
# Edit files in postgres-adminer-setup/api/
vim postgres-adminer-setup/api/main.py
# Changes apply in 2-3 seconds, no restart needed
```

### Run Tests

```bash
# Test API
cd postgres-adminer-setup
bash test_api.sh

# Test SQL queries
bash test_sql_query.sh
```

### View Logs

```bash
# API logs
docker compose -f postgres-adminer-setup/docker-compose.yml logs -f api

# Agent logs
ls sgr-agent-core/logs/
```

## 📚 Documentation

- **SQL Agent Guide**: `sgr-agent-core/SQL_AGENT_GUIDE.md`
- **Setup Complete**: `sgr-agent-core/SQL_AGENT_SETUP_COMPLETE.md`
- **API Documentation**: `postgres-adminer-setup/API_README.md`
- **SQL Examples**: `postgres-adminer-setup/SQL_QUERY_EXAMPLES.md`
- **Tools README**: `sgr-agent-core/sgr_agent_core/tools/sql_agent/README.md`

## 🔒 Security

- ✅ **Read-only database access** - Only SELECT queries allowed
- ✅ **SQL injection protection** - Parameterized queries
- ✅ **Input validation** - Query validation before execution
- ✅ **Forbidden operations** - INSERT/UPDATE/DELETE/DROP blocked

## 🐳 Docker

### Start Services

```bash
cd postgres-adminer-setup
docker compose up -d
```

### Stop Services

```bash
docker compose down
```

### View Running Containers

```bash
docker compose ps
```

### Rebuild API

```bash
docker compose build api
docker compose up -d api
```

## 💻 System Requirements

- **Python**: 3.12+
- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Memory**: 4GB+ recommended
- **Disk**: 2GB+ free space

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 Example Use Cases

### Business Analytics

```bash
# Budget analysis
uv run python run_agent.py sql_database_agent "What's the budget execution rate by CFO for October 2025?"

# Trend analysis
uv run python run_agent.py sql_database_agent "Compare OPEX spending: October vs September"

# Cross-analysis
uv run python run_agent.py sql_database_agent "Which tribes have highest budget execution % in Q3?"
```

### Data Exploration

```bash
# Discover structure
uv run python run_agent.py sql_database_agent "Describe the database structure"

# Find relationships
uv run python run_agent.py sql_database_agent "How are tables related to each other?"

# Check data quality
uv run python run_agent.py sql_database_agent "Find any anomalies in budget data"
```

### Research Tasks

```bash
# Web research
uv run python run_agent.py russian_deep_research_agent "Последние новости по искусственному интеллекту"

# Technical documentation
uv run python run_agent.py sql_database_agent "How to use window functions in PostgreSQL for running totals?"
```

## 🎓 Architecture

### Agent Framework

- **Schema-Guided Reasoning** - Structured thinking process
- **Tool Calling** - Dynamic tool selection and execution
- **Context Management** - Efficient context window usage
- **Error Recovery** - Automatic error handling and retry

### SQL Agent Workflow

```
User Question
    ↓
ReasoningTool (plan approach)
    ↓
SQLDatabaseGetTablesTool (discover tables)
    ↓
SQLTableGetSchemaTool (understand structure)
    ↓
SQLDatabaseExecuteQueryTool (execute query)
    ↓
Analyze results
    ↓
FinalAnswerTool (provide insights)
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- PostgreSQL for robust database
- Anthropic Claude, OpenAI GPT, and Alibaba Qwen for LLM capabilities
- All contributors and users

## 📧 Support

For questions and issues:
- Open an issue on GitHub
- Check documentation in `docs/` folder
- Review examples in `examples/` folder

---

**Made with ❤️ for data analysts, researchers, and AI enthusiasts**
