from django.core.management.base import BaseCommand
from django.utils import timezone
from membership.models import GymMember, GymInout
from membership.zk_utils import get_connection

class Command(BaseCommand):
    help = "Pull attendance logs from ZKTeco device and sync with GymInout table"

    def handle(self, *args, **kwargs):
        try:
            conn = get_connection()
            self.stdout.write(self.style.SUCCESS("Connected to device"))

            logs = conn.get_attendance()
            for log in logs:
                user_id = str(log.user_id)  # device user_id
                punch_time = log.timestamp

                try:
                    member = GymMember.objects.get(members_reg_number=user_id)
                except GymMember.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"No member linked for device user {user_id}"))
                    continue

                # Check if already has in_time today
                inout, created = GymInout.objects.get_or_create(
                    member_id=member.id,
                    member_reg_code=member.members_reg_number,
                    in_time__date=punch_time.date(),
                    defaults={"in_time": punch_time},
                )

                if not created:
                    # If already exists, update out_time
                    if not inout.out_time or punch_time > inout.out_time:
                        inout.out_time = punch_time
                        inout.save()

                self.stdout.write(self.style.SUCCESS(
                    f"Synced log for {member.first_name} at {punch_time}"
                ))

            conn.disconnect()
            self.stdout.write(self.style.SUCCESS("Done syncing attendance"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
