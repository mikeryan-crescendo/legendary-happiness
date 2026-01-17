"""Seed data with high-performing LinkedIn posts."""

from models import LinkedInPost, SessionLocal, init_db

SAMPLE_POSTS = [
    # STORY posts
    {
        "post_type": "story",
        "content": """I got fired from my first job in tech.

Best thing that ever happened to me.

Here's what I learned:

My manager called me into her office on a Friday.
"This isn't working out," she said.

I was devastated. I thought my career was over.

But here's the truth nobody tells you:

→ Getting fired isn't failure, it's redirection
→ Sometimes you need to be pushed to jump
→ The job that fires you isn't the job meant for you

6 months later, I started my own company.
3 years later, we hit $10M in revenue.
5 years later, I hired my former manager.

The lesson?

What feels like an ending is often just the beginning.

Your biggest setback might be setting you up for your greatest comeback.""",
        "engagement_score": 15000,
        "author": "Tech Entrepreneur",
        "industry": "Technology"
    },
    {
        "post_type": "story",
        "content": """My 6-year-old daughter taught me the best business lesson I've learned in 20 years.

Last week, she set up a lemonade stand.

I watched her struggle with pricing, customer service, and inventory.

Then something magical happened:

A customer complained the lemonade was too sour.

Instead of getting defensive, she:
→ Asked what would make it better
→ Made a fresh batch on the spot
→ Gave him the first glass free

"I want him to come back tomorrow," she said.

She gets it.

She understands what took me years to learn:

Customer feedback isn't criticism.
It's free consulting.

Sometimes the best business wisdom comes from the smallest voices.""",
        "engagement_score": 12000,
        "author": "Business Leader",
        "industry": "Entrepreneurship"
    },

    # HOW-TO posts
    {
        "post_type": "how-to",
        "content": """How to 10x your productivity without burning out:

I went from working 80 hours a week to 40 hours while doubling my output.

Here's my exact system:

1. The 3-Task Rule
   → Pick only 3 critical tasks per day
   → Everything else is a bonus
   → Finish these before checking email

2. Time Blocking
   → 9-11am: Deep work (no meetings)
   → 11-12pm: Communications
   → 1-3pm: Meetings only
   → 3-5pm: Admin and planning

3. The 2-Minute Rule
   → If it takes less than 2 minutes, do it now
   → Everything else gets scheduled
   → Never let small tasks pile up

4. Energy Management Over Time Management
   → Schedule hard tasks when you're energized
   → Your peak hours are sacred
   → Protect them ruthlessly

5. The Weekly Review
   → Friday afternoon: Review wins and losses
   → Plan next week's priorities
   → Adjust systems that aren't working

The result?
→ More output in less time
→ Better work-life balance
→ Actually enjoy what I do

Productivity isn't about doing more.
It's about doing what matters.""",
        "engagement_score": 18000,
        "author": "Productivity Coach",
        "industry": "Professional Development"
    },
    {
        "post_type": "how-to",
        "content": """How I grew my LinkedIn following from 500 to 50,000 in 12 months:

No paid ads. No bots. Just strategy.

Here's the playbook:

Step 1: Find Your Lane
→ Pick ONE topic you can own
→ Become known for that thing
→ Don't try to be everything to everyone

Step 2: The 3-3-3 Content Formula
→ 3 posts per week minimum
→ 3 value bombs per post
→ 3 engaging questions to spark comments

Step 3: Hook in First 2 Lines
→ If they don't stop scrolling, you lost
→ Start with a bold statement
→ Or a personal story that resonates

Step 4: Engage Like Your Life Depends On It
→ Spend 30 min daily commenting on others' posts
→ Thoughtful comments, not "Great post!"
→ Build real relationships

Step 5: Study Your Analytics
→ Double down on what works
→ Kill what doesn't
→ Track engagement rate, not just likes

The secret?

Consistency beats perfection.
Show up daily, provide value, and the growth follows.""",
        "engagement_score": 22000,
        "author": "LinkedIn Growth Expert",
        "industry": "Marketing"
    },

    # LIST posts
    {
        "post_type": "list",
        "content": """10 harsh truths about career growth nobody wants to hear:

1. Working hard doesn't guarantee success
   → Working smart does

2. Your loyalty means nothing if you're underpaid
   → Companies will replace you in 2 weeks

3. Titles are overrated
   → Skills pay the bills

4. Your network is more valuable than your GPA
   → Relationships open doors

5. You're probably not as good as you think
   → Stay humble, keep learning

6. Comfort is the enemy of growth
   → If you're comfortable, you're stagnating

7. Nobody cares about your 10-year plan
   → Focus on the next 90 days

8. Your mentor should scare you a little
   → If you're the smartest in the room, find a new room

9. Waiting for permission will keep you stuck
   → Forgive yourself and take action

10. You'll regret the risks you didn't take
    → Not the ones you did

Save this for when you need a reality check.""",
        "engagement_score": 20000,
        "author": "Career Coach",
        "industry": "Career Development"
    },
    {
        "post_type": "list",
        "content": """7 things I wish I knew before becoming a manager:

1. Your job is no longer to be the best player
   → It's to make your team the best players

2. You'll spend 80% of your time on people problems
   → Technical skills become secondary

3. Not everyone wants your job
   → And that's perfectly okay

4. Your bad days become their bad days
   → Your mood sets the team's mood

5. Feedback is a gift you give too rarely
   → Don't wait for performance reviews

6. The best leaders create more leaders
   → Not more followers

7. You'll be lonely sometimes
   → You can't vent to your team about your team

Management isn't a promotion.
It's a career change.

Treat it accordingly.""",
        "engagement_score": 16000,
        "author": "Engineering Manager",
        "industry": "Leadership"
    },

    # QUESTION posts
    {
        "post_type": "question",
        "content": """Honest question for founders:

What's the ONE thing you wish you'd done differently in your first year?

For me, it was hiring too slowly.

I tried to do everything myself for way too long.

By the time I hired, I was burned out and the business had suffered.

Now I hire before I think I need to.

What about you?

Drop your lessons below 👇""",
        "engagement_score": 8000,
        "author": "Startup Founder",
        "industry": "Entrepreneurship"
    },
    {
        "post_type": "question",
        "content": """Controversial take:

"Follow your passion" is terrible career advice.

Here's what I think instead:

→ Follow your skills
→ Build your passion along the way
→ Get so good they can't ignore you

Most people don't start passionate about what they do.
They become passionate because they're excellent at it.

Am I wrong?

Let's debate this in the comments.""",
        "engagement_score": 14000,
        "author": "Career Strategist",
        "industry": "Career Development"
    },

    # INSIGHT posts
    {
        "post_type": "insight",
        "content": """The #1 difference between senior and junior developers?

It's not coding skill.
It's not years of experience.
It's not even technical knowledge.

It's this:

Junior devs focus on writing code.
Senior devs focus on NOT writing code.

Here's what I mean:

→ Before writing, they ask: "Should this even exist?"
→ They delete more code than they write
→ They solve problems by simplifying, not adding complexity
→ They know the best code is no code at all

The best engineers aren't the ones who can build anything.
They're the ones who know when NOT to build.

Wisdom isn't knowing more.
It's knowing what to ignore.""",
        "engagement_score": 17000,
        "author": "Senior Engineer",
        "industry": "Software Engineering"
    },
    {
        "post_type": "insight",
        "content": """I've hired 200+ people.

Here's what separates the top 1% from everyone else:

It's not their resume.
It's not their skills.
It's not even their experience.

It's their response to: "What don't you know?"

Average candidates:
→ Try to hide their gaps
→ Pretend they know everything
→ Get defensive about weaknesses

Top 1% candidates:
→ Openly discuss what they're learning
→ Share how they fill knowledge gaps
→ See weaknesses as opportunities

The best people I've ever hired said:
"I don't know, but here's how I'd figure it out."

Confidence without arrogance.
Humility without weakness.

That's what separates good from great.""",
        "engagement_score": 19000,
        "author": "VP of Engineering",
        "industry": "Hiring"
    },

    # CONTRARIAN posts
    {
        "post_type": "contrarian",
        "content": """Unpopular opinion:

Work-life balance is a myth.

Here's what nobody tells you:

The most successful people I know don't have "balance."

They have seasons.

→ Seasons of grinding
→ Seasons of rest
→ Seasons of growth
→ Seasons of harvest

Trying to balance everything every day is exhausting.

Instead:

Sprint when it matters.
Rest when you can.
Know which season you're in.

Stop trying to give 100% to everything.
Start giving 100% to the right thing at the right time.

Balance isn't daily.
It's over a lifetime.""",
        "engagement_score": 13000,
        "author": "CEO",
        "industry": "Leadership"
    },
    {
        "post_type": "contrarian",
        "content": """Hot take that'll upset people:

You don't need a mentor.

You need to stop waiting for someone to save you.

Here's the truth:

→ The best mentors are books, podcasts, and people you'll never meet
→ Asking successful people for coffee is just wasting their time
→ Everything you need to learn is already free online

Instead of finding a mentor:

1. Study people from afar
2. Learn from their content
3. Implement what they teach
4. Get results
5. THEN reach out with proof

Want mentorship? Earn it.

Success leaves clues.
You don't need someone to hold your hand.
You need to pay attention.""",
        "engagement_score": 11000,
        "author": "Entrepreneur",
        "industry": "Business"
    },

    # PERSONAL ACHIEVEMENT posts
    {
        "post_type": "achievement",
        "content": """We just hit $1M ARR.

With a team of 3 people.
No funding.
No fancy office.
Just focus and persistence.

3 things that got us here:

1. We said NO to almost everything
   → 100 feature requests
   → We built 5 of them
   → Nailed those 5

2. We talked to customers daily
   → Not surveys
   → Real conversations
   → Built exactly what they needed

3. We moved fast
   → Launched in 6 weeks
   → Improved daily
   → Perfection is the enemy

To everyone building in silence:

Keep going.
Your breakthrough is closer than you think.""",
        "engagement_score": 21000,
        "author": "SaaS Founder",
        "industry": "Startups"
    },

    # DATA/STATS posts
    {
        "post_type": "data",
        "content": """I analyzed 10,000 LinkedIn posts to find what actually drives engagement.

The results surprised me:

📊 Top performing post types:
→ Personal stories: 2.3x more engagement
→ Contrarian takes: 2.1x more engagement
→ Listicles: 1.8x more engagement
→ How-tos: 1.6x more engagement

📏 Optimal post length:
→ Sweet spot: 150-200 words
→ Anything over 300 words: 40% drop in engagement
→ One-liners: Viral or invisible (no middle ground)

⏰ Best times to post:
→ Tuesday 9am: Peak engagement
→ Thursday 8am: Second best
→ Weekend posts: 60% less engagement

🎣 Hook performance:
→ "I quit my job...": 3x average engagement
→ "Unpopular opinion...": 2.5x average engagement
→ "Here's what nobody tells you...": 2.2x average engagement

💬 Comments > Likes:
→ Posts with 50+ comments get 10x more reach
→ Asking questions increases comments by 300%
→ Responding to every comment doubles your reach

The algorithm is simple:
Start conversations, not monologues.

Data doesn't lie.""",
        "engagement_score": 25000,
        "author": "LinkedIn Analyst",
        "industry": "Marketing"
    }
]


def seed_database():
    """Populate the database with sample LinkedIn posts."""
    init_db()
    db = SessionLocal()

    try:
        # Check if database already has posts
        existing_count = db.query(LinkedInPost).count()
        if existing_count > 0:
            print(f"Database already contains {existing_count} posts. Skipping seed.")
            return

        # Add sample posts
        for post_data in SAMPLE_POSTS:
            post = LinkedInPost(**post_data)
            db.add(post)

        db.commit()
        print(f"Successfully seeded database with {len(SAMPLE_POSTS)} posts!")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
