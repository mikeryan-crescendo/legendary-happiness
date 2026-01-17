#!/usr/bin/env python
"""Command-line interface for LinkedIn Post Generator."""

import sys
from dotenv import load_dotenv
from claude_service import ClaudePostGenerator
from seed_data import seed_database
from models import init_db

# Load environment variables
load_dotenv()


def print_banner():
    """Print CLI banner."""
    print("\n" + "="*60)
    print("  LinkedIn Post Generator - CLI")
    print("  AI-Powered Viral Content Creation")
    print("="*60 + "\n")


def print_post_types(generator):
    """Display available post types."""
    print("Available Post Types:\n")
    post_types = generator.get_post_types()

    for i, pt in enumerate(post_types, 1):
        print(f"{i}. {pt['name']} ({pt['type']})")
        print(f"   {pt['description']}")
        print(f"   Best for: {pt['best_for']}\n")


def get_user_input():
    """Get user input for post generation."""
    print("Let's create your LinkedIn post!\n")

    # Get post type
    print("Select post type (or type the number):")
    post_types = ["story", "how-to", "list", "question", "insight", "contrarian", "achievement", "data"]

    for i, pt in enumerate(post_types, 1):
        print(f"  {i}. {pt}")

    while True:
        choice = input("\nPost type (1-8 or name): ").strip()

        if choice.isdigit() and 1 <= int(choice) <= 8:
            post_type = post_types[int(choice) - 1]
            break
        elif choice in post_types:
            post_type = choice
            break
        else:
            print("Invalid choice. Please try again.")

    # Get context
    print(f"\nWhat do you want to write about?")
    print("(Provide as much context and detail as possible)")
    print("Type your context below (press Enter twice when done):\n")

    lines = []
    empty_count = 0

    while empty_count < 2:
        line = input()
        if line.strip() == "":
            empty_count += 1
        else:
            empty_count = 0
            lines.append(line)

    context = "\n".join(lines).strip()

    if not context:
        print("Context cannot be empty!")
        sys.exit(1)

    # Get tone
    print("\nSelect tone:")
    print("  1. Professional (default)")
    print("  2. Casual")
    print("  3. Inspirational")

    tone_choice = input("\nTone (1-3, default=1): ").strip() or "1"
    tones = {"1": "professional", "2": "casual", "3": "inspirational"}
    tone = tones.get(tone_choice, "professional")

    # Get length
    print("\nSelect length:")
    print("  1. Short (100-150 words)")
    print("  2. Medium (150-250 words) - default")
    print("  3. Long (250-400 words)")

    length_choice = input("\nLength (1-3, default=2): ").strip() or "2"
    lengths = {"1": "short", "2": "medium", "3": "long"}
    length = lengths.get(length_choice, "medium")

    return {
        "post_type": post_type,
        "context": context,
        "tone": tone,
        "length": length
    }


def display_post(post_data, generated_post, tips):
    """Display the generated post and tips."""
    print("\n" + "="*60)
    print("  YOUR GENERATED LINKEDIN POST")
    print("="*60 + "\n")
    print(generated_post)
    print("\n" + "="*60)

    print("\n📊 TIPS TO MAXIMIZE ENGAGEMENT:\n")
    for i, tip in enumerate(tips, 1):
        print(f"  {i}. {tip}")

    print("\n" + "="*60)
    print("\nCopy the post above and paste it into LinkedIn!")
    print("Want to generate another? Run this script again.\n")


def main():
    """Main CLI function."""
    print_banner()

    # Initialize database
    print("Initializing database...")
    init_db()
    seed_database()

    # Initialize generator
    try:
        generator = ClaudePostGenerator()
    except ValueError as e:
        print(f"ERROR: {e}")
        print("\nMake sure you have set ANTHROPIC_API_KEY in your .env file")
        print("Get your API key at: https://console.anthropic.com/\n")
        sys.exit(1)

    # Check if user wants to see post types
    if len(sys.argv) > 1 and sys.argv[1] in ["--types", "-t", "types"]:
        print_post_types(generator)
        sys.exit(0)

    # Get user input
    params = get_user_input()

    # Generate post
    print("\n⏳ Generating your viral LinkedIn post...")
    print("(This may take 10-30 seconds)\n")

    try:
        generated_post = generator.generate_post(**params)

        # Get tips
        tips_map = {
            "story": [
                "Start with the ending or twist to hook readers",
                "Keep paragraphs short (1-2 lines max)",
                "End with a universal lesson others can apply"
            ],
            "how-to": [
                "Make each step actionable and specific",
                "Use numbers and bullets for easy scanning",
                "Include a real example or result"
            ],
            "list": [
                "Keep items parallel in structure",
                "Use odd numbers (7, 9) - they perform better",
                "Add brief explanations under each item"
            ],
            "question": [
                "Ask something people have strong opinions about",
                "Share your own answer first to model responses",
                "Respond to every comment to boost engagement"
            ],
            "insight": [
                "Lead with the contrarian or surprising angle",
                "Back it up with evidence or examples",
                "End with implications for your audience"
            ],
            "contrarian": [
                "State the controversial opinion upfront",
                "Explain your reasoning clearly",
                "Be respectful - contrarian not combative"
            ],
            "achievement": [
                "Share the struggle, not just the success",
                "Give credit to others who helped",
                "Include actionable lessons learned"
            ],
            "data": [
                "Lead with the most surprising statistic",
                "Explain what the data means (so what?)",
                "Include your source for credibility"
            ]
        }

        tips = tips_map.get(params["post_type"], [
            "Keep paragraphs short and scannable",
            "Use line breaks generously",
            "End with a question or call-to-action"
        ])

        display_post(params, generated_post, tips)

    except Exception as e:
        print(f"\n❌ Error generating post: {e}")
        print("Please try again or check your API key.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
