import os
import re
from pprint import pprint

import requests

TOKEN = os.environ.get("GITHUB_TOKEN")
OWNER = "iterative"
REPO = "ldb-hackathon"

HEADERS = {"Accept": "application/vnd.github+json",
           "Authorization": f"token {TOKEN}"}


def get_submit_commit(job_id):
    data = requests.get(
        f"https://api.github.com/repos/{OWNER}/{REPO}/actions/jobs/{job_id}/logs",
        headers=HEADERS).text
    match = re.search(
        r"copy: s3://ldb-hackathon-team-6/repo/(.*)/train/dataset.json", data)
    if not match:
        return
    return match.group(1).split("/")[0]


def get_scores():
    data = requests.get(
        "https://raw.githubusercontent.com/iterative/ldb-hackathon/main/leaderboard.md?token=GHSAT0AAAAAABOGYIY3THDAHNARMO73SH2UYXWLSIQ").text
    res = {}
    for line in data.splitlines():
        match = re.search("\|\s*(\d*)\s*\|\s*mike0sv\s*\|.*\|.*\|\s*(\w*)\s*\|",
                          line)
        if match:
            rank, descr = match.groups()
            res[descr] = rank
    return res

def get_sumbit_message(sumbit):
    r = requests.get(f"https://api.github.com/repos/mike0sv/ldb-hack/commits/{sumbit}", headers=HEADERS)

    return r.json()["commit"]["message"]


def main():
    """curl \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token <TOKEN>" \
  https://api.github.com/repos/OWNER/REPO/actions/runs"""
    r = requests.get(
        f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs",
        params={"actor": "mike0sv", "per_page": 100},
        headers=HEADERS)

    all_wfs = r.json()
    team_workflows = [
        wf for wf in all_wfs["workflow_runs"] if
        wf["name"] == "Submission" and wf["actor"]["login"] == "mike0sv" and
        wf['conclusion'] != 'cancelled'
    ]

    stats = {
        wf["html_url"]: {
            "status": wf["status"],
            'conclusion': wf['conclusion'],
            "jobs_url": wf['jobs_url']
        } for wf in team_workflows
    }
    scores = get_scores()
    for url, values in stats.items():
        jobs = requests.get(values["jobs_url"], headers=HEADERS)
        setup_job_id = jobs.json()["jobs"][0]["id"]
        submit = get_submit_commit(setup_job_id)
        if not submit:
            continue
        values["submit"] = submit
        values["rank"] = scores.get(submit, None)
        values[
            "submit_url"] = f"https://github.com/mike0sv/ldb-hack/commit/{submit}"
        values["message"] = get_sumbit_message(submit)

    for run_url, values in stats.items():
        print(run_url)
        pprint(values)
        print()


if __name__ == '__main__':
    main()
