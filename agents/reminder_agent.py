import pandas as pd

class ReminderAgent:
    def __init__(self, csv_path="data/daily_reminders.csv"):
        self.csv_path = csv_path

    def get_reminders(self, user_id=None, limit=10):
        df = pd.read_csv(self.csv_path)
        df.columns = df.columns.str.strip()

        if user_id:
            df = df[df["Device-ID/User-ID"] == user_id]
        

        # df["Scheduled Time"] = pd.to_datetime(
        #     df["Scheduled Time"],
        #     format="%Y-%m-%d %H:%M:%S",
        #     errors="coerce"
        #     )

        df["Scheduled Time"] = pd.to_datetime(df["Scheduled Time"], errors='coerce')
        df = df.sort_values(by="Scheduled Time", ascending=False)

        reminders = []
        for _, row in df.iterrows():
            reminder_type = row.get("Reminder Type", "").strip()
            time = row["Scheduled Time"]
            if reminder_type and pd.notnull(time):
                reminders.append(f"⏰ {reminder_type} — {time.strftime('%Y-%m-%d %H:%M:%S')}")

        return reminders[:limit]
