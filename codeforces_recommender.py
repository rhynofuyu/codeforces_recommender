#!/usr/bin/env python3
"""
Codeforces Problem Recommender
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta
import requests


# API endpoints
CF_API_BASE = "https://codeforces.com/api/"
USER_STATUS_ENDPOINT = CF_API_BASE + "user.status"
USER_INFO_ENDPOINT = CF_API_BASE + "user.info"
PROBLEM_SET_ENDPOINT = CF_API_BASE + "problemset.problems"

# Cache settings
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")
PROBLEMSET_CACHE_FILE = os.path.join(CACHE_DIR, "problemset_cache.json")
CACHE_EXPIRY_DAYS = 1  # Refresh problem set cache after this many days


def setup_cache_dir():
    """Create cache directory if it doesn't exist."""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)


def fetch_with_retry(url, params=None, max_retries=3):
    """Fetch data from an API with retry logic."""
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries == max_retries:
                print(f"Error fetching data: {e}")
                return None
            print(f"Retry {retries}/{max_retries} after error: {e}")
            time.sleep(2)  # Wait before retrying


def fetch_user_info(handle):
    """Fetch user rating information."""
    print(f"Fetching user information for {handle}...")
    response = fetch_with_retry(USER_INFO_ENDPOINT, params={"handles": handle})
    
    if not response or response.get("status") != "OK":
        print(f"Failed to fetch user info for {handle}.")
        if response and response.get("comment"):
            print(f"Error: {response.get('comment')}")
        return None
    
    return response["result"][0]


def fetch_user_submissions(handle):
    """Fetch the submissions history for a user."""
    print(f"Fetching submission history for {handle}...")
    response = fetch_with_retry(USER_STATUS_ENDPOINT, params={"handle": handle})
    
    if not response or response.get("status") != "OK":
        print(f"Failed to fetch submission history for {handle}.")
        if response and response.get("comment"):
            print(f"Error: {response.get('comment')}")
        return None
    
    return response["result"]


def fetch_problemset():
    """Fetch the problem set, using cache if available and recent."""
    setup_cache_dir()
    
    if os.path.exists(PROBLEMSET_CACHE_FILE):
        cache_file_time = datetime.fromtimestamp(os.path.getmtime(PROBLEMSET_CACHE_FILE))
        if datetime.now() - cache_file_time < timedelta(days=CACHE_EXPIRY_DAYS):
            print("Using cached problem set data...")
            with open(PROBLEMSET_CACHE_FILE, 'r') as f:
                return json.load(f)
    
    print("Fetching problem set from Codeforces API...")
    response = fetch_with_retry(PROBLEM_SET_ENDPOINT)
    
    if not response or response.get("status") != "OK":
        print("Failed to fetch problem set.")
        if response and response.get("comment"):
            print(f"Error: {response.get('comment')}")
        if os.path.exists(PROBLEMSET_CACHE_FILE):
            print("Using outdated cache as fallback...")
            with open(PROBLEMSET_CACHE_FILE, 'r') as f:
                return json.load(f)
        return None
    
    with open(PROBLEMSET_CACHE_FILE, 'w') as f:
        json.dump(response["result"], f)
    
    return response["result"]


def analyze_user_data(user_info, submissions):
    """Analyze user's submission data to extract problem-solving patterns."""
    if not user_info or not submissions:
        return None
    
    user_rating = user_info.get("rating", 0)
    solved_problems = set()
    tag_counts = {}
    
    for submission in submissions:
        if submission.get("verdict") == "OK":
            problem = submission.get("problem", {})
            problem_id = (problem.get("contestId"), problem.get("index"))
            
            if problem_id not in solved_problems:
                solved_problems.add(problem_id)
                
                for tag in problem.get("tags", []):
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    return {
        "user_rating": user_rating,
        "solved_problems": solved_problems,
        "tag_counts": tag_counts,
        "total_solved": len(solved_problems)
    }


def generate_recommendations(user_analysis, problemset, num_recommendations=5):
    """Generate problem recommendations based on user analysis."""
    if not user_analysis or not problemset:
        return []
    
    problems = problemset.get("problems", [])
    user_rating = user_analysis["user_rating"]
    solved_problems = user_analysis["solved_problems"]
    tag_counts = user_analysis["tag_counts"]
    
    min_rating = max(800, user_rating - 100)
    max_rating = user_rating + 200
    
    sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1])
    weaker_tags = [tag for tag, count in sorted_tags[:len(sorted_tags)//2]] if sorted_tags else []
    
    scored_problems = []
    for problem in problems:
        problem_id = (problem.get("contestId"), problem.get("index"))
        
        if problem_id in solved_problems or "rating" not in problem:
            continue
        
        problem_rating = problem["rating"]
        if problem_rating < min_rating or problem_rating > max_rating:
            continue
        
        rating_diff = abs(problem_rating - (user_rating + 50))
        base_score = 1000 - rating_diff
        
        problem_tags = problem.get("tags", [])
        tag_score = 0
        
        for tag in problem_tags:
            if tag in weaker_tags:
                tag_score += 300
            elif tag in tag_counts:
                tag_score += 100
        
        final_score = base_score + tag_score
        
        reasons = []
        if any(tag in weaker_tags for tag in problem_tags):
            weak_tags = [tag for tag in problem_tags if tag in weaker_tags]
            reasons.append(f"Targets less-practiced tag(s): {', '.join(weak_tags)}")
        elif problem_rating > user_rating:
            reasons.append(f"Slightly harder problem ({problem_rating - user_rating} above your rating)")
        else:
            reasons.append(f"Good match for your current rating")
        
        scored_problems.append({
            "problem": problem,
            "score": final_score,
            "reasons": reasons
        })
    
    recommendations = sorted(scored_problems, key=lambda x: x["score"], reverse=True)
    return recommendations[:num_recommendations]


def display_results(recommendations, handle):
    """Display the recommended problems in a user-friendly format."""
    if not recommendations:
        print("\nSorry, no suitable problems found for your profile.")
        print("This might happen if you've solved all problems in your rating range.")
        return
    
    print(f"\nRecommended problems for {handle}:")
    print("-" * 80)
    
    for i, rec in enumerate(recommendations, 1):
        problem = rec["problem"]
        contest_id = problem.get("contestId")
        index = problem.get("index")
        name = problem.get("name", "Unnamed")
        rating = problem.get("rating", "Unknown")
        tags = ", ".join(problem.get("tags", []))
        
        if contest_id is not None:
            url = f"https://codeforces.com/problemset/problem/{contest_id}/{index}"
        else:
            url = "URL not available"
        
        print(f"{i}. {name} (Rating: {rating})")
        print(f"   Tags: {tags}")
        print(f"   URL: {url}")
        print(f"   Why: {' '.join(rec['reasons'])}")
        print("-" * 80)


def main():
    """Main function to run the recommender."""
    parser = argparse.ArgumentParser(description="Codeforces Problem Recommender")
    parser.add_argument("handle", help="Codeforces handle (username)")
    parser.add_argument("--num", type=int, default=5, help="Number of recommendations (default: 5)")
    args = parser.parse_args()
    
    user_info = fetch_user_info(args.handle)
    if not user_info:
        sys.exit(1)
    
    submissions = fetch_user_submissions(args.handle)
    if submissions is None:
        sys.exit(1)
    
    problemset = fetch_problemset()
    if not problemset:
        sys.exit(1)
    
    user_analysis = analyze_user_data(user_info, submissions)
    if not user_analysis:
        print("Failed to analyze user data.")
        sys.exit(1)
    
    print(f"\nAnalysis: You have solved {user_analysis['total_solved']} problems")
    print(f"Current rating: {user_analysis['user_rating']}")
    
    recommendations = generate_recommendations(user_analysis, problemset, args.num)
    display_results(recommendations, args.handle)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)