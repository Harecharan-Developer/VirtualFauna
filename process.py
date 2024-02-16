import pandas as pd
import random
from datetime import datetime, timedelta
import json

def fisherman_json(list_of_fisherman_name):
    df = pd.read_csv('community_fisherman_data.csv')         # Read the CSV file into a DataFrame
    new_rows = []                                            # Create a list to store new rows 
    for name in list_of_fisherman_name:                     # I terate through the list of fisherman names
        if name not in df['Community_Name'].values:         # Check if the name is not already present in the 'Community_Name' column
            new_rows.append({'Community_Name': name})

    new_df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
    new_df.fillna('', inplace=True)
    new_df.to_csv('community_fisherman_data.csv', index=False)


# Read community_fisherman_data CSV file
def read_community_fisherman_data():
    community_fisherman_data = pd.read_csv('community_fisherman_data.csv')
    fishermen = []
    last_column_name = community_fisherman_data.columns[-1]

    # Convert the data into tuples of (fisherman_name, allocated, actual, difference)
    for i in range(len(community_fisherman_data['Community_Name'])):
        community_name = community_fisherman_data['Community_Name'][i]
        data_str = community_fisherman_data[last_column_name][i]
        allocated, actual, difference = map(int, data_str.split(';'))
        fishermen.append((community_name, allocated, actual, difference))

    # Sort fishermen based on the difference (priority to the most difference)
    fishermen.sort(key=lambda x: x[3], reverse=True)

    # Read fish_data CSV file
    fish_data = pd.read_csv('fish_data.csv')

    # Find fishes that match the current season
    current_date = datetime.strptime(last_column_name, '%m/%d/%Y')
    next_week_date = current_date + timedelta(days=7)

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

    # Select fishes present in the current season
    selected_fish = current_season_fish['name_of_fish'].tolist()

    allocated_fish = {}

    allocated_quantity_list=[]
    for i in range(len(fishermen)):
        allocated_quantity_list.append(random.randint(100, 150))

    allocated_quantity_list.sort(reverse=True)

    counter=0
# Allocate fishes to fishermen
    for fisherman in fishermen:
        allocated_fisherman = []
        for fish in selected_fish:
            if fish in allocated_fisherman:
                continue
            actual_haul = random.randint(allocated_quantity_list[counter] - 30, allocated_quantity_list[counter] + 30)
            difference = allocated_quantity_list[counter] - actual_haul
            allocated_fisherman.append((fish, allocated_quantity_list[counter],actual_haul, difference))
        counter += 1
        allocated_fish[fisherman[0]] = allocated_fisherman


    # Write updated community_fisherman_data to CSV file
    community_fisherman_data.to_csv('community_fisherman_data.csv', index=False)

    # Return allocated fish data as a dictionary
    return allocated_fish

# Example usage:
allocated_fish_dict = read_community_fisherman_data()
print("Allocated Fish (Dictionary):")
print(allocated_fish_dict)




