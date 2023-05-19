# -----------------------------------------------------------------------------
# Emily Mitchell
# 5/19/23
#
# Using Python to query GitHub API
#  - using to get traffic for AHRQ repositories
#  - and store data 
# 
# Note: need a personal access token to query traffics 
#  - need push access to repositories that you are querying
# -----------------------------------------------------------------------------

# get date for tagging csv output files
from datetime import date

# Using 'requests' library to query Github API 
import pandas as pd
import os
import requests


# Get a Personal Access Token from GitHub -------------------------------------
# Steps (as of 2/1/23):
#   https://github.com/settings/developers
#   > GitHub Developer Settings > Personal access tokens (classic) 
#     Generate new token (classic)
#      1. Add note (e.g. python_meps)
#      2. Set expiration (github will email when it's almost expired)
#      3. check 'repo' box
#      4. Generate token



token = os.getenv("GH_TOKEN") # get secret token 


# Set headers, using token
headers = {
      "Authorization": f"token {token}",
      "User-Agent": "testing-requests-5801",
      "Accept": "application/vnd.github.v3+json",
  }


# Examples --------------------------------------------------------------------
#
# # Example 1: get general info on e-mitchell
# em_url = "https://api.github.com/users/e-mitchell"
# em_info = requests.get(em_url, headers = headers).json()
# 
# 
# # Example 2: Get general info on e-mitchell's repos
# em_repo_url = "https://api.github.com/users/e-mitchell/repos"
# em_repos = requests.get(em_repo_url, headers = headers).json()


# Get traffic data for AHRQ repositories -------------------------------------

# first, need to loop to get all repositories
# [add looping code here]

ahrq_repos_url = "https://api.github.com/users/HHS-AHRQ/repos"

resp = requests.get(ahrq_repos_url, headers = headers)
print(resp)

all_repos = resp.json()

user = "HHS-AHRQ"

meps_repos = [
  "MEPS",
  "MEPS-workshop",
  "MEPS-summary-tables",
  "MEPS-linking-webinar-1",
  "MEPS-linking-webinar-2"]


for repo in meps_repos:
  print(repo)

  # Then, pull traffic views from each repo and output to a csv file
  
  traffic_views = f"https://api.github.com/repos/{user}/{repo}/traffic/views"
  
  # Make request
  r = requests.get(traffic_views, headers = headers)
  print(r)
      
  # Convert to pandas dataframe
  traffic_df = pd.DataFrame(r.json()['views'])
  
  # output to csv
  traffic_df.to_csv(f"traffic_reports/traffic_{repo}_{date.today()}.csv", index = False)





