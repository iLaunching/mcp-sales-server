# MCP Sales Server

Model Context Protocol server providing tools and actions for the Sales API.

## Features

### Retrieval Tools
- **Pitch Template Retriever**: Get personalized pitch templates based on industry and pain points
- **Success Story Finder**: Find relevant customer success stories
- **Feature Matcher**: Match platform features to user needs
- **Objection Handler**: Get responses for common objections (price, timing, features, competitors, trust)
- **Value Calculator**: Calculate ROI and value proposition

### Action Tools
- **Draft Email**: Generate personalized email drafts (follow_up, introduction, demo_invite)
- **Schedule Meeting**: Create meeting scheduling messages (discovery, demo, closing)

## Quick Start

### Local Development
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8081
```

Visit: http://localhost:8081

### Docker
```bash
docker build -t mcp-sales-server .
docker run -p 8081:8081 mcp-sales-server
```

### Railway Deployment
```bash
# Deploy to Railway
railway up

# Set environment variables (optional)
railway variables set PORT=8081
```

## API Endpoints

### Information
- `GET /` - Server info
- `GET /health` - Health check
- `GET /tools` - List all tools

### Retrieval Tools
- `POST /tools/pitch_template_retriever` - Get pitch template
- `POST /tools/success_story_finder` - Find success story
- `POST /tools/feature_matcher` - Match features
- `POST /tools/objection_handler` - Handle objection
- `POST /tools/value_calculator` - Calculate value

### Action Tools
- `POST /tools/draft_email` - Generate email draft
- `POST /tools/schedule_meeting` - Create meeting message

## Example Usage

### Get Pitch Template
```bash
curl -X POST http://localhost:8081/tools/pitch_template_retriever \
  -H "Content-Type: application/json" \
  -d '{
    "industry": "technology",
    "pain_points": ["slow research", "manual analysis"],
    "company_size": "medium"
  }'
```

### Draft Follow-up Email
```bash
curl -X POST http://localhost:8081/tools/draft_email \
  -H "Content-Type: application/json" \
  -d '{
    "prospect_name": "John",
    "company": "TechCorp",
    "pain_points": ["manual competitor analysis"],
    "template_type": "follow_up"
  }'
```

### Calculate Value
```bash
curl -X POST http://localhost:8081/tools/value_calculator \
  -H "Content-Type: application/json" \
  -d '{
    "company_size": "medium",
    "industry": "technology"
  }'
```

## Integration with Sales API

Update your Sales API's `.env`:
```bash
MCP_ENABLED=true
MCP_SERVER_URL=https://your-mcp-server.railway.app
```

The Sales API will automatically use these tools during conversations.

## Architecture

```
Sales API → MCP Server → Tools/Actions
                      ↓
            - Pitch Templates
            - Success Stories  
            - Feature Matching
            - Objection Handling
            - Value Calculation
            - Email Generation
            - Meeting Scheduling
```

## Development Roadmap

### Phase 1 (Current)
- ✅ Basic retrieval tools
- ✅ Action tools (email, meeting)
- ✅ REST API

### Phase 2 (Next)
- [ ] Add Qdrant vector DB for semantic search
- [ ] Real customer data integration
- [ ] A/B testing for templates
- [ ] Analytics tracking

### Phase 3 (Future)
- [ ] CRM integration (HubSpot, Salesforce)
- [ ] Calendar API integration (Google, Outlook)
- [ ] Email sending (SendGrid, Postmark)
- [ ] WebSocket support for real-time

## License

MIT
