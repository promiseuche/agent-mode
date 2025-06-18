from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from bson import ObjectId
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activity, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        try:
            # Create users
            users_data = [
                {"username": "thundergod", "email": "thundergod@mhigh.edu", "password": "thundergodpassword"},
                {"username": "metalgeek", "email": "metalgeek@mhigh.edu", "password": "metalgeekpassword"},
                {"username": "zerocool", "email": "zerocool@mhigh.edu", "password": "zerocoolpassword"},
                {"username": "crashoverride", "email": "crashoverride@hmhigh.edu", "password": "crashoverridepassword"},
                {"username": "sleeptoken", "email": "sleeptoken@mhigh.edu", "password": "sleeptokenpassword"},
            ]
            for user_data in users_data:
                user, created = User.objects.update_or_create(username=user_data["username"], defaults=user_data)
                logger.info(f"User {'created' if created else 'updated'}: {user.username}")

            # Create team
            team, created = Team.objects.update_or_create(name="Blue Team")
            team.members.set(User.objects.all())
            logger.info(f"Team {'created' if created else 'updated'}: {team.name}")

            # Create activities
            activities_data = [
                {"user": User.objects.get(username="thundergod"), "activity_type": "Cycling", "duration": timedelta(hours=1)},
                {"user": User.objects.get(username="metalgeek"), "activity_type": "Crossfit", "duration": timedelta(hours=2)},
                {"user": User.objects.get(username="zerocool"), "activity_type": "Running", "duration": timedelta(hours=1, minutes=30)},
                {"user": User.objects.get(username="crashoverride"), "activity_type": "Strength", "duration": timedelta(minutes=30)},
                {"user": User.objects.get(username="sleeptoken"), "activity_type": "Swimming", "duration": timedelta(hours=1, minutes=15)},
            ]
            for activity_data in activities_data:
                activity, created = Activity.objects.update_or_create(user=activity_data["user"], activity_type=activity_data["activity_type"], defaults=activity_data)
                logger.info(f"Activity {'created' if created else 'updated'}: {activity.activity_type} for user {activity.user.username}")

            # Create leaderboard entries
            leaderboard_data = [
                {"user": User.objects.get(username="thundergod"), "score": 100},
                {"user": User.objects.get(username="metalgeek"), "score": 90},
                {"user": User.objects.get(username="zerocool"), "score": 95},
                {"user": User.objects.get(username="crashoverride"), "score": 85},
                {"user": User.objects.get(username="sleeptoken"), "score": 80},
            ]
            for entry_data in leaderboard_data:
                entry, created = Leaderboard.objects.update_or_create(user=entry_data["user"], defaults=entry_data)
                logger.info(f"Leaderboard entry {'created' if created else 'updated'}: {entry.score} for user {entry.user.username}")

            # Create workouts
            workouts_data = [
                {"name": "Cycling Training", "description": "Training for a road cycling event"},
                {"name": "Crossfit", "description": "Training for a crossfit competition"},
                {"name": "Running Training", "description": "Training for a marathon"},
                {"name": "Strength Training", "description": "Training for strength"},
                {"name": "Swimming Training", "description": "Training for a swimming competition"},
            ]
            for workout_data in workouts_data:
                workout, created = Workout.objects.update_or_create(name=workout_data["name"], defaults=workout_data)
                logger.info(f"Workout {'created' if created else 'updated'}: {workout.name}")

            self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
        except Exception as e:
            logger.error(f"Error populating database: {e}")
            raise
