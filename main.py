"""
MCP Sales Server
Provides tools and actions for the Sales API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
import json
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="MCP Sales Server",
    description="Model Context Protocol server for sales tools and actions",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class PitchTemplateRequest(BaseModel):
    industry: str
    pain_points: List[str]
    company_size: Optional[str] = None

class SuccessStoryRequest(BaseModel):
    industry: str
    company_size: Optional[str] = None
    pain_points: Optional[List[str]] = None

class FeatureMatchRequest(BaseModel):
    pain_points: List[str]
    goals: List[str]

class ObjectionRequest(BaseModel):
    objection_type: str
    context: Dict[str, Any]

class ValueCalculationRequest(BaseModel):
    company_size: str
    industry: str
    current_process: Optional[str] = None

class EmailDraftRequest(BaseModel):
    prospect_name: str
    company: str
    pain_points: List[str]
    template_type: str  # "follow_up", "introduction", "demo_invite"

class MeetingScheduleRequest(BaseModel):
    prospect_email: str
    meeting_type: str  # "discovery", "demo", "closing"
    timezone: str
    preferred_times: List[str]


# ============= RETRIEVAL TOOLS =============

@app.post("/tools/pitch_template_retriever")
async def get_pitch_template(request: PitchTemplateRequest):
    """Retrieve personalized pitch template"""
    logger.info(f"Retrieving pitch template for {request.industry}")
    
    # Industry-specific templates
    templates = {
        "technology": {
            "opener": f"I see you're in {request.industry}. Fast-moving tech companies like yours need real-time insights to stay ahead.",
            "pain_point_response": "Many tech companies struggle with manual analysis slowing down their product decisions.",
            "value_prop": "Our AI platform gives you instant market intelligence so you can ship features customers actually want.",
            "cta": "Want to see how we helped a similar SaaS company reduce their research time by 80%?"
        },
        "ecommerce": {
            "opener": f"E-commerce moves fast. You need data-driven decisions, not gut feelings.",
            "pain_point_response": "Most e-commerce teams waste hours analyzing competitors manually.",
            "value_prop": "We automate competitive intelligence so you can focus on growing your business.",
            "cta": "Let me show you how we helped an e-commerce brand increase their margins by 15%."
        },
        "finance": {
            "opener": f"In finance, timing is everything. You need insights before your competitors do.",
            "pain_point_response": "Manual market research puts you behind the curve.",
            "value_prop": "Our platform delivers real-time financial market analysis with AI-powered insights.",
            "cta": "Want to see how we're helping fintech companies make faster decisions?"
        }
    }
    
    template = templates.get(request.industry.lower(), templates["technology"])
    
    return {
        "template": template,
        "industry": request.industry,
        "confidence": 0.92,
        "suggestions": [
            f"Mention specific pain point: {request.pain_points[0] if request.pain_points else 'speed'}",
            "Ask about their current process",
            "Offer a quick demo or case study"
        ]
    }


@app.post("/tools/success_story_finder")
async def get_success_story(request: SuccessStoryRequest):
    """Find relevant customer success story"""
    logger.info(f"Finding success story for {request.industry}")
    
    stories = {
        "technology": {
            "company": "TechFlow (SaaS Platform)",
            "industry": "Technology",
            "size": "50-100 employees",
            "challenge": "Product team spent 20+ hours weekly on manual competitor analysis",
            "solution": "Implemented our AI platform for automated market intelligence",
            "results": {
                "time_saved": "18 hours per week",
                "faster_decisions": "3x speed increase",
                "features_shipped": "+40% more features",
                "cost_savings": "$75K annually"
            },
            "testimonial": "This platform transformed our product strategy. We now ship features our customers actually want.",
            "contact": "Sarah Chen, Head of Product"
        },
        "ecommerce": {
            "company": "StyleHub (Fashion E-commerce)",
            "industry": "E-commerce",
            "size": "20-50 employees",
            "challenge": "Manual competitor price monitoring and trend analysis",
            "solution": "Automated competitive intelligence and trend detection",
            "results": {
                "margin_increase": "15% higher margins",
                "time_saved": "25 hours per month",
                "revenue_impact": "+$200K in first quarter",
                "faster_response": "React to trends 5x faster"
            },
            "testimonial": "We're now ahead of trends instead of chasing them.",
            "contact": "Mike Rodriguez, CEO"
        }
    }
    
    story = stories.get(request.industry.lower(), stories["technology"])
    
    return {
        "success_story": story,
        "relevance_score": 0.88,
        "talking_points": [
            f"Similar company size to yours ({story['size']})",
            f"Faced similar challenge: {story['challenge']}",
            f"Key result: {story['results']['time_saved']}"
        ]
    }


@app.post("/tools/feature_matcher")
async def match_features(request: FeatureMatchRequest):
    """Match platform features to user needs"""
    logger.info(f"Matching features for pain points: {request.pain_points}")
    
    all_features = [
        {
            "id": "ai_market_analysis",
            "name": "AI Market Analysis",
            "category": "Intelligence",
            "description": "Automated competitor and market research with real-time insights",
            "benefits": [
                "Save 15-20 hours per week",
                "Never miss market trends",
                "Data-driven decisions"
            ],
            "matches": ["slow research", "manual analysis", "competitor tracking", "market intelligence"]
        },
        {
            "id": "real_time_streaming",
            "name": "Real-time AI Streaming",
            "category": "UX",
            "description": "See AI thinking in real-time as it generates analysis",
            "benefits": [
                "Transparent AI process",
                "Interactive analysis",
                "Immediate feedback"
            ],
            "matches": ["transparency", "trust", "speed", "interaction"]
        },
        {
            "id": "social_intelligence",
            "name": "Social Media Intelligence",
            "category": "Marketing",
            "description": "Track brand mentions, sentiment, and trending topics",
            "benefits": [
                "Monitor brand reputation",
                "Identify opportunities",
                "Engage at the right time"
            ],
            "matches": ["social media", "brand monitoring", "sentiment", "reputation"]
        },
        {
            "id": "content_generation",
            "name": "AI Content Generation",
            "category": "Content",
            "description": "Generate marketing content, social posts, and reports",
            "benefits": [
                "10x faster content creation",
                "Consistent brand voice",
                "SEO-optimized output"
            ],
            "matches": ["content", "writing", "marketing", "social posts"]
        }
    ]
    
    # Simple matching logic
    matched = []
    all_text = " ".join(request.pain_points + request.goals).lower()
    
    for feature in all_features:
        relevance = sum(1 for keyword in feature["matches"] if keyword in all_text)
        if relevance > 0:
            matched.append({
                **feature,
                "relevance_score": min(relevance * 0.3, 1.0),
                "why_relevant": f"Addresses: {', '.join([p for p in request.pain_points[:2]])}"
            })
    
    # Sort by relevance
    matched.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    return {
        "matched_features": matched[:3],
        "total_matches": len(matched)
    }


@app.post("/tools/objection_handler")
async def handle_objection(request: ObjectionRequest):
    """Get objection handling script"""
    logger.info(f"Handling objection: {request.objection_type}")
    
    responses = {
        "price": {
            "response": "I understand cost is important. Let me show you the ROI our customers see. Most save 20+ hours per week - that's essentially a full-time employee. What's that worth to your team?",
            "follow_up": "Would it help to see a detailed cost-benefit breakdown for your specific situation?",
            "proof_points": [
                "Average ROI: 5x within 6 months",
                "Typical payback period: 2-3 months",
                "Most customers save $50K+ annually"
            ]
        },
        "timing": {
            "response": "I hear you on timing. Here's the thing - the longer you wait, the more time your team wastes on manual analysis. What if we could get you up and running in just 3 days?",
            "follow_up": "We have a quick-start program specifically for busy teams. Want to hear about it?",
            "proof_points": [
                "Average onboarding: 3-5 days",
                "No IT resources needed",
                "Start seeing value immediately"
            ]
        },
        "features": {
            "response": "Great question. Let me walk you through exactly what you need for your situation. What's your top priority?",
            "follow_up": "Would a quick demo showing those specific features be helpful?",
            "proof_points": [
                "Built for [user's industry]",
                "Covers 90% of use cases out of the box",
                "Custom features available"
            ]
        },
        "competitors": {
            "response": "Good question - we're different in three key ways: [1] Real-time streaming AI so you see the thinking process, [2] Specialized brains for different tasks, not one generic AI, [3] Built-in learning that gets smarter over time.",
            "follow_up": "Want to see a side-by-side comparison with [competitor]?",
            "proof_points": [
                "Only platform with real-time streaming",
                "7 specialized AI brains vs generic chatbot",
                "Customers report 2x better results vs alternatives"
            ]
        },
        "trust": {
            "response": "I totally get it - trusting a new platform is a big decision. That's why we offer a risk-free 14-day trial. See results first, then decide.",
            "follow_up": "Would you like to start with a small pilot project to test it out?",
            "proof_points": [
                "Used by [X] companies",
                "99.9% uptime SLA",
                "Money-back guarantee"
            ]
        }
    }
    
    objection_type = request.objection_type.lower()
    response = responses.get(objection_type, responses["trust"])
    
    return {
        "response": response["response"],
        "follow_up_question": response["follow_up"],
        "proof_points": response["proof_points"],
        "confidence": 0.91
    }


@app.post("/tools/value_calculator")
async def calculate_value(request: ValueCalculationRequest):
    """Calculate ROI and value proposition"""
    logger.info(f"Calculating value for {request.company_size} in {request.industry}")
    
    # Size-based calculations
    multipliers = {
        "startup": {"hours": 10, "cost_per_hour": 75, "efficiency": 0.7},
        "small": {"hours": 15, "cost_per_hour": 85, "efficiency": 0.75},
        "medium": {"hours": 20, "cost_per_hour": 100, "efficiency": 0.8},
        "large": {"hours": 30, "cost_per_hour": 125, "efficiency": 0.85}
    }
    
    size_key = request.company_size.lower()
    if size_key not in multipliers:
        size_key = "medium"
    
    metrics = multipliers[size_key]
    
    weekly_hours_saved = metrics["hours"] * metrics["efficiency"]
    weekly_value = weekly_hours_saved * metrics["cost_per_hour"]
    monthly_value = weekly_value * 4
    annual_value = monthly_value * 12
    
    return {
        "time_savings": {
            "weekly_hours": round(weekly_hours_saved, 1),
            "monthly_hours": round(weekly_hours_saved * 4, 1),
            "annual_hours": round(weekly_hours_saved * 52, 1)
        },
        "financial_impact": {
            "weekly": f"${weekly_value:,.0f}",
            "monthly": f"${monthly_value:,.0f}",
            "annual": f"${annual_value:,.0f}"
        },
        "roi": {
            "payback_period": "2-3 months",
            "first_year_roi": "500-700%",
            "break_even": "Within 90 days"
        },
        "additional_benefits": [
            "Faster decision making (3x speed increase)",
            "Better decisions (data-driven vs gut feel)",
            "Competitive advantage (react to market faster)",
            "Team satisfaction (no more manual work)"
        ]
    }


# ============= ACTION TOOLS =============

@app.post("/tools/draft_email")
async def draft_email(request: EmailDraftRequest):
    """Generate personalized email draft"""
    logger.info(f"Drafting {request.template_type} email for {request.prospect_name}")
    
    templates = {
        "follow_up": f"""Subject: Quick follow-up - {request.company}

Hi {request.prospect_name},

Thanks for our conversation earlier. I've been thinking about what you mentioned regarding {request.pain_points[0] if request.pain_points else 'your challenges'}.

I wanted to share a quick case study of how we helped a similar company solve this exact problem. They saw results in the first week.

Would you be open to a 15-minute demo? I can show you exactly how this would work for {request.company}.

Best,
[Your name]

P.S. - I can do this week if that works for you.""",

        "introduction": f"""Subject: Solving {request.pain_points[0] if request.pain_points else 'your challenges'} at {request.company}

Hi {request.prospect_name},

I noticed {request.company} is {request.pain_points[0] if request.pain_points else 'growing fast'}.

Most companies at your stage struggle with this - which is why we built our AI platform specifically for teams like yours.

Quick question: How much time does your team spend on manual analysis each week?

I ask because our customers typically save 15-20 hours weekly, which they reinvest into actually building/growing their business.

Worth a quick 10-minute call to explore?

Best,
[Your name]""",

        "demo_invite": f"""Subject: {request.company} + AI Platform Demo

Hi {request.prospect_name},

I've set up a custom demo environment for {request.company} that shows exactly how our platform addresses:

• {request.pain_points[0] if request.pain_points else 'Your key challenge'}
• {request.pain_points[1] if len(request.pain_points) > 1 else 'Faster insights'}

The demo takes 15 minutes and you'll see real results with your own use case.

When works better for you - this week or next?

Best,
[Your name]

P.S. - I'll show you ROI numbers specific to your situation."""
    }
    
    email_content = templates.get(request.template_type, templates["follow_up"])
    
    return {
        "subject": email_content.split('\n')[0].replace("Subject: ", ""),
        "body": '\n'.join(email_content.split('\n')[2:]),
        "tone": "professional, friendly",
        "estimated_response_rate": "25-35%",
        "best_send_time": "Tuesday or Wednesday, 9-11am"
    }


@app.post("/tools/schedule_meeting")
async def schedule_meeting(request: MeetingScheduleRequest):
    """Generate meeting scheduling message"""
    logger.info(f"Scheduling {request.meeting_type} meeting")
    
    meeting_info = {
        "discovery": {
            "duration": "30 minutes",
            "agenda": [
                "Understand your current process",
                "Identify pain points and goals",
                "Show relevant case studies",
                "Discuss potential fit"
            ]
        },
        "demo": {
            "duration": "15-20 minutes",
            "agenda": [
                "Live demo with your use case",
                "Show key features",
                "Answer specific questions",
                "Discuss next steps"
            ]
        },
        "closing": {
            "duration": "45 minutes",
            "agenda": [
                "Review proposal and pricing",
                "Address final questions",
                "Discuss implementation",
                "Close the deal"
            ]
        }
    }
    
    info = meeting_info.get(request.meeting_type, meeting_info["demo"])
    
    return {
        "meeting_type": request.meeting_type,
        "duration": info["duration"],
        "agenda": info["agenda"],
        "scheduling_message": f"""I'd love to schedule our {request.meeting_type} call.

Duration: {info["duration"]}
Agenda:
{chr(10).join([f"• {item}" for item in info["agenda"]])}

What time works best for you? I'm flexible with these times:
{chr(10).join([f"• {time}" for time in request.preferred_times[:3]])}

Looking forward to it!""",
        "calendar_title": f"{request.meeting_type.title()} Call - [Company Name]",
        "suggested_tools": ["Calendly", "Cal.com", "Google Calendar"]
    }


# ============= HEALTH & INFO =============

@app.get("/")
async def root():
    return {
        "service": "MCP Sales Server",
        "version": "1.0.0",
        "status": "operational",
        "tools": [
            "pitch_template_retriever",
            "success_story_finder",
            "feature_matcher",
            "objection_handler",
            "value_calculator",
            "draft_email",
            "schedule_meeting"
        ]
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/tools")
async def list_tools():
    """List all available tools"""
    return {
        "retrieval_tools": [
            {
                "name": "pitch_template_retriever",
                "description": "Get personalized pitch template based on industry and pain points",
                "endpoint": "/tools/pitch_template_retriever"
            },
            {
                "name": "success_story_finder",
                "description": "Find relevant customer success story",
                "endpoint": "/tools/success_story_finder"
            },
            {
                "name": "feature_matcher",
                "description": "Match features to user needs",
                "endpoint": "/tools/feature_matcher"
            },
            {
                "name": "objection_handler",
                "description": "Get response for common objections",
                "endpoint": "/tools/objection_handler"
            },
            {
                "name": "value_calculator",
                "description": "Calculate ROI and value proposition",
                "endpoint": "/tools/value_calculator"
            }
        ],
        "action_tools": [
            {
                "name": "draft_email",
                "description": "Generate personalized email draft",
                "endpoint": "/tools/draft_email"
            },
            {
                "name": "schedule_meeting",
                "description": "Create meeting scheduling message",
                "endpoint": "/tools/schedule_meeting"
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
