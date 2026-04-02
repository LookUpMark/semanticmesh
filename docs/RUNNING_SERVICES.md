# Running the Thesis Project - Services & Setup Guide

This guide explains how to set up and run the background services required for the Multi-Agent Framework for Semantic Discovery & GraphRAG.

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Neo4j Database Setup](#neo4j-database-setup)
3. [Environment Configuration](#environment-configuration)
4. [Running the Application](#running-the-application)
5. [Interactive Demo Notebook](#interactive-demo-notebook)
6. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

The fastest way to get started:

```bash
# 1. Start Neo4j with Docker
docker run -d --name neo4j-thesis \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/test_password \
  neo4j:5

# 2. Configure environment
cp .env.example .env
# Edit .env with your OPENROUTER_API_KEY

# 3. Install dependencies
pip install -e ".[dev]"

# 4. Run the interactive demo
jupyter notebook notebooks/00_interactive_demo.ipynb
```

---

## 🗄️ Neo4j Database Setup

### Why Neo4j?

The Multi-Agent Framework uses Neo4j as its knowledge graph storage because:
- **Native graph database** - Optimized for traversing relationships
- **Cypher query language** - Powerful, SQL-like language for graphs
- **Vector indexing** - Supports hybrid vector + graph queries

### Option 1: Docker (Recommended)

#### Start a new Neo4j container:

```bash
docker run -d \
  --name neo4j-thesis \
  -p 7474:7474 \
  -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/your_password_here \
  -v neo4j-data:/data \
  neo4j:5
```

**What this does:**
- `-d` - Run in detached mode (background)
- `--name neo4j-thesis` - Name the container for easy management
- `-p 7474:7474` - Expose Neo4j Browser (web UI) on port 7474
- `-p 7687:7687` - Expose Bolt protocol (database connection) on port 7687
- `-e NEO4J_AUTH` - Set username/password
- `-v neo4j-data:/data` - Persist data in a named volume

#### Neo4j Browser UI:

Once running, access the Neo4j Browser at:
- **URL:** http://localhost:7474
- **Username:** `neo4j`
- **Password:** `your_password_here`

#### Docker Management Commands:

```bash
# Check if Neo4j is running
docker ps | grep neo4j-thesis

# View Neo4j logs
docker logs neo4j-thesis

# Stop Neo4j
docker stop neo4j-thesis

# Start Neo4j (stopped container)
docker start neo4j-thesis

# Remove Neo4j container (WARNING: deletes data)
docker rm -f neo4j-thesis
```

### Option 2: Neo4j Desktop

1. Download [Neo4j Desktop](https://neo4j.com/download/)
2. Install and open Neo4j Desktop
3. Create a new project
4. Add a local database (version 5.x)
5. Set username: `neo4j` and your chosen password
6. Start the database
7. Note the Bolt URL (usually `bolt://localhost:7687`)

### Option 3: Neo4j AuraDB (Cloud - Free Tier)

1. Visit [Neo4j Aura](https://neo4j.com/cloud-platform/aura-free/)
2. Create a free account
3. Create a new AuraDB Free instance
4. Copy the connection string (Bolt URI)
5. Use the AuraDB credentials in your `.env` file

---

## 🔧 Environment Configuration

### Create `.env` File

Copy the example environment file and add your credentials:

```bash
cp .env.example .env
```

### Edit `.env` with your values:

```bash
# ── Neo4j Connection ────────────────────────────────────────────────
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password_here

# ── LLM API Key (OpenRouter) ────────────────────────────────────────
# Get your free API key at: https://openrouter.ai/keys
OPENROUTER_API_KEY=sk-or-your-key-here
```

### Optional: Override Default Configuration

You can override any default setting from `src/config/config.py`:

```bash
# Use different LLM models
LLM_MODEL_REASONING=openai/gpt-4o
LLM_MODEL_EXTRACTION=openai/gpt-4o-mini

# Adjust retrieval settings
RETRIEVAL_VECTOR_TOP_K=30
RETRIEVAL_BM25_TOP_K=15

# Disable specific components (for ablation testing)
ENABLE_CYPHER_HEALING=false
ENABLE_HALLUCINATION_GRADER=false
```

---

## ▶️ Running the Application

### Python Environment Setup

```bash
# Create virtual environment (if not exists)
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Linux/Mac
# OR
.venv\Scripts\activate     # On Windows

# Install with development dependencies
pip install -e ".[dev]"
```

### Verify Installation

```bash
# Check Python version (requires 3.11+)
python --version

# Check installed packages
pip list | grep -E "langgraph|neo4j|pydantic"

# Run unit tests to verify
pytest tests/unit/ -v
```

---

## 📓 Interactive Demo Notebook

The **Interactive Demo Notebook** (`notebooks/00_interactive_demo.ipynb`) provides a hands-on way to explore the entire pipeline.

### Start Jupyter:

```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Start Jupyter Lab (recommended) or Notebook
jupyter lab notebooks/

# OR
jupyter notebook notebooks/
```

### What the Demo Notebook Includes:

1. **📋 Configuration Cell** - Modify all settings at the top
2. **🔍 Service Check** - Verify Neo4j connection and API keys
3. **📁 Data Loading** - Load your PDF and DDL files
4. **🏗️ Builder Graph** - Step-by-step knowledge graph construction
5. **🔎 Graph Inspection** - Query and visualize the knowledge graph
6. **❓ Query Graph** - Ask questions and see RAG in action
7. **📊 Batch Queries** - Test multiple questions at once
8. **🧹 Cleanup** - Reset the graph if needed

---

## 🧪 Running Tests

### Unit Tests (No Neo4j required)

```bash
# Run all unit tests
pytest tests/unit/ -v

# Run specific test file
pytest tests/unit/test_settings.py -v

# Run with coverage
pytest tests/unit/ --cov=src --cov-report=html
```

### Integration Tests (Neo4j required)

```bash
# Run integration tests (Neo4j must be running)
pytest tests/integration/ -v -m integration

# Run all tests
pytest tests/ -v
```

---

## 🔍 Troubleshooting

### Neo4j Connection Issues

**Problem:** `ServiceUnavailable: Unable to connect to bolt://localhost:7687`

**Solutions:**
1. Verify Neo4j is running: `docker ps | grep neo4j`
2. Check Neo4j logs: `docker logs neo4j-thesis`
3. Verify port 7687 is not in use: `lsof -i :7687`
4. Ensure NEO4J_URI matches your setup

### LLM API Issues

**Problem:** `AuthenticationError: Invalid API key`

**Solutions:**
1. Verify `.env` file exists
2. Check `OPENROUTER_API_KEY` is set correctly
3. Ensure no extra spaces in the API key
4. Test API key with curl:
   ```bash
   curl -X POST https://openrouter.ai/api/v1/chat/completions \
     -H "Authorization: Bearer $OPENROUTER_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"model": "openai/gpt-3.5-turbo", "messages": [{"role": "user", "content": "Hello"}]}'
   ```

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'src'`

**Solutions:**
1. Ensure you installed the package in editable mode:
   ```bash
   pip install -e .
   ```
2. Verify you're in the project root directory
3. Check Python path includes the project directory

### Docker Issues

**Problem:** `docker.errors.DockerException: Error while fetching server API version`

**Solutions:**
1. Verify Docker is installed: `docker --version`
2. Start Docker Desktop (on Windows/Mac)
3. Check Docker service is running: `sudo systemctl status docker` (Linux)
4. Add your user to docker group (Linux):
   ```bash
   sudo usermod -aG docker $USER
   # Log out and back in for changes to take effect
   ```

### Memory Issues

**Problem:** Out of memory errors during graph construction

**Solutions:**
1. Reduce batch size in settings
2. Process smaller documents
3. Increase Docker memory limit (Docker Desktop → Settings → Resources → Memory)
4. Use smaller LLM models

---

## 📚 Additional Resources

- **Project README:** [`README.md`](../README.md)
- **Implementation Tasks:** [`docs/implementation/TASK.md`](TASK.md)
- **Test Plan:** [`docs/draft/TEST_PLAN.md`](TEST_PLAN.md)
- **API Documentation:** Check docstrings in source files
- **LangGraph Documentation:** https://langchain-ai.github.io/langgraph/
- **Neo4j Documentation:** https://neo4j.com/docs/

---

## 🆘 Getting Help

If you encounter issues not covered here:

1. Check the [GitHub Issues](https://github.com/your-repo/issues)
2. Review the test files in `tests/unit/` for usage examples
3. Enable debug logging in `.env`:
   ```bash
   LOG_LEVEL=DEBUG
   ```
4. Check the logs for detailed error messages

---

**Last updated:** March 2026
