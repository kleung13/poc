import requests, re
from datetime import datetime

class Calendar:
    def __init__(self, api_key, base_url):
        """
        Initialize the Calendar with the API URL.
        """
        self.api_key = api_key
        self.base_url = base_url

    def fetch_workouts(self):
        """
        Fetch workouts from the API endpoint.
        """
        try:
            # response = requests.get(self.api_url)
            response = requests.get(self.base_url, auth=("API_KEY", self.api_key))
            response.raise_for_status()
            return response.json()  # Assuming the response is a JSON array
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return []

    def parse_description(self, description):
        match = re.search(r"TSS (\d+), IF ([\d.]+), kJ\(Cal\) (\d+)", description)
        if match:
            tss = int(match.group(1))
            intensity_factor = float(match.group(2))
            kilojoules = int(match.group(3))
            return tss, intensity_factor, kilojoules
        return None, None, None
    
    def filter_workouts_by_date(self, workouts, start_date, end_date):
        """
        Filter workouts within the given date range.
        """
        filtered = []
        for workout in workouts:
            # Parse workout dates
            workout_start = datetime.fromisoformat(workout["start_date_local"])
            workout_end = datetime.fromisoformat(workout["end_date_local"])

            # Check if the workout is within the range
            if workout_start >= start_date and workout_end <= end_date:
                filtered.append(workout)
        return filtered

    def get_workouts(self, start_date, end_date):
        """
        Get workouts within the given date range.
        """
        # Convert string dates to datetime objects
        start_date = datetime.fromisoformat(start_date)
        end_date = datetime.fromisoformat(end_date)

        # Fetch all workouts
        workouts = self.fetch_workouts()

        # Filter workouts by date
        return self.filter_workouts_by_date(workouts, start_date, end_date)