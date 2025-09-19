from django.core.management.base import BaseCommand
from django.utils import timezone
from membership.models import GymMember, GymInout
from membership.zk_utils import get_connection
from django.utils.timezone import make_aware, is_naive


class Command(BaseCommand):
    help = "Pull NEW attendance logs from ZKTeco device and sync with GymInout table"

    def handle(self, *args, **kwargs):
        try:
            conn = get_connection()
            self.stdout.write(self.style.SUCCESS("Connected to device"))

            # Get last synced punch time from DB
            last_inout = GymInout.objects.order_by("-in_time").first()
            last_sync_time = last_inout.in_time if last_inout else None

            logs = conn.get_attendance()

            if last_sync_time:
                logs = [log for log in logs if log.timestamp > last_sync_time]

            if not logs:
                self.stdout.write(self.style.WARNING("No new logs to sync"))
                conn.disconnect()
                return

            for log in logs:
                user_id = str(log.user_id)
                punch_time = log.timestamp
                if is_naive(punch_time):
                    punch_time = make_aware(punch_time)

                try:
                    member = GymMember.objects.get(members_reg_number=user_id)
                except GymMember.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"No member linked for device user {user_id}"))
                    continue

                punch_date = punch_time.date()

                inout = GymInout.objects.filter(
                    member_id=member.id,
                    in_time__date=punch_date
                ).first()

                if inout:
                    if punch_time < inout.in_time:
                        inout.in_time = punch_time
                    if not inout.out_time or punch_time > inout.out_time:
                        inout.out_time = punch_time
                    inout.save()
                else:
                    GymInout.objects.create(
                        member_id=member.id,
                        member_reg_code=member.members_reg_number,
                        in_time=punch_time
                    )

                self.stdout.write(self.style.SUCCESS(
                    f"Synced log for {member.first_name} at {punch_time}"
                ))

            # ✅ Clear device logs after successful sync
            conn.clear_attendance()
            self.stdout.write(self.style.SUCCESS("Cleared logs from device"))

            conn.disconnect()
            self.stdout.write(self.style.SUCCESS("Done syncing NEW attendance"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
