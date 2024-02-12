import pandas as pd
import random
from datetime import datetime, timedelta
import json

# Read community_fisherman_data CSV file
def read_community_fisherman_data():
    community_fisherman_data = pd.read_csv('community_fisherman_data.csv')

    # Create a list to store fishermen data
    fishermen = []

    # Extract the last column name
    last_column_name = community_fisherman_data.columns[-1]

    # Convert the data into tuples of (fisherman_name, allocated, actual, difference)
    for i in range(len(community_fisherman_data['Community_Name'])):
        community_name = community_fisherman_data['Community_Name'][i]
        data_str = community_fisherman_data[last_column_name][i]
        allocated, actual, difference = map(int, data_str.split(';'))
        fishermen.append((community_name, allocated, actual, difference))

    # Sort fishermen based on the difference (priority to the most difference)
    fishermen.sort(key=lambda x: x[3], reverse=True)
    # print("Fishermen:")
    # print(fishermen)

    # Read fish_data CSV file
    fish_data = pd.read_csv('fish_data.csv')

    # Find fishes that match the current season
    current_date = datetime.strptime(last_column_name, '%m/%d/%Y')
    next_week_date = current_date + timedelta(days=7)
    # print("Next week date:")
    # print(next_week_date)
    # print("Current date:")
    # print(current_date)

    # Determine the current season
    if current_date.month in [3, 4, 5]:
        current_season = 'Spring'
    elif current_date.month in [6, 7, 8]:
        current_season = 'Summer'
    elif current_date.month in [9, 10, 11]:
        current_season = 'Fall'
    else:
        current_season = 'Winter'

    # Filter fish data for the current season
    current_season_fish = fish_data[fish_data['viable_season'] == current_season]
    # print('Current season fish:')
    # print(current_season_fish)

    # Select fishes present in the current season
    selected_fish = current_season_fish['name_of_fish'].tolist()
    # print("Selected fish:", selected_fish)

    allocated_fish = []

    # Allocate fishes to fishermen
    for fisherman in fishermen:
        allocated_fisherman = []
        for fish in selected_fish:
            if fish in allocated_fisherman:
                continue
            allocated_quantity = random.randint(100, 150)  # Randomly allocate quantity between 100 and 150
            actual_haul = random.randint(allocated_quantity - 30, allocated_quantity + 30)
            difference = allocated_quantity - actual_haul
            allocated_fisherman.append((fish, allocated_quantity, actual_haul, difference))

        allocated_fish.append({
            'fisherman_name': fisherman[0],
            'allocated_fish': allocated_fisherman
        })

    # Write updated community_fisherman_data to CSV file
    community_fisherman_data.to_csv('community_fisherman_data.csv', index=False)

    # print("Scheduling completed, and data written to community_fisherman_data.csv.")

    # Return allocated fish data as JSON
    return json.dumps(allocated_fish)

# Example usage:
# allocated_fish_json = read_community_fisherman_data()
# print("Allocated Fish (JSON):")
# print(allocated_fish_json)
