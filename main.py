"""Main FastAPI application for LinkedIn post generator."""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import Optional
import uvicorn
from contextlib import asynccontextmanager

from models import init_db
from seed_data import seed_database
from claude_service import ClaudePostGenerator


# Request/Response models
class GeneratePostRequest(BaseModel):
    post_type: str = Field(..., description="Type of LinkedIn post to generate")
    context: str = Field(..., description="Context or topic for the post")
    tone: str = Field(default="professional", description="Tone: professional, casual, or inspirational")
    length: str = Field(default="medium", description="Length: short, medium, or long")


class GeneratePostResponse(BaseModel):
    post: str
    post_type: str
    tips: list[str]


# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database and seed data on startup."""
    print("Initializing database...")
    init_db()
    seed_database()
    print("Application ready!")
    yield
    print("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="LinkedIn Post Generator",
    description="AI-powered LinkedIn post generator inspired by Virio.ai",
    version="1.0.0",
    lifespan=lifespan
)

# Initialize Claude service
generator = ClaudePostGenerator()

# Setup templates
templates = Jinja2Templates(directory="templates")


# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main web interface."""
    post_types = generator.get_post_types()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "post_types": post_types}
    )


@app.get("/api/post-types")
async def get_post_types():
    """Get available post types and their descriptions."""
    return {"post_types": generator.get_post_types()}


@app.post("/api/generate", response_model=GeneratePostResponse)
async def generate_post(request: GeneratePostRequest):
    """
    Generate a LinkedIn post based on user input.

    - **post_type**: Type of post (story, how-to, list, etc.)
    - **context**: Your topic or what you want to write about
    - **tone**: professional, casual, or inspirational
    - **length**: short, medium, or long
    """
    try:
        # Validate post type
        valid_types = [pt["type"] for pt in generator.get_post_types()]
        if request.post_type not in valid_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid post_type. Must be one of: {', '.join(valid_types)}"
            )

        # Generate the post
        post = generator.generate_post(
            post_type=request.post_type,
            context=request.context,
            tone=request.tone,
            length=request.length
        )

        # Get tips for this post type
        tips = get_tips_for_post_type(request.post_type)

        return GeneratePostResponse(
            post=post,
            post_type=request.post_type,
            tips=tips
        )

    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating post: {str(e)}"
        )


def get_tips_for_post_type(post_type: str) -> list[str]:
    """Get engagement tips for a specific post type."""
    tips_map = {
        "story": [
            "Start with the ending or twist to hook readers",
            "Keep paragraphs short (1-2 lines max)",
            "End with a universal lesson others can apply",
            "Use specific details to make it memorable"
        ],
        "how-to": [
            "Make each step actionable and specific",
            "Use numbers and bullets for easy scanning",
            "Include a real example or result if possible",
            "End with a summary or key takeaway"
        ],
        "list": [
            "Keep items parallel in structure",
            "Add brief explanations under each item",
            "Use odd numbers (7, 9) - they perform better",
            "Start with your strongest point"
        ],
        "question": [
            "Ask something people have strong opinions about",
            "Share your own answer first to model responses",
            "Respond to every comment to boost engagement",
            "Make it easy to answer (not too complex)"
        ],
        "insight": [
            "Lead with the contrarian or surprising angle",
            "Back it up with evidence or examples",
            "Acknowledge the common wisdom first",
            "End with implications for your audience"
        ],
        "contrarian": [
            "State the controversial opinion upfront",
            "Explain your reasoning clearly",
            "Acknowledge valid counterarguments",
            "Be respectful - contrarian not combative"
        ],
        "achievement": [
            "Share the struggle, not just the success",
            "Give credit to others who helped",
            "Include actionable lessons learned",
            "Keep humility - inspire don't brag"
        ],
        "data": [
            "Lead with the most surprising statistic",
            "Visualize data if possible (emojis, symbols)",
            "Explain what the data means (so what?)",
            "Include your source for credibility"
        ]
    }

    return tips_map.get(post_type, [
        "Keep paragraphs short and scannable",
        "Use line breaks generously",
        "End with a question or call-to-action",
        "Engage with comments to boost reach"
    ])


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "LinkedIn Post Generator"}


if __name__ == "__main__":
    import os
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", 8000))
    debug = os.getenv("DEBUG", "True").lower() == "true"

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug
    )
