import os

os.system('crontab -e 0 8 * * * ./run_days.sh')
os.system('crontab -e 0 8 1 * * ./run_months.sh')
os.system('crontab -e 0 8 * * 1 ./run_weeks.sh')
os.system('python3 AutoCollect_Minutes.py')