import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime, pylab
import dateutil
from matplotlib.dates import DayLocator, MonthLocator, DateFormatter


days    = DayLocator()   # every year
months   = MonthLocator()  # every month
yearsFmt = DateFormatter('%m-%d')

quantity = [3,5,3,6,3]
datestrings = ["2011-03-17 17:27:49","2011-03-17 17:27:49","2011-03-13 16:57:49","2011-03-07 00:47:48","2011-02-17 16:57:21"]
dates = [dateutil.parser.parse(s) for s in datestrings]

fig = plt.figure()
ax = fig.add_subplot(111)
ax.bar(pylab.date2num(dates), quantity)
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(yearsFmt)
ax.xaxis.set_minor_locator(days)
ax.autoscale_view()
ax.fmt_xdata = DateFormatter('%Y-%m-%d')

fig.autofmt_xdate()

plt.show()