# LinkedIn Post Generator

An AI-powered LinkedIn post generator inspired by Virio.ai. Create viral LinkedIn posts using Claude AI and a database of high-performing post examples.

## Features

- **8 Post Types**: Story, How-To, List, Question, Insight, Contrarian, Achievement, Data-Driven
- **AI-Powered**: Uses Anthropic's Claude API for intelligent content generation
- **Curated Examples**: Database of 15+ high-performing LinkedIn posts (engagement 8K-25K)
- **Customization**: Choose tone (professional, casual, inspirational) and length
- **Web Interface**: Beautiful, easy-to-use web UI
- **CLI Tool**: Interactive command-line interface for terminal users
- **REST API**: Full API for programmatic access
- **Engagement Tips**: Get specific tips for each post type

## Quick Start

### 1. Prerequisites

- Python 3.8+
- Anthropic API key ([get one here](https://console.anthropic.com/))

### 2. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd legendary-happiness

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:

```
ANTHROPIC_API_KEY=your_api_key_here
```

### 4. Initialize Database

```bash
python seed_data.py
```

This will create a SQLite database with 15 curated high-performing LinkedIn posts.

### 5. Run the Application

```bash
python main.py
```

The application will start at `http://localhost:8000`

## Usage

### Web Interface

1. Open `http://localhost:8000` in your browser
2. Select a post type (Story, How-To, List, etc.)
3. Describe what you want to write about
4. Choose tone and length
5. Click "Generate Post"
6. Copy your viral-ready LinkedIn post!

### Command-Line Interface (CLI)

For a terminal-based experience:

```bash
python cli.py
```

The CLI will guide you through:
1. Selecting a post type
2. Providing context
3. Choosing tone and length
4. Generating and displaying your post

**View available post types:**
```bash
python cli.py --types
```

### API Usage

**Get available post types:**
```bash
curl http://localhost:8000/api/post-types
```

**Generate a post:**
```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "post_type": "story",
    "context": "I learned an important lesson about delegation when I hired my first employee",
    "tone": "professional",
    "length": "medium"
  }'
```

## Post Types

| Type | Description | Best For |
|------|-------------|----------|
| **Story** | Personal experience with a lesson | Building personal brand, emotional connection |
| **How-To** | Step-by-step actionable guide | Establishing expertise, providing value |
| **List** | Numbered tips or insights | Quick value, high shareability |
| **Question** | Thought-provoking discussion starter | Driving comments, community building |
| **Insight** | Unique industry perspective | Thought leadership, demonstrating expertise |
| **Contrarian** | Challenge common wisdom | Standing out, sparking debate |
| **Achievement** | Share wins with lessons learned | Credibility building, inspiring others |
| **Data** | Statistics with insights | Authority building, unique value |

## Project Structure

```
legendary-happiness/
├── main.py                 # FastAPI application
├── cli.py                  # Command-line interface
├── models.py               # Database models
├── claude_service.py       # Claude API integration
├── seed_data.py            # Sample data loader
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── templates/
│   └── index.html          # Web interface
└── README.md               # This file
```

## How It Works

1. **Database of Examples**: The system stores 15+ high-performing LinkedIn posts categorized by type
2. **Example Selection**: When generating a post, it retrieves the top 3 examples of that type
3. **Prompt Engineering**: Creates a detailed prompt for Claude including examples and best practices
4. **AI Generation**: Claude analyzes the examples and generates a new post matching the style
5. **Optimization**: The prompt includes proven engagement techniques (hooks, formatting, CTAs)

## Viral Post Techniques Built-In

- Strong hooks in first 1-2 lines
- Short paragraphs with line breaks
- Strategic use of bullets and lists
- Emotional resonance or valuable insights
- Clear takeaways
- Call-to-action when appropriate
- Optimized for stopping scrollers

## Customization

### Adding Your Own Posts

Edit `seed_data.py` and add your own high-performing posts to the `SAMPLE_POSTS` list:

```python
{
    "post_type": "story",
    "content": "Your post content here...",
    "engagement_score": 15000,
    "author": "Your Name",
    "industry": "Your Industry"
}
```

Then run:
```bash
rm linkedin_posts.db  # Delete old database
python seed_data.py   # Recreate with new posts
```

### Adjusting AI Behavior

Edit `claude_service.py` to modify:
- Temperature (creativity level)
- Max tokens (post length limits)
- System prompt (instructions to Claude)
- Model selection

## API Reference

### POST /api/generate

Generate a LinkedIn post.

**Request Body:**
```json
{
  "post_type": "story",
  "context": "What you want to write about",
  "tone": "professional",
  "length": "medium"
}
```

**Response:**
```json
{
  "post": "Generated LinkedIn post content...",
  "post_type": "story",
  "tips": [
    "Tip 1 for maximizing engagement",
    "Tip 2 for maximizing engagement"
  ]
}
```

### GET /api/post-types

Get all available post types with descriptions.

**Response:**
```json
{
  "post_types": [
    {
      "type": "story",
      "name": "Personal Story",
      "description": "Share a personal experience...",
      "best_for": "Building personal brand..."
    }
  ]
}
```

## Tips for Best Results

1. **Be Specific**: The more context you provide, the better the output
2. **Match Your Voice**: Choose the tone that matches your personal brand
3. **Edit & Personalize**: Use the AI output as a starting point, then add your unique touch
4. **Test Different Types**: Try multiple post types for the same topic to see what resonates
5. **Engage After Posting**: Reply to every comment to maximize reach

## Troubleshooting

**"ANTHROPIC_API_KEY environment variable not set"**
- Make sure you created a `.env` file with your API key

**"Database already contains X posts. Skipping seed."**
- This is normal - the database was already initialized
- To reinitialize: `rm linkedin_posts.db && python seed_data.py`

**Posts feel too generic**
- Provide more specific context and details
- Consider editing the generated post to add personal touches
- Try adjusting the tone and length settings

## Contributing

This is a personal project, but feel free to fork and customize for your needs!

## License

MIT License - feel free to use this for personal or commercial projects.

## Credits

- Inspired by [Virio.ai](https://virio.ai)
- Powered by [Anthropic Claude](https://www.anthropic.com)
- Built with [FastAPI](https://fastapi.tiangolo.com)

---

**Happy posting!** Create content that stops the scroll and starts conversations.
