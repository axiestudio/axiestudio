<!-- markdownlint-disable MD030 -->
<!-- Database Fix Deployment Trigger - 2025-08-21 -->

![Axie Studio logo](https://scontent-arn2-1.xx.fbcdn.net/v/t39.30808-6/499498872_122132145854766980_5268724011023190696_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=6ee11a&_nc_ohc=xLVYhlEYae4Q7kNvwHtfkHd&_nc_oc=AdnJqlOOFeYRaGihnOCTDh7BqhomO70C4ohACN7i21RGp7WtWOUoaBYAWaAmv9Vl4R4&_nc_zt=23&_nc_ht=scontent-arn2-1.xx&_nc_gid=CjUMK_SK11uYLtn5b4hAyA&oh=00_AfUgO7heIBkN7WFcOFkMJNEfUGhjbDv5rfiuXoH7vwQz_g&oe=68AD4019)


[![Release Notes](https://img.shields.io/github/release/axiestudio/axiestudio?style=flat-square)](https://github.com/axiestudio/axiestudio/releases)
[![PyPI - License](https://img.shields.io/badge/license-MIT%20(Open%20Source)-green)](https://opensource.org/licenses/MIT)
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
- **Integrated Store** with one-click flow import and modern search functionality.
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

## 🏪 Component & Flow Showcase

AxieStudio features a comprehensive showcase with **1,600 professional components and flows** ready for immediate use:

### ✨ Showcase Features

- **📊 1,600 Items** - Complete collection of 1,172 flows and 428 components
- **🔍 Advanced Search** - Real-time search across names, descriptions, authors, and tags
- **🎯 Smart Filtering** - Filter by type (flows/components), categories, and popularity
- **📱 Modern Interface** - Beautiful, responsive design with grid layout and pagination
- **⚡ Instant Download** - Download components as JSON files for immediate use
- **🔗 Easy Access** - Available via Library button in flow toolbar and Settings page
- **🎨 Preview Mode** - View component details before downloading

### 🛠️ How to Use the Showcase

1. **Access via Toolbar** - Click the Library icon (📚) in any flow page toolbar
2. **Browse Collection** - Explore all 1,600 components and flows with pagination
3. **Search & Filter** - Use advanced search and filtering to find exactly what you need
4. **Preview Items** - Click on any item to see detailed information
5. **Download** - Get JSON files for immediate import into your projects
6. **Settings Access** - Also available through Settings → Component Showcase

### 🎯 Showcase Configuration

The showcase is enabled by default and includes all store data. To customize:

```bash
# Enable/disable showcase features
ENABLE_AXIESTUDIO_STORE="true"  # Controls showcase availability
```

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

## 🗄️ Enhanced Database Management System

AxieStudio features an **enterprise-grade automatic database management system** with intelligent table creation, migration handling, and comprehensive monitoring.

### 🚀 **Automatic Table Creation**

The system automatically creates and manages all database tables on startup:

```bash
# Enhanced CLI Database Administration Tool
python database_admin.py status          # Show comprehensive database status
python database_admin.py create-tables   # Create missing tables automatically
python database_admin.py migrate         # Run database migration
python database_admin.py health          # Perform health check
python database_admin.py list-tables     # List all tables with details
python database_admin.py help            # Show help information
```

### 🔧 **Database API Endpoints (Admin Only)**

```bash
# Comprehensive database management API
GET    /api/v1/database/status           # Detailed database status & table info
GET    /api/v1/database/tables           # List all tables with column details
GET    /api/v1/database/migration-status # Current migration version info
POST   /api/v1/database/create-tables    # Create missing tables automatically
POST   /api/v1/database/migrate          # Run full Alembic migration
GET    /api/v1/database/health           # Comprehensive health check
```

### 📊 **Auto-Created Database Tables**

The system automatically creates and maintains these core tables:
- **user** - User accounts, authentication, and profiles
- **flow** - AI workflow definitions and configurations
- **folder** - Project organization and hierarchy
- **apikey** - API key management and authentication
- **variable** - Global variables and environment settings
- **file** - File attachments and document storage
- **message** - Chat messages and conversation history
- **transaction** - Subscription and billing transactions
- **vertex_build** - Build information and deployment logs
- **alembic_version** - Database migration version tracking

### ✨ **Advanced Features**

- 🔄 **Intelligent Startup** - Automatically detects and creates missing tables
- 📈 **Progress Tracking** - Real-time progress indicators with emoji status
- 🛡️ **Error Recovery** - Robust error handling with detailed logging
- 🔍 **Health Monitoring** - Comprehensive database health checks
- 📋 **Rich CLI Interface** - Beautiful command-line tools with tables and panels
- 🔒 **Security Columns** - Automatic addition of enhanced security fields
- 📊 **Detailed Reporting** - Table counts, row counts, and status information
- 🎯 **Production Ready** - Enterprise-grade reliability and monitoring

### 🔧 Production Environment Configuration

For production deployments, use these environment variables:

```bash
# 🗄️ DATABASE CONFIGURATION
AXIESTUDIO_DATABASE_URL="postgresql://your_username:your_password@your-db-host:5432/your_database?sslmode=require"

# 🔐 AUTHENTICATION CONFIGURATION
AXIESTUDIO_SUPERUSER="admin@yourdomain.com"
AXIESTUDIO_SUPERUSER_PASSWORD="your_secure_password"
AXIESTUDIO_AUTO_LOGIN="false"
AXIESTUDIO_NEW_USER_IS_ACTIVE="false"  # Users must verify email to activate

# 🔒 SECURITY CONFIGURATION
AXIESTUDIO_SECRET_KEY="your-production-secret-key-change-this-in-production"

# 🌐 SERVER CONFIGURATION
AXIESTUDIO_HOST="0.0.0.0"
AXIESTUDIO_PORT="7860"
PORT="7860"

# 📊 PERFORMANCE & LOGGING
AXIESTUDIO_LOG_LEVEL="INFO"
AXIESTUDIO_WORKERS="1"

# 💾 CACHE & STORAGE
AXIESTUDIO_CACHE_TYPE="memory"

# 🏪 STORE CONFIGURATION
ENABLE_AXIESTUDIO_STORE="true"

# � EMAIL VERIFICATION CONFIGURATION
# Set to "false" to require email verification before users can login
# Users will receive activation email and must click link to activate account
AXIESTUDIO_NEW_USER_IS_ACTIVE="false"

# �💳 STRIPE CONFIGURATION (Optional - for subscription features)
STRIPE_PRICE_ID="your_stripe_price_id_here"
STRIPE_PUBLISHABLE_KEY="your_stripe_publishable_key_here"
STRIPE_SECRET_KEY="your_stripe_secret_key_here"
STRIPE_WEBHOOK_SECRET="your_stripe_webhook_secret_here"

# 📈 MONITORING
DO_NOT_TRACK="1"
```

## 🗄️ Database Migration for Subscription Features

If you're using PostgreSQL and encounter migration errors related to subscription columns, run these SQL commands in your database console:

### 📋 Step-by-Step Migration Commands

Copy and paste each command **one by one** into your PostgreSQL console:

#### 1. Add Email Column
```sql
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS email VARCHAR;
```

#### 2. Add Stripe Customer ID
```sql
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS stripe_customer_id VARCHAR;
```

#### 3. Add Subscription Status (with default)
```sql
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS subscription_status VARCHAR DEFAULT 'trial';
```

#### 4. Add Subscription ID
```sql
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS subscription_id VARCHAR;
```

#### 5. Add Trial Start Date
```sql
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS trial_start TIMESTAMP;
```

#### 6. Add Trial End Date
```sql
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS trial_end TIMESTAMP;
```

#### 7. Add Subscription Start Date
```sql
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS subscription_start TIMESTAMP;
```

#### 8. Add Subscription End Date
```sql
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS subscription_end TIMESTAMP;
```

#### 9. Create Email Index for Performance
```sql
CREATE INDEX IF NOT EXISTS ix_user_email ON "user" (email);
```

#### 10. Update Existing Users with Trial Status
```sql
UPDATE "user"
SET subscription_status = 'trial',
    trial_start = NOW()
WHERE subscription_status IS NULL;
```

#### 11. Add Email Verification Column (Required for Email Verification)
```sql
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT false;
```

#### 12. Add Active Status Column (Required for User Activation)
```sql
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS active BOOLEAN DEFAULT true;
```

#### 13. Set Default Email Verified Status for Existing Users
```sql
UPDATE "user"
SET email_verified = false
WHERE email_verified IS NULL;
```

#### 14. Set Default Active Status for Existing Users
```sql
UPDATE "user"
SET active = true
WHERE active IS NULL;
```

#### 15. Create Email Verification Index for Performance
```sql
CREATE INDEX IF NOT EXISTS ix_user_email_verified ON "user" (email_verified);
```

#### 16. Create Active Status Index for Performance
```sql
CREATE INDEX IF NOT EXISTS ix_user_active ON "user" (active);
```

#### 17. Verify Email Verification Setup
```sql
SELECT email, email_verified, active
FROM "user"
LIMIT 5;
```

#### 18. Verify Migration Success
```sql
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'user' AND table_schema = 'public'
ORDER BY ordinal_position;
```

### 🎯 Migration Notes

- ✅ **Safe to run multiple times** - Uses `IF NOT EXISTS` clauses
- ✅ **No data loss** - Only adds columns, doesn't modify existing data
- ✅ **Works with any PostgreSQL** - Neon, Supabase, DigitalOcean, etc.
- ✅ **Required for subscription features** - Enables Stripe integration
- ✅ **Required for email verification** - Enables secure user activation
- ✅ **Performance optimized** - Includes indexes for fast queries

> **💡 Tip:** If you're using Neon, Supabase, or another cloud PostgreSQL service, run these commands in their web console SQL editor.

> **⚠️ Important:** Commands 11-17 are required for email verification functionality. Run them if you're implementing user email verification.

### 🔐 Production Features

- ✅ **Enterprise Database Support** (PostgreSQL, SQLite)
- ✅ **Secure Authentication** (Login required, email verification)
- ✅ **Production Security** (JWT tokens, secret keys)
- ✅ **Integrated Store** (Community flows and components)
- ✅ **Email Verification** (Secure user activation)
- ✅ **Subscription Management** (Stripe integration)
- ✅ **Optimized Performance** (Memory caching, configurable workers)

> **⚠️ Security Note:** Replace placeholder values with your actual production credentials. Keep sensitive data in environment variables, not in repositories.

## 📚 Documentation

- [Installation Guide](https://docs.axiestudio.org/get-started-installation)
- [Quickstart Tutorial](https://docs.axiestudio.org/get-started-quickstart)
- [Component Documentation](https://docs.axiestudio.org/components)
- [API Reference](https://docs.axiestudio.org/api-reference)

## 🤝 Contributing

Axie Studio is a fork of [Langflow](https://github.com/langflow-ai/langflow) with enhanced features for production use.

We welcome contributions! Please see our [Contributing Guide](./CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License (Open Source) - see the [LICENSE](./LICENSE) file for details.

## 🔒 Security

For security concerns, please see our [Security Policy](./SECURITY.md).

---

**Built with ❤️ by the Axie Studio team**

<!-- Force rebuild: 2025-08-19 -->
