from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient
from datetime import timedelta
from bson import ObjectId

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activity, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting database population...')

        # Connect to MongoDB
        try:
            client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
            db = client[settings.DATABASES['default']['NAME']]
            self.stdout.write('Connected to MongoDB successfully.')
        except Exception as e:
            self.stderr.write(f'Error connecting to MongoDB: {e}')
            return

        # Drop existing collections
        try:
            db.users.drop()
            db.teams.drop()
            db.activity.drop()
            db.leaderboard.drop()
            db.workouts.drop()
            self.stdout.write('Dropped existing collections successfully.')
        except Exception as e:
            self.stderr.write(f'Error dropping collections: {e}')
            return

        # Create users
        try:
            users = [
                User(_id=ObjectId(), username='thundergod', email='thundergod@mhigh.edu', password='thundergodpassword'),
                User(_id=ObjectId(), username='metalgeek', email='metalgeek@mhigh.edu', password='metalgeekpassword'),
                User(_id=ObjectId(), username='zerocool', email='zerocool@mhigh.edu', password='zerocoolpassword'),
                User(_id=ObjectId(), username='crashoverride', email='crashoverride@hmhigh.edu', password='crashoverridepassword'),
                User(_id=ObjectId(), username='sleeptoken', email='sleeptoken@mhigh.edu', password='sleeptokenpassword'),
            ]
            User.objects.bulk_create(users)
            self.stdout.write('Created users successfully.')
        except Exception as e:
            self.stderr.write(f'Error creating users: {e}')
            return

        # Create teams
        try:
            team = Team(_id=ObjectId(), name='Blue Team')
            team.save()
            team.members.add(*users)
            self.stdout.write('Created team successfully.')
        except Exception as e:
            self.stderr.write(f'Error creating team: {e}')
            return

        # Create activities
        try:
            activities = [
                Activity(_id=ObjectId(), user=users[0], activity_type='Cycling', duration=timedelta(hours=1)),
                Activity(_id=ObjectId(), user=users[1], activity_type='Crossfit', duration=timedelta(hours=2)),
                Activity(_id=ObjectId(), user=users[2], activity_type='Running', duration=timedelta(hours=1, minutes=30)),
                Activity(_id=ObjectId(), user=users[3], activity_type='Strength', duration=timedelta(minutes=30)),
                Activity(_id=ObjectId(), user=users[4], activity_type='Swimming', duration=timedelta(hours=1, minutes=15)),
            ]
            Activity.objects.bulk_create(activities)
            self.stdout.write('Created activities successfully.')
        except Exception as e:
            self.stderr.write(f'Error creating activities: {e}')
            return

        # Create leaderboard entries
        try:
            leaderboard_entries = [
                Leaderboard(_id=ObjectId(), user=users[0], score=100),
                Leaderboard(_id=ObjectId(), user=users[1], score=90),
                Leaderboard(_id=ObjectId(), user=users[2], score=95),
                Leaderboard(_id=ObjectId(), user=users[3], score=85),
                Leaderboard(_id=ObjectId(), user=users[4], score=80),
            ]
            Leaderboard.objects.bulk_create(leaderboard_entries)
            self.stdout.write('Created leaderboard entries successfully.')
        except Exception as e:
            self.stderr.write(f'Error creating leaderboard entries: {e}')
            return

        # Create workouts
        try:
            workouts = [
                Workout(_id=ObjectId(), name='Cycling Training', description='Training for a road cycling event'),
                Workout(_id=ObjectId(), name='Crossfit', description='Training for a crossfit competition'),
                Workout(_id=ObjectId(), name='Running Training', description='Training for a marathon'),
                Workout(_id=ObjectId(), name='Strength Training', description='Training for strength'),
                Workout(_id=ObjectId(), name='Swimming Training', description='Training for a swimming competition'),
            ]
            Workout.objects.bulk_create(workouts)
            self.stdout.write('Created workouts successfully.')
        except Exception as e:
            self.stderr.write(f'Error creating workouts: {e}')
            return

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
