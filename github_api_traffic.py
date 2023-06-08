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
#   > GitHub Developer Settings 
#   > Personal access tokens (classic) 
#   > Generate new token (classic)
#      1. Add note (e.g. python_meps)
#      2. Set expiration (github will email when it's almost expired)
#      3. check 'repo' box
#      4. Generate token


# PRO TIP: If this code is in a public repo, don't paste the token here! Save it 
# as a 'secret' in GitHub repo (under 'settings'), then refer to it using the 
# 'os.getenv' function


token = os.getenv("GH_TOKEN") # get secret token 


# Set headers, using token
headers = {
      "Authorization": f"token {token}",
      "User-Agent": "testing-requests-5801",
      "Accept": "application/vnd.github.v3+json",
  }


# Get traffic data for AHRQ repositories -------------------------------------

ahrq_repos_url = "https://api.github.com/users/HHS-AHRQ/repos"

# API query to get info for all HHS-AHRQ repositories
meps_repos = requests.get(ahrq_repos_url, headers = headers).json()

user = "HHS-AHRQ"


# Loop through repositories
for repo in meps_repos:
  
  repo_name = repo['name']
  #print(repo_name)
  
  # Pull traffic views from each repo 
  traffic_views = f"https://api.github.com/repos/{user}/{repo_name}/traffic/views"
  
  # Make request
  r = requests.get(traffic_views, headers = headers)
  #pprint(r.json()['views'])
  
  # Convert to pandas dataframe
  traffic_df = pd.DataFrame(r.json()['views'])
  
  # Output to csv 
  #  > first create directory for storing traffic reports if it doesn't exist
  
  repo_dir = f"traffic_reports/{repo_name}"
  
  if not os.path.exists(repo_dir):
    os.mkdir(repo_dir)
  
  traffic_df.to_csv(f"traffic_reports/{repo_name}/traffic_{repo_name}_{date.today()}.csv", index = False)


