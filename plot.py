# plots the data created by jobserve_gmail.py
# requires http://matplotlib.sourceforge.net/
#
# author jerome.lacoste@gmail.com

import sys
import dateutil, pylab 
import time
import datetime

def read_csv(csv):
  with open(csv, "r") as f:
    r = []
    data = f.read()
    for line in data.split("\n"):
      r.append(line.split(","))
    return r

def plot_jobserve(csv):
  array = read_csv(csv)
  dates = []
  values = []
  for a in array:
    if -1 == a[0].find("JobServe"):
      continue
    subject = a[0].split(":")
#    print subject
#    full_date = subject[len(subject) - 1].strip()
    date = a[1].strip()
    nb = a[2].strip()
    d = time.strptime(date, "%d %B %Y")
#    print date + "," + nb
    dates.append(datetime.datetime(*d[0:5]))
    values.append(int(nb))

  pylab.plot_date(pylab.date2num(dates), values, linestyle='-')  
  pylab.savefig("jobserve_stats.png")
  pylab.show()

if __name__ == "__main__":
  csv = "jobserve.txt"
  if len(sys.argv) > 1:
    csv = sys.argv[1]
  plot_jobserve(csv)

