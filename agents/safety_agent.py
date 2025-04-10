import pandas as pd

class SafetyAgent:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.df.columns = self.df.columns.str.strip()

    def get_alerts(self, user_id=None):
        df = self.df
        if user_id:
            df = df[df["Device-ID/User-ID"] == user_id]

        df = df[df["Alert Triggered (Yes/No)"] == "Yes"]

        alerts = []
        for _, row in df.iterrows():
            alerts.append({
                "user": row["Device-ID/User-ID"],
                "issue": f"Fall Detected: {row['Fall Detected (Yes/No)']}, Location: {row['Location']}",
                "details": f"Impact Force: {row['Impact Force Level']}, Inactivity: {row['Post-Fall Inactivity Duration (Seconds)']}s at {row['Timestamp']}"
            })

        return alerts
