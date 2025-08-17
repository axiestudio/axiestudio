<!-- markdownlint-disable MD030 -->

![Axie Studio logo](./docs/static/img/axiestudio-logo-color-black-solid.svg)


[![Release Notes](https://img.shields.io/github/release/axiestudio/axiestudio?style=flat-square)](https://github.com/axiestudio/axiestudio/releases)
[![PyPI - License](https://img.shields.io/badge/license-MIT-orange)](https://opensource.org/licenses/MIT)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/axiestudio?style=flat-square)](https://pypistats.org/packages/axiestudio)
[![GitHub star chart](https://img.shields.io/github/stars/axiestudio/axiestudio?style=flat-square)](https://star-history.com/#axiestudio/axiestudio)
[![Open Issues](https://img.shields.io/github/issues-raw/axiestudio/axiestudio?style=flat-square)](https://github.com/axiestudio/axiestudio/issues)
[![Docker Hub](https://img.shields.io/docker/pulls/axiestudio/axiestudio?style=flat-square)](https://hub.docker.com/r/axiestudio/axiestudio)

[Axie Studio](https://axiestudio.org) is a powerful tool for building and deploying AI-powered agents and workflows. It provides developers with both a visual authoring experience and built-in API and MCP servers that turn every workflow into a tool that can be integrated into applications built on any framework or stack. Axie Studio comes with batteries included and supports all major LLMs, vector databases and a growing library of AI tools.

## ✨ Highlight features

- **Visual builder interface** to quickly get started and iterate.
- **Source code access** lets you customize any component using Python.
- **Interactive playground** to immediately test and refine your flows with step-by-step control.
- **Multi-agent orchestration** with conversation management and retrieval.
- **Deploy as an API** or export as JSON for Python apps.
- **Deploy as an MCP server** and turn your flows into tools for MCP clients.
- **Observability** with LangSmith, LangFuse and other integrations.
- **Enterprise-ready** security and scalability.

## ⚡️ Quickstart

Axie Studio requires [Python 3.10 to 3.13](https://www.python.org/downloads/release/python-3100/) and [uv](https://docs.astral.sh/uv/getting-started/installation/).

1. To install Axie Studio, run:

```shell
uv pip install axiestudio -U
```

2. To run Axie Studio, run:

```shell
uv run axiestudio run
```

3. Go to the default Axie Studio URL at `http://127.0.0.1:7860`.

For more information about installing Axie Studio, including Docker and Desktop options, see [Install Axie Studio](https://docs.axiestudio.org/get-started-installation).

## 🐳 Docker

You can run Axie Studio using Docker:

```shell
docker run -it --rm -p 7860:7860 axiestudio/axiestudio:latest
```

## 🚀 Deploy

Deploy Axie Studio on your preferred cloud platform:

- [DigitalOcean App Platform](./DEPLOYMENT.md)
- [Railway](./RAILWAY_ENV.md)
- [Docker Hub](https://hub.docker.com/r/axiestudio/axiestudio)

### 🔧 Production Environment Configuration

For production deployments, use these environment variables:

```bash
# 🗄️ DATABASE CONFIGURATION
AXIESTUDIO_DATABASE_URL=postgresql://username:password@your-db-host:25060/database?sslmode=require

# 🔐 AUTHENTICATION CONFIGURATION
AXIESTUDIO_SUPERUSER=admin@yourdomain.com
AXIESTUDIO_SUPERUSER_PASSWORD=your_secure_password
AXIESTUDIO_AUTO_LOGIN=false
AXIESTUDIO_NEW_USER_IS_ACTIVE=false

# 🔒 SECURITY CONFIGURATION
AXIESTUDIO_SECRET_KEY=your-production-secret-key-here
AXIESTUDIO_JWT_SECRET=your-jwt-secret-here

# 🌐 SERVER CONFIGURATION
AXIESTUDIO_HOST=0.0.0.0
AXIESTUDIO_PORT=7860
PORT=7860

# 📊 PERFORMANCE & LOGGING
AXIESTUDIO_LOG_LEVEL=INFO
AXIESTUDIO_DEBUG=false
AXIESTUDIO_WORKERS=1

# 💾 CACHE & STORAGE
AXIESTUDIO_CACHE_TYPE=memory
AXIESTUDIO_STORE=false

# 🔧 APPLICATION SETTINGS
AXIESTUDIO_SAVE_DB_IN_CONFIG_DIR=false
AXIESTUDIO_STORE_ENVIRONMENT_VARIABLES=true
AXIESTUDIO_FALLBACK_TO_ENV_VAR=true
AXIESTUDIO_AUTO_SAVING=true

# 📈 MONITORING
DO_NOT_TRACK=1
AXIESTUDIO_OPEN_BROWSER=false
```

### 🔐 Production Features

- ✅ **Enterprise Database Support** (PostgreSQL, SQLite)
- ✅ **Secure Authentication** (Login required, admin approval)
- ✅ **Production Security** (JWT tokens, secret keys)
- ✅ **Store Disabled** (No external dependencies)
- ✅ **Optimized Performance** (Memory caching, configurable workers)

> **⚠️ Security Note:** Replace placeholder values with your actual production credentials. Keep sensitive data in environment variables, not in repositories.

## 📚 Documentation

- [Installation Guide](https://docs.axiestudio.org/get-started-installation)
- [Quickstart Tutorial](https://docs.axiestudio.org/get-started-quickstart)
- [Component Documentation](https://docs.axiestudio.org/components)
- [API Reference](https://docs.axiestudio.org/api-reference)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](./CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## 🔒 Security

For security concerns, please see our [Security Policy](./SECURITY.md).

---

**Built with ❤️ by the Axie Studio team**
