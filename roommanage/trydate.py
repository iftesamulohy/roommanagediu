# importing datetime module
import datetime
from dateutil.relativedelta import relativedelta, MO,WE
# getting today's date
todayDate = datetime.date.today()
print('Today Date:',todayDate)

# Increment today's date with 1 week to get the next Monday
nextMonday = todayDate + relativedelta(weekday=WE(1))

print('Next Monday Date:',nextMonday)