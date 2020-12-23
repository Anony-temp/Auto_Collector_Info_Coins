import os

os.system('crontab -e 0 8 * * * python3 AutoCollect_Days.py')
os.system('crontab -e 0 8 1 * * python3 AutoCollect_Months.py')
os.system('crontab -e 0 8 * * 1 python3 AutoCollect_Weeks.py')
os.system('python3 AutoCollect_Minutes.py')