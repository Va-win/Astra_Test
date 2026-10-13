import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

os.makedirs("data", exist_ok=True)
base_url = "https://www.scrapethissite.com/pages/forms/?page_num="

rows = []
for page in range(1, 25):
    resp = requests.get(f"{base_url}{page}", timeout=15)
    soup = BeautifulSoup(resp.content, "html.parser")
    table = soup.find("table", class_="table")
    if not table:
        break
    
    for tr in table.find_all("tr", class_="team"):
        tds = tr.find_all("td")
        if not tds:
            continue
        
        team = tds[0].text.strip()
        year = tds[1].text.strip()
        wins = tds[2].text.strip()
        losses = tds[3].text.strip()
        ot_losses = tds[4].text.strip()
        win_rate = tds[5].text.strip()
        goals_for = tds[6].text.strip()
        goals_against = tds[7].text.strip()
        goal_diff = tds[8].text.strip()
        
        rows.append({
            "team": team,
            "year": int(year) if year else None,
            "wins": int(wins) if wins else None,
            "losses": int(losses) if losses else None,
            "ot_losses": int(ot_losses) if ot_losses else None,
            "win_rate": float(win_rate) if win_rate else None,
            "goals_for": int(goals_for) if goals_for else None,
            "goals_against": int(goals_against) if goals_against else None,
            "goal_diff": int(goal_diff) if goal_diff else None
        })

df = pd.DataFrame(rows)
df.to_csv("data/hockey_raw.csv", index=False)
print(f"Собрано {len(df)} строк и сохранено в data/hockey_raw.csv")