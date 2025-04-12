# present.py

import requests  # For API calls
class Player:
    def __init__(self, name, api_key):
        """
        Initialize a player with a name and API key.
        """
        self.info = {
            "name": name,
            "api_key": api_key,
            "color": None,  # Will be set to "white" or "black"
            "rating": None  # Can be fetched via API
        }

    def connect_to_api(self, endpoint):
        """
        Simulate connecting to an API using the player's API key.
        Returns a mock response (replace with real API call).
        """
        headers = {"Authorization": f"Bearer {self.info['api_key']}"}
        try:
            # Replace with real API call, e.g., to Lichess or Chess.com
            response = requests.get(endpoint, headers=headers)
            return response.json()
        except Exception as e:
            return f"API connection failed: {str(e)}"