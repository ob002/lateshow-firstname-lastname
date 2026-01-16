from app import app
from app_package.models import db, Episode, Guest, Appearance

def seed_database():
    with app.app_context():
        # Clear existing data
        db.session.query(Appearance).delete()
        db.session.query(Guest).delete()
        db.session.query(Episode).delete()
        db.session.commit()

        # Create episodes
        episode1 = Episode(date='1/11/99', number=1)
        episode2 = Episode(date='1/12/99', number=2)

        db.session.add(episode1)
        db.session.add(episode2)
        db.session.commit()

        # Create guests
        guest1 = Guest(name='Michael J. Fox', occupation='actor')
        guest2 = Guest(name='Sandra Bernhard', occupation='Comedian')
        guest3 = Guest(name='Tracey Ullman', occupation='television actress')

        db.session.add(guest1)
        db.session.add(guest2)
        db.session.add(guest3)
        db.session.commit()

        # Create appearances
        appearance1 = Appearance(rating=4, episode_id=episode1.id, guest_id=guest1.id)
        appearance2 = Appearance(rating=5, episode_id=episode2.id, guest_id=guest3.id)

        db.session.add(appearance1)
        db.session.add(appearance2)
        db.session.commit()

        print("Database seeded successfully!")
        print(f"Created {Episode.query.count()} episodes")
        print(f"Created {Guest.query.count()} guests")
        print(f"Created {Appearance.query.count()} appearances")

if __name__ == '__main__':
    seed_database()
if __name__ == '__main__':
    seed_database()
