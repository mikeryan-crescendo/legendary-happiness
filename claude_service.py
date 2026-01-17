"""Claude API service for generating LinkedIn posts."""

import os
from typing import List
from anthropic import Anthropic
from models import LinkedInPost, SessionLocal
import random


class ClaudePostGenerator:
    """Generate LinkedIn posts using Claude API."""

    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        self.client = Anthropic(api_key=api_key)

    def get_example_posts(self, post_type: str, limit: int = 3) -> List[LinkedInPost]:
        """Get example posts of a specific type from the database."""
        db = SessionLocal()
        try:
            posts = (
                db.query(LinkedInPost)
                .filter(LinkedInPost.post_type == post_type)
                .order_by(LinkedInPost.engagement_score.desc())
                .limit(limit)
                .all()
            )
            return posts
        finally:
            db.close()

    def generate_post(
        self,
        post_type: str,
        context: str,
        tone: str = "professional",
        length: str = "medium"
    ) -> str:
        """
        Generate a LinkedIn post using Claude API.

        Args:
            post_type: Type of post (story, how-to, list, question, insight, etc.)
            context: User's context/topic for the post
            tone: Tone of the post (professional, casual, inspirational)
            length: Length of post (short, medium, long)

        Returns:
            Generated LinkedIn post
        """
        # Get example posts for this type
        examples = self.get_example_posts(post_type, limit=3)

        # Build examples text
        examples_text = "\n\n---\n\n".join([
            f"Example {i+1} (Engagement: {post.engagement_score}):\n{post.content}"
            for i, post in enumerate(examples)
        ])

        # Define length guidelines
        length_guide = {
            "short": "100-150 words, punchy and concise",
            "medium": "150-250 words, balanced detail and readability",
            "long": "250-400 words, in-depth but still engaging"
        }

        # Build the prompt
        prompt = f"""You are an expert LinkedIn content creator specializing in viral posts. Your task is to create a high-engagement LinkedIn post.

POST TYPE: {post_type}
USER CONTEXT: {context}
TONE: {tone}
LENGTH: {length_guide.get(length, length_guide['medium'])}

Here are examples of high-performing {post_type} posts on LinkedIn:

{examples_text}

INSTRUCTIONS:
1. Analyze the examples above to understand what makes this post type engaging
2. Create a NEW post based on the user's context that follows similar patterns
3. Use proven engagement techniques:
   - Strong hook in first 1-2 lines
   - Short paragraphs and line breaks for readability
   - Emotional resonance or valuable insights
   - Clear takeaways or lessons
   - Conversational tone
   - Strategic use of → bullets or numbered lists
   - End with a call-to-action or thought-provoking question (if appropriate)

4. Make it authentic and personal, not generic corporate speak
5. Focus on VALUE first, self-promotion last (or never)
6. Optimize for stopping scrollers and sparking comments

Generate ONLY the post content - no titles, no explanations, no meta-commentary.
Make it ready to copy-paste directly into LinkedIn.

POST:"""

        # Call Claude API
        message = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2000,
            temperature=0.7,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Extract the generated post
        generated_post = message.content[0].text.strip()

        return generated_post

    def get_post_types(self) -> List[dict]:
        """Get available post types with descriptions."""
        return [
            {
                "type": "story",
                "name": "Personal Story",
                "description": "Share a personal experience or journey with a lesson learned. High emotional impact.",
                "best_for": "Building personal brand, creating emotional connection, showing vulnerability"
            },
            {
                "type": "how-to",
                "name": "How-To Guide",
                "description": "Step-by-step actionable advice or tutorial. Pure value delivery.",
                "best_for": "Establishing expertise, providing actionable value, teaching"
            },
            {
                "type": "list",
                "name": "List/Listicle",
                "description": "Numbered or bulleted list of tips, lessons, or insights. Easy to scan and share.",
                "best_for": "Quick value, high shareability, easy consumption"
            },
            {
                "type": "question",
                "name": "Engagement Question",
                "description": "Thought-provoking question that sparks discussion and comments.",
                "best_for": "Driving comments, starting conversations, community building"
            },
            {
                "type": "insight",
                "name": "Industry Insight",
                "description": "Unique perspective or observation about your industry or profession.",
                "best_for": "Thought leadership, demonstrating expertise, sparking debate"
            },
            {
                "type": "contrarian",
                "name": "Contrarian Take",
                "description": "Challenge common wisdom with a bold, different perspective.",
                "best_for": "Standing out, sparking debate, building thought leadership"
            },
            {
                "type": "achievement",
                "name": "Achievement/Milestone",
                "description": "Share a win or milestone with lessons learned along the way.",
                "best_for": "Credibility building, inspiring others, humble bragging done right"
            },
            {
                "type": "data",
                "name": "Data-Driven Post",
                "description": "Share interesting statistics or research findings with insights.",
                "best_for": "Authority building, providing unique value, getting saves/shares"
            }
        ]
