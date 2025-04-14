# Codeforces Problem Recommender
A command-line application that suggests personalized Codeforces practice problems based on a user's handle, rating, and the tags of problems they've already solved successfully.

## Features

- Fetches user's solved problems and rating from Codeforces API
- Analyzes which problem tags the user has practiced more/less
- Recommends problems based on:
  - User's current rating (suggests problems within an appropriate difficulty range)
  - Problem tags (prioritizes less-practiced tags)
  - Already solved problems (excludes these from recommendations)
- Provides explanations for why each problem is recommended
- Caches problem set data to minimize API requests

## Requirements

- Python 3.6+
- `requests` library

## Installation

1. Clone or download this repository
2. Install the required library:

```bash
pip install requests
```

## Usage

Run the script with a Codeforces handle (username) as an argument:

```bash
python codeforces_recommender.py [handle]
```

Optional arguments:
- `--num`: Number of problems to recommend (default: 5)

Example:

```bash
python codeforces_recommender.py tourist --num 3
```

## How It Works

1. **Data Collection**: Fetches your submission history and current rating from Codeforces
2. **Analysis**: Determines which problem tags you've solved more/less and your rating range
3. **Recommendation**: Finds unsolved problems that match your skill level while helping you improve in weaker areas
4. **Display**: Shows problem details with direct links and explains why each problem was recommended

## Project Structure

- `codeforces_recommender.py`: Main script with all functionality
- `cache/`: Directory for caching problem set data (created automatically)

## Notes

- The first run may take longer as it downloads the problem set data
- Subsequent runs will use cached data (refreshed daily)
