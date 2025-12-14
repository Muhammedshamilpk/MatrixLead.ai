# MatrixLead.ai

**AI-Powered Lead Qualification & Automated Sales Engagement System**

MatrixLead.ai is an intelligent lead management system that automatically qualifies leads using multi-factor analysis and sends personalized emails to qualified prospects.

## 🚀 Recent Improvements (December 2025)

### ✅ Enhanced Lead Qualification
- **Multi-factor scoring** with 10+ dimensions (industry, company size, buying intent, urgency)
- **6 qualification tiers** (HOT, QUALIFIED, WARM, NURTURE, REVIEW, NOT_QUALIFIED)
- **Intelligent risk assessment** with differentiated penalties
- **Combination bonuses** for high-quality signal patterns

### ✅ Automatic Email Sending
- **Real SMTP integration** (Gmail, Outlook, SendGrid, Amazon SES)
- **Professional HTML templates** with personalized content
- **Automatic sending** for HOT, QUALIFIED, and WARM leads
- **Tier-based customization** (urgency, messaging, call-to-action)

**📖 See [IMPROVEMENTS_SUMMARY.md](IMPROVEMENTS_SUMMARY.md) for quick overview**  
**📚 See [IMPROVEMENTS.md](IMPROVEMENTS.md) for detailed documentation**

## 🎯 Features

- **Multi-Tool Lead Analysis**: Email validation, phone verification, company enrichment, intent detection
- **AI-Powered Scoring**: Weighted scoring with industry and intent bonuses
- **Automatic Email Outreach**: Personalized emails sent to qualified leads
- **Risk Detection**: Identifies disposable emails, fake companies, spam patterns
- **Confidence Scoring**: Measures data quality and completeness
- **Dashboard UI**: Modern interface for lead management

## 🏗️ Architecture

```
Frontend (React) → Backend (FastAPI) → Agents (Qualification) → MCP Tools
                                              ↓
                                        Email Service (SMTP)
```

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone <repository-url>
cd MatrixNew
```

### 2. Configure Email Service
```bash
python setup_email.py
# Follow the interactive prompts
```

### 3. Start Services
```bash
docker-compose up -d
```

### 4. Test the System
```bash
python test_flow.py
```

## 📊 Qualification Tiers

| Tier | Score | Action | Email Sent |
|------|-------|--------|------------|
| 🔥 **HOT** | ≥88% | Immediate contact | ✅ Yes |
| ⭐ **QUALIFIED** | ≥75% | Contact within 24h | ✅ Yes |
| 🌡️ **WARM** | ≥65% | Contact within 48h | ✅ Yes |
| 🌱 **NURTURE** | ≥50% | Drip campaign | ❌ No |
| 👁️ **REVIEW** | ≥35% | Manual review | ❌ No |
| ❌ **NOT_QUALIFIED** | <35% | Reject | ❌ No |

## 📁 Project Structure

```
MatrixNew/
├── frontend/          # React dashboard
├── backend/           # FastAPI backend
│   └── app/
│       ├── api/       # API routes
│       ├── models/    # Database models
│       └── crud/      # Database operations
├── agents/            # Lead qualification agents
│   ├── agent_runner.py      # Main agent orchestrator
│   ├── sales_agent.py       # Email sending agent
│   └── email_service.py     # SMTP email service
├── mcp/               # MCP tools (microservices)
│   ├── aggregator/    # Score aggregation & decision logic
│   ├── email_tool/    # Email validation
│   ├── phone_tool/    # Phone verification
│   ├── company_tool/  # Company enrichment
│   ├── name_tool/     # Name validation
│   └── intent_tool/   # Message intent analysis
└── test_flow.py       # End-to-end test script
```

## 🔧 Configuration

### Email Service Setup

1. **Gmail** (Recommended for testing):
   - Enable 2FA on your Google account
   - Generate App Password: https://myaccount.google.com/apppasswords
   - Add to `agents/.env`

2. **Production** (SendGrid/SES recommended):
   - Better deliverability
   - Higher sending limits
   - Advanced analytics

See `agents/.env.example` for configuration templates.

## 📈 Usage

### Create a Lead
```bash
curl -X POST http://localhost:8000/api/leads \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@techcorp.com",
    "company": "TechCorp",
    "phone": "+1234567890",
    "data": {"message": "Interested in AI solutions"}
  }'
```

### View Leads
```bash
curl http://localhost:8000/api/leads
```

### Dashboard
Open http://localhost:3000 in your browser

## 🧪 Testing

```bash
# Run end-to-end test
python test_flow.py

# Check logs
docker-compose logs -f agents
docker-compose logs -f backend
```

## 📊 Monitoring

### Database Logs
```sql
-- View qualification results
SELECT * FROM logs WHERE event_type = 'agent_result';

-- View email sending status
SELECT * FROM logs WHERE event_type IN ('email_sent', 'email_failed');

-- View qualified leads
SELECT * FROM leads WHERE status IN ('HOT', 'QUALIFIED', 'WARM');
```

## 🎨 Customization

### Adjust Qualification Thresholds
Edit `mcp/aggregator/main.py` - `calculate_score()` function

### Customize Email Templates
Edit `agents/email_service.py` - `generate_qualified_lead_email()` function

### Add High-Value Industries
Edit `mcp/aggregator/main.py` - `HIGH_VALUE_INDUSTRIES` set

## 🔒 Security

- Never commit `.env` files
- Use App Passwords for Gmail (not regular passwords)
- Consider dedicated email service for production
- Implement rate limiting
- Add unsubscribe functionality for compliance

## 📚 Documentation

- **[IMPROVEMENTS_SUMMARY.md](IMPROVEMENTS_SUMMARY.md)** - Quick overview of recent improvements
- **[IMPROVEMENTS.md](IMPROVEMENTS.md)** - Detailed documentation with examples
- **[agents/.env.example](agents/.env.example)** - Email configuration template

## 🛠️ Tech Stack

- **Frontend**: React, TailwindCSS
- **Backend**: FastAPI, SQLAlchemy, SQLite
- **Agents**: Python, httpx, asyncio
- **MCP Tools**: FastAPI microservices
- **AI/LLM**: Groq (Llama 3.1)
- **Email**: SMTP (Gmail, SendGrid, SES, etc.)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

[Your License Here]

## 🆘 Support

For issues or questions:
1. Check [IMPROVEMENTS.md](IMPROVEMENTS.md) for troubleshooting
2. Review logs: `docker-compose logs`
3. Open an issue on GitHub

---

**Built with ❤️ using AI-powered automation**
