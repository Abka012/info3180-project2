import argparse
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import bcrypt, create_app, db
from app.models import Bookmark, Like, Match, Message, Notification, Profile, User

random.seed(42)


def seed(screenshot_mode=False):
    instance_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "instance"
    )
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
        print(f"Created instance folder: {instance_dir}")

    app = create_app()

    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Seeding database...")

        users = []

        # 1. CREATE 15 REALISTIC USERS
        for i in range(1, 16):
            user = User(
                email=f"user{i}@test.com",
                username=f"user{i}",
                password_hash=bcrypt.generate_password_hash("password123").decode(
                    "utf-8"
                ),
                is_verified=(i <= 12),  # 12 verified, 3 unverified for edge cases
            )
            db.session.add(user)
            users.append(user)

        db.session.commit()

        # 2. CREATE DETAILED PROFILES
        profiles_data = [
            {
                "name": "Alex Chen",
                "age": 28,
                "bio": "Software engineer who loves hiking, photography, and trying new restaurants. Looking for meaningful connections!",
                "interests": ["coding", "hiking", "photography", "food"],
                "gender": "male",
            },
            {
                "name": "Jordan Smith",
                "age": 25,
                "bio": "Yoga instructor and travel enthusiast. I've visited 30 countries and counting! 🧘‍♀️✈️",
                "interests": ["yoga", "travel", "wellness", "meditation"],
                "gender": "female",
            },
            {
                "name": "Taylor Kim",
                "age": 30,
                "bio": "Music producer and part-time chef. Ask me about my famous kimchi fried rice!",
                "interests": ["music", "cooking", "art", "concerts"],
                "gender": "non-binary",
            },
            {
                "name": "Chris Johnson",
                "age": 32,
                "bio": "Marathon runner and coffee addict. PR: 3:15. Let's grab a brew (coffee or beer)! ☕🏃",
                "interests": ["running", "fitness", "coffee", "sports"],
                "gender": "male",
            },
            {
                "name": "Sam Rivera",
                "age": 27,
                "bio": "Graphic designer with a passion for street art. My dog Bailey is my co-pilot. 🐕🎨",
                "interests": ["art", "design", "dogs", "urban-exploration"],
                "gender": "female",
            },
            {
                "name": "Jamie Lee",
                "age": 29,
                "bio": "Environmental scientist working on climate solutions. Weekend gardener and compost enthusiast! 🌱🌍",
                "interests": ["science", "gardening", "sustainability", "nature"],
                "gender": "non-binary",
            },
            {
                "name": "Casey Brown",
                "age": 26,
                "bio": "Indie game developer and board game collector. Own over 200 games! 🎲🎮 Looking for my player 2.",
                "interests": ["gaming", "coding", "board-games", "tech"],
                "gender": "male",
            },
            {
                "name": "Drew Wilson",
                "age": 31,
                "bio": "Sous chef at a French bistro. Can make a killer coq au vin. Let's cook together! 👨‍🍳🍷",
                "interests": ["cooking", "wine", "food", "culinary"],
                "gender": "male",
            },
            {
                "name": "Morgan Taylor",
                "age": 24,
                "bio": "Journalism student and aspiring travel writer. Currently planning a solo trip to Japan! 🇯🇵📝",
                "interests": ["writing", "travel", "reading", "culture"],
                "gender": "female",
            },
            {
                "name": "Riley Martinez",
                "age": 33,
                "bio": "Architect who designs sustainable homes. Love mid-century modern design. Let's talk Frank Lloyd Wright! 🏡📐",
                "interests": ["architecture", "design", "sustainability", "history"],
                "gender": "non-binary",
            },
            {
                "name": "Avery Thompson",
                "age": 28,
                "bio": "Veterinarian who loves all animals. Have 2 cats, 1 dog, and a bearded dragon! 🐱🐶🦎",
                "interests": ["animals", "veterinary", "nature", "pets"],
                "gender": "female",
            },
            {
                "name": "Quinn Davis",
                "age": 30,
                "bio": "Data scientist with a creative side. Paint in my free time. Check out my gallery! 📊🎨",
                "interests": ["data-science", "art", "painting", "analytics"],
                "gender": "male",
            },
            {
                "name": "Emery Garcia",
                "age": 26,
                "bio": "Fashion design student with a love for vintage finds. Thrift shopping is my cardio! 👗✨",
                "interests": ["fashion", "design", "vintage", "shopping"],
                "gender": "non-binary",
            },
            {
                "name": "Skyler Nguyen",
                "age": 29,
                "bio": "Physical therapist and rock climber. Bouldering V5 and working on V6! 🧗‍♀️💪",
                "interests": ["climbing", "fitness", "health", "outdoors"],
                "gender": "female",
            },
            {
                "name": "Dakota Lewis",
                "age": 31,
                "bio": "High school teacher and trivia night champion. My specialty: 90s pop culture! 🏫🎤 Ask me anything about NSYNC.",
                "interests": ["education", "trivia", "music", "pop-culture"],
                "gender": "male",
            },
        ]

        for i, user in enumerate(users):
            if i < len(profiles_data):
                data = profiles_data[i]
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
                )
            else:
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

        db.session.commit()

        # ===== SCREENSHOT MODE: ALEX-FOCUSED DATA =====
        if screenshot_mode:
            print("📸 Screenshot mode: Creating Alex-focused data...")

            alex = users[0]  # Alex Chen (user1)
            jordan = users[1]  # Jordan Smith (user2)
            taylor = users[2]  # Taylor Kim (user3)

            # 🔥 Create MATCHES: Alex ↔ Jordan, Alex ↔ Taylor
            match1 = Match(user1_id=alex.user_id, user2_id=jordan.user_id)
            match2 = Match(user1_id=alex.user_id, user2_id=taylor.user_id)
            db.session.add_all([match1, match2])

            # ❤️ Create mutual LIKES (required for matches to show)
            mutual_likes = [
                Like(
                    from_user_id=alex.user_id, to_user_id=jordan.user_id, status="liked"
                ),
                Like(
                    from_user_id=jordan.user_id, to_user_id=alex.user_id, status="liked"
                ),
                Like(
                    from_user_id=alex.user_id, to_user_id=taylor.user_id, status="liked"
                ),
                Like(
                    from_user_id=taylor.user_id, to_user_id=alex.user_id, status="liked"
                ),
            ]
            db.session.add_all(mutual_likes)

            # 💬 Create REALISTIC MESSAGE CONVERSATIONS
            alex_jordan_msgs = [
                {
                    "sender": alex,
                    "receiver": jordan,
                    "content": "Hey Jordan! I saw you've traveled to 30 countries — that's amazing! 🌍 What's your favorite place so far?",
                },
                {
                    "sender": jordan,
                    "receiver": alex,
                    "content": "Thanks Alex! 😊 Probably Bali — the culture and nature are incredible. Have you traveled much?",
                },
                {
                    "sender": alex,
                    "receiver": jordan,
                    "content": "I've done some hiking trips in the Rockies! Would love to hear more about your yoga journey sometime 🧘",
                },
                {
                    "sender": jordan,
                    "receiver": alex,
                    "content": "I'd love that! Maybe we could grab coffee and swap travel stories? ☕",
                },
            ]

            alex_taylor_msgs = [
                {
                    "sender": alex,
                    "receiver": taylor,
                    "content": "Hey Taylor! Your bio made me laugh — kimchi fried rice sounds delicious! 🍳 Do you have a recipe?",
                },
                {
                    "sender": taylor,
                    "receiver": alex,
                    "content": "Haha thanks! I might share it... if you tell me about your photography hobby first 📸",
                },
                {
                    "sender": alex,
                    "receiver": taylor,
                    "content": "Deal! I mostly shoot landscapes. Here's one from my last hike: [photo]",
                },
                {
                    "sender": taylor,
                    "receiver": alex,
                    "content": "Wow, that's stunning! You're talented 😍",
                },
            ]

            for msg in alex_jordan_msgs + alex_taylor_msgs:
                message = Message(
                    sender_id=msg["sender"].user_id,
                    receiver_id=msg["receiver"].user_id,
                    content=msg["content"],
                )
                db.session.add(message)

            # ⭐ Create BOOKMARKS (favorites)
            bookmarks = [
                Bookmark(user_id=alex.user_id, bookmarked_user_id=jordan.user_id),
                Bookmark(user_id=alex.user_id, bookmarked_user_id=taylor.user_id),
                Bookmark(user_id=jordan.user_id, bookmarked_user_id=alex.user_id),
                Bookmark(user_id=taylor.user_id, bookmarked_user_id=alex.user_id),
            ]
            db.session.add_all(bookmarks)

            # 🔔 Create NOTIFICATIONS for Alex
            notifications = [
                Notification(
                    user_id=alex.user_id,
                    type="match",
                    message=f"You matched with {Profile.query.get(jordan.user_id).name}!",
                    from_user_id=jordan.user_id,
                ),
                Notification(
                    user_id=alex.user_id,
                    type="match",
                    message=f"You matched with {Profile.query.get(taylor.user_id).name}!",
                    from_user_id=taylor.user_id,
                ),
                Notification(
                    user_id=alex.user_id,
                    type="message",
                    message=f"{Profile.query.get(jordan.user_id).name} sent you a message",
                    from_user_id=jordan.user_id,
                ),
            ]
            db.session.add_all(notifications)

            db.session.commit()

            print("✅ Screenshot mode seeding complete!")
            print(
                f"   • Alex has {Match.query.filter((Match.user1_id == alex.user_id) | (Match.user2_id == alex.user_id)).count()} matches"
            )
            print(
                f"   • Alex has {Message.query.filter((Message.sender_id == alex.user_id) | (Message.receiver_id == alex.user_id)).count()} messages"
            )
            print(
                f"   • Alex has {Bookmark.query.filter_by(user_id=alex.user_id).count()} favorites"
            )
            return

        # ===== NORMAL MODE: FULL RANDOM DATA (UNCHANGED) =====
        # 3. CREATE LIKES (mutual for matches)
        likes = []
        for i, user in enumerate(users):
            others = [u for u in users if u.user_id != user.user_id]
            liked_users = random.sample(others, k=min(5, len(others)))
            for target in liked_users:
                like = Like(
                    from_user_id=user.user_id, to_user_id=target.user_id, status="liked"
                )
                db.session.add(like)
                likes.append((user.user_id, target.user_id))
        db.session.commit()

        # 4. CREATE MATCHES (mutual likes)
        matches_created = set()
        for u1, u2 in likes:
            if (u2, u1) in likes and (u1, u2) not in matches_created:
                match = Match(user1_id=min(u1, u2), user2_id=max(u1, u2))
                db.session.add(match)
                matches_created.add((u1, u2))
                matches_created.add((u2, u1))
        db.session.commit()

        # 5. CREATE REALISTIC MESSAGES
        message_templates = [
            "Hey! How's it going? 😊",
            "I saw we matched! Tell me about yourself.",
            "What's your favorite thing to do on weekends?",
            "I love your profile pic! Is that your hobby?",
            "Have you been to any good restaurants lately?",
            "What kind of music are you into?",
            "Do you have any travel plans coming up?",
            "I'm a big fan of [interest]. How about you?",
            "Would you like to grab coffee sometime?",
            "What's the most interesting place you've visited?",
        ]

        matches = Match.query.all()
        for match in matches:
            for _ in range(random.randint(5, 15)):
                sender = random.choice([match.user1_id, match.user2_id])
                receiver = (
                    match.user2_id if sender == match.user1_id else match.user1_id
                )
                content = random.choice(message_templates)
                message = Message(
                    sender_id=sender, receiver_id=receiver, content=content
                )
                db.session.add(message)
        db.session.commit()

        # 6. CREATE NOTIFICATIONS
        for match in matches[:8]:
            notification = Notification(
                user_id=match.user1_id,
                type="match",
                message=f"You matched with {Profile.query.filter_by(user_id=match.user2_id).first().name}!",
                from_user_id=match.user2_id,
            )
            db.session.add(notification)
        db.session.commit()

        # 7. CREATE BOOKMARKS
        for user in users[:10]:
            others = [u for u in users if u.user_id != user.user_id]
            bookmarked = random.choice(others)
            bookmark = Bookmark(
                user_id=user.user_id, bookmarked_user_id=bookmarked.user_id
            )
            db.session.add(bookmark)
        db.session.commit()

        # Print summary
        print("\n" + "=" * 50)
        print("DATABASE SEEDING COMPLETE - SUMMARY")
        print("=" * 50)
        print(f"\n📊 Users: {User.query.count()}")
        print(f"👤 Profiles: {Profile.query.count()}")
        print(f"❤️  Likes: {Like.query.count()}")
        print(f"🔥 Matches: {Match.query.count()}")
        print(f"💬 Messages: {Message.query.count()}")
        print(f"🔔 Notifications: {Notification.query.count()}")
        print(f"📌 Bookmarks: {Bookmark.query.count()}")
        print("\n" + "=" * 50)
        print("✅ Database seeded successfully!")
        print("=" * 50)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed the database")
    parser.add_argument(
        "--screenshot-mode",
        action="store_true",
        help="Create minimal data for quick screenshot testing",
    )
    args = parser.parse_args()
    seed(screenshot_mode=args.screenshot_mode)
