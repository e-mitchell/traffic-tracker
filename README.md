# traffic-tracker

This repository uses GitHub Actions to regularly store traffic data for the [HHS-AHRQ repositories](https://github.com/HHS-AHRQ).

GitHub traffic stores data for only the last 2 weeks. This repository contains spreadsheets of snapshots of traffic data, starting in May 2023 (or initialization of repository, whichever comes later).

### Background
Federal agencies can track website views on .gov sites using tools like Google Analytics. For external sites, such as code posted on GitHub, we must rely on GitHub's traffic insights to track views. 

However, GitHub traffic is only available for the last two weeks, so we wanted a way to automatically capture and store this data.

# Process
## 1.  Generate personal access token from GitHub
Go to: [github.com/settings/developers](github.com/settings/developers)
<br>\> GitHub Developer Settings
<br>\> Personal access tokens (classic)
<br>\> Generate new token (classic):
1. Add note (e.g. 'python_meps')
2. Set expiration (github will email when it's almost expired)
3. check 'repo' box
4. Generate token

> *PRO TIP*: If this code is in a public repo, don't paste the token in your Python code! Save it as a 'secret' in GitHub repo (under 'settings'), then refer to it using the 'os.getenv' function

## 2.  Write Python Code to query API and output data to csv
[github_api_traffic.py](github_api_traffic.py) loops through all repositories under the user 'HHS_AHRQ'. This simpler example code shows how to query the API for a single repository:

``` python
from datetime import date
import pandas as pd
import os
import requests

token = os.getenv("GH_TOKEN") # get secret token 

# Set headers, using token
headers = {
      "Authorization": f"token {token}",
      "User-Agent": "testing-requests-5801",
      "Accept": "application/vnd.github.v3+json",
  }
  
ahrq_repos_url = "https://api.github.com/users/HHS-AHRQ/repos"

user = "HHS-AHRQ"
repo_name = "MEPS"

traffic_views = f"https://api.github.com/repos/{user}/{repo_name}/traffic/views"

# Make request and output to csv
r = requests.get(traffic_views, headers = headers)

# select traffic 'views' from response
traffic_df = pd.DataFrame(r.json()['views'])

traffic_df.to_csv(f"traffic_reports/{repo_name}/traffic_{repo_name}_{date.today()}.csv", index = False)
```

## 3.  Run code automatically using GitHub Actions
[.github/workflows/run_tracker.yml](.github/workflows/run_tracker.yml)
Create yaml file in GitHub Actions that runs Python code every day (or week). After the python code saves the csv file, the yaml tells GitHub to commit the csv files to the repository.

```yaml
name: traffic tracker
on:
  # run every day at 6am UTC time (2am EST)
  schedule:
    - cron: "0 6 * * *"

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run Python script
        env:
          GH_TOKEN: ${{ secrets.GH_TOKEN }}
        run: python github_api_traffic.py

      - name: Commit changes
        run: |
          git config --global user.email "mitcheem@gmail.com"
          git config --global user.name "Emily Mitchell"
          git add .
          git commit -m "Add generated CSV traffic files"
          git push
```

## 4.  Visualize!
