import json

# Load data from JSON file
user_input = input("Enter a file name: ")
with open(f'database/{user_input}.json', 'r') as f:
    data = json.load(f)

# Find duplicates
app_counts = {}
duplicate_apps = []

for app in data['apps']:
    if app in app_counts:
        if app_counts[app] == 1:
            duplicate_apps.append(app)
        app_counts[app] += 1
    else:
        app_counts[app] = 1

# Print duplicates
if duplicate_apps:
    print("Duplicate apps:")
    for app in duplicate_apps:
        print(app)
else:
    print("No duplicate apps found.")
