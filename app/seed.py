import logging
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Bookmark, Like, Match, Message, Notification, Profile, User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

random.seed(42)


def seed(screenshot_mode=False):
    logger.info("=" * 60)
    logger.info("DATABASE SEEDING STARTED")
    logger.info("=" * 60)

    instance_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "instance"
    )
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
        logger.info(f"Created instance folder: {instance_dir}")

    app = create_app()

    with app.app_context():
        logger.info("[SEED] Dropping all tables...")
        db.drop_all()
        logger.info("[SEED] Creating all tables...")
        db.create_all()
        logger.info("[SEED] Database tables created successfully")

        users = []

        logger.info("[SEED] Creating 5 seeded users...")
        for i in range(1, 6):
            email = f"user{i}@test.com"
            username = f"user{i}"

            logger.info(f"[SEED] Creating user {i}: email={email}, username={username}")

            user = User(
                email=email,
                username=username,
                is_verified=True,
            )
            user.set_password("password123")
            db.session.add(user)
            users.append(user)

            logger.info(f"[SEED] User {i} added to session, now committing...")
            db.session.commit()
            logger.info(
                f"[SEED] SUCCESS - User {i} committed to database with user_id={user.user_id}"
            )

        logger.info("[SEED] All 5 users created and committed")

        profiles_data = [
            {
                "name": "Alex Chen",
                "age": 28,
                "bio": "Software engineer who loves hiking, photography, and trying new restaurants. Looking for meaningful connections!",
                "interests": ["coding", "hiking", "photography", "food"],
                "gender": "male",
                "occupation": "Software Engineer",
            },
            {
                "name": "Jordan Smith",
                "age": 25,
                "bio": "Yoga instructor and travel enthusiast. I've visited 30 countries and counting! 🧘‍♀️✈️",
                "interests": ["yoga", "travel", "wellness", "meditation"],
                "gender": "female",
                "occupation": "Yoga Instructor",
            },
            {
                "name": "Taylor Kim",
                "age": 30,
                "bio": "Music producer and part-time chef. Ask me about my famous kimchi fried rice!",
                "interests": ["music", "cooking", "art", "concerts"],
                "gender": "non-binary",
                "occupation": "Music Producer",
            },
            {
                "name": "Chris Johnson",
                "age": 32,
                "bio": "Marathon runner and coffee addict. PR: 3:15. Let's grab a brew (coffee or beer)! ☕🏃",
                "interests": ["running", "fitness", "coffee", "sports"],
                "gender": "male",
                "occupation": "Fitness Coach",
            },
            {
                "name": "Sam Rivera",
                "age": 27,
                "bio": "Graphic designer with a passion for street art. My dog Bailey is my co-pilot. 🐕🎨",
                "interests": ["art", "design", "dogs", "urban-exploration"],
                "gender": "female",
                "occupation": "Graphic Designer",
            },
        ]

        logger.info("[SEED] Creating profiles for all users...")
        for i, user in enumerate(users):
            if i < len(profiles_data):
                data = profiles_data[i]
                logger.info(
                    f"[SEED] Creating profile for user_id={user.user_id}, name={data['name']}"
                )

                profile = Profile(
                    user_id=user.user_id,
                    name=data["name"],
                    age=data["age"],
                    bio=data["bio"],
                    interests=data["interests"],
                    gender=data["gender"],
                    gender_preference="all",
                    relationship_goal=random.choice(
                        ["dating", "friendship", "long-term"]
                    ),
                    occupation=data.get("occupation", ""),
                )
            else:
                logger.info(
                    f"[SEED] Creating random profile for user_id={user.user_id}"
                )
                profile = Profile(
                    user_id=user.user_id,
                    name=f"User{i + 1}",
                    age=random.randint(18, 40),
                    bio=f"Hi, I'm User{i + 1}!",
                    interests=random.sample(
                        ["music", "sports", "coding", "travel", "fitness", "gaming"],
                        k=3,
                    ),
                    gender=random.choice(["male", "female", "non-binary"]),
                    gender_preference="all",
                    relationship_goal="dating",
                )
            db.session.add(profile)

        logger.info("[SEED] Committing all profiles...")
        db.session.commit()
        logger.info("[SEED] All profiles committed successfully")

        match_pairs = [(1, 2), (1, 3), (2, 4), (3, 5), (4, 5)]

        conversation_templates = {
            (1, 2): [
                (
                    "Hey Jordan! I saw you've traveled to 30 countries — that's amazing! 🌍 What's your favorite place so far?"
                ),
                (
                    "Thanks Alex! 😊 Probably Bali — the culture and nature are incredible. Have you traveled much?"
                ),
                (
                    "I've done some hiking trips in the Rockies! Would love to hear more about your yoga journey sometime 🧘"
                ),
                (
                    "I'd love that! Maybe we could grab coffee and swap travel stories? ☕"
                ),
            ],
            (1, 3): [
                (
                    "Hey Taylor! Your bio made me laugh — kimchi fried rice sounds delicious! 🍳 Do you have a recipe?"
                ),
                (
                    "Haha thanks! I might share it... if you tell me about your photography hobby first 📸"
                ),
                (
                    "Deal! I mostly shoot landscapes. Here's one from my last hike: [photo]"
                ),
                ("Wow, that's stunning! You're talented 😍"),
            ],
            (2, 4): [
                (
                    "Hey Chris! Your marathon times are impressive! What's your training routine?"
                ),
                ("Thanks Jordan! I run 5 days a week. What yoga style do you teach?"),
                (
                    "I teach vinyasa flow mostly. Would love to try running sometime! 🧘‍♀️🏃"
                ),
                (
                    "Let's do it! There's a great 5k trail near here. We could go together!"
                ),
            ],
            (3, 5): [
                ("Hey Sam! Love your street art passion. What's your favorite style?"),
                (
                    "Thanks Taylor! I'm really into muralism and graffiti art. Do you produce music?"
                ),
                ("Yeah! I make electronic music. We should collaborate sometime 🎵🎨"),
                ("That sounds amazing! Let's definitely do that."),
            ],
            (4, 5): [
                (
                    "Hey Sam! Your graphic design work is really cool. What's your design philosophy?"
                ),
                (
                    "Thanks Chris! I believe good design should be accessible and authentic. How do you stay motivated for marathons?"
                ),
                (
                    "I set small goals and celebrate each milestone. Same approach to anything in life!"
                ),
                ("Love that mindset! We should grab coffee and talk more ☕"),
            ],
        }

        logger.info(
            "[SEED] Creating matches, likes, messages, bookmarks, and notifications..."
        )

        for u1, u2 in match_pairs:
            user1 = users[u1 - 1]
            user2 = users[u2 - 1]
            logger.info(f"[SEED] Creating mutual data for user pair: {u1} <-> {u2}")

            like1 = Like(
                from_user_id=user1.user_id, to_user_id=user2.user_id, status="liked"
            )
            like2 = Like(
                from_user_id=user2.user_id, to_user_id=user1.user_id, status="liked"
            )
            db.session.add_all([like1, like2])

            match = Match(user1_id=user1.user_id, user2_id=user2.user_id)
            db.session.add(match)

            key = (u1, u2) if u1 < u2 else (u2, u1)
            messages = conversation_templates.get(
                key,
                [
                    "Hey! How's it going? 😊",
                    "I saw we matched! Tell me about yourself.",
                    "What's your favorite thing to do on weekends?",
                    "Would you like to grab coffee sometime?",
                ],
            )

            for idx, content in enumerate(messages):
                sender = user1 if idx % 2 == 0 else user2
                receiver = user2 if idx % 2 == 0 else user1
                message = Message(
                    sender_id=sender.user_id,
                    receiver_id=receiver.user_id,
                    content=content,
                )
                db.session.add(message)

            bookmark1 = Bookmark(
                user_id=user1.user_id, bookmarked_user_id=user2.user_id
            )
            bookmark2 = Bookmark(
                user_id=user2.user_id, bookmarked_user_id=user1.user_id
            )
            db.session.add_all([bookmark1, bookmark2])

            profile1 = Profile.query.filter_by(user_id=user1.user_id).first()
            profile2 = Profile.query.filter_by(user_id=user2.user_id).first()

            notif1 = Notification(
                user_id=user1.user_id,
                type="match",
                message=f"You matched with {profile2.name}!",
                from_user_id=user2.user_id,
            )
            notif2 = Notification(
                user_id=user2.user_id,
                type="match",
                message=f"You matched with {profile1.name}!",
                from_user_id=user1.user_id,
            )
            db.session.add_all([notif1, notif2])

        logger.info("[SEED] Committing all relationship data...")
        db.session.commit()
        logger.info("[SEED] All relationship data committed successfully")

        user_count = User.query.count()
        profile_count = Profile.query.count()
        like_count = Like.query.count()
        match_count = Match.query.count()
        message_count = Message.query.count()
        notification_count = Notification.query.count()
        bookmark_count = Bookmark.query.count()

        logger.info("\n" + "=" * 50)
        logger.info("DATABASE SEEDING COMPLETE - SUMMARY")
        logger.info("=" * 50)
        logger.info(f"Users: {user_count}")
        logger.info(f"Profiles: {profile_count}")
        logger.info(f"Likes: {like_count}")
        logger.info(f"Matches: {match_count}")
        logger.info(f"Messages: {message_count}")
        logger.info(f"Notifications: {notification_count}")
        logger.info(f"Bookmarks: {bookmark_count}")
        logger.info("\n" + "=" * 50)
        logger.info("Seeded users login credentials:")
        logger.info("  Email: user1@test.com - user5@test.com")
        logger.info("  Password: password123")
        logger.info("=" * 50)

        return {
            "users": user_count,
            "profiles": profile_count,
            "likes": like_count,
            "matches": match_count,
            "messages": message_count,
            "notifications": notification_count,
            "bookmarks": bookmark_count,
        }


if __name__ == "__main__":
    result = seed()
    print(f"\nSeeding complete: {result}")
