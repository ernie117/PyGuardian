from pyguardian.main.pyguardian import PyGuardian


PyGuardian().gamertag("Chuckles2505").platform("playstation").fetch_historical_stats().print_stats_json()
