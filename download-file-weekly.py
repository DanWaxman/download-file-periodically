#!/usr/bin/python

from urllib.request import urlretrieve
import time
import getopt
import sys
import validators
import os

''' 
I store these as global variables so they can be accessed by every class and there's 
not chance of using the wrong one
'''
file_path = None
url = None
# Made for readability
seconds_in_week = 604800
# Made for readability
usage = '-h/--help -- prints out usage\n-u/--url -- defines url to retrieve file from\n-f/--file -- defines output file path'


class GetFiles:
  def __init__(self):
    # declare the global variables to class instance variables for easier access
    global file_path
    global url
    self.file_path = file_path
    self.url = url
  def get_file(self):
    '''
    Downloads the file.
    Param free since the script is using global variables.
    Files are named by the convention master-%weekday-%month-%year.
    Next run time is calculated as well and stored in next_run.txt.
    '''
    self.file_name = time.strftime('master-%a-%b-%d-%Y', time.localtime())
    print('Downloading...')
    urlretrieve(self.url, self.file_path + '/' + self.file_name)
    print('Downloaded.')
    self.next_run = int(time.time()) + seconds_in_week
    with open('next_run.txt', 'w') as f:
      f.write(str(self.next_run))
    print('Next run on ' + str(self.next_run))

class TimeCheck:
  def check_time(self):
    ''' 
    Checks if the current time is greater than or equal to the calculated next run.
    next_run.txt is opened in a+ mode so the file is created if it doesn't exist.
    Returns True if it's time for next download, or False if it's not.
    Empty string needs to be accounted for because if the file was just created the file needs to be downloaded.
    It is worth being noted that the next run is stored in a text file so the next run remains unchanged even on seperate executions.
    '''
    self.current_time = time.time()
    with open('next_run.txt', 'a+') as f:
      self.scheduled_run = f.read(10)
      if self.scheduled_run == '':
        return True
      return True if int(self.scheduled_run) >= self.current_time else False

class MainClass:
  def main(self, argv):
    '''
    Parses arguments and makes sure they're valid.
    Sets global variables for global use.
    Makes sure path and url are defined.
    If path doesn't exist, path is made.
    Checks time. If check_time() returns True, get the file.
    Then sleeps for a week + 1 second to avoid possible rounding errors.
    '''
    global usage
    global url
    global file_path
    try:
      opts, args = getopt.getopt(argv, "u:f:h", ["url=", "file=", "help"])
    except getopt.GetoptError: # Exception for invalid args
      print(usage)
      sys.exit(2)
    for opt, arg in opts:
      if opt in ('-h', '--help'):
        print(usage)
        sys.exit(2)
      elif opt in ('-u', '--url'):
        url = arg
        if not validators.url(url):
          print('Sorry, invalid url!')
          sys.exit(2)
        print('url set to ' + url)
      elif opt in ('-f', '--file'):
        file_path = arg
        if not os.path.exists(file_path):
          os.makedirs(file_path)
        print('file path set to ' + file_path)

    self.get_files = GetFiles()
    self.time_check = TimeCheck()

    if file_path is not None and url is not None:
      while True:
        if(self.time_check.check_time() == True):
          self.get_files.get_file()
        print('Sleeping...')
        time.sleep(seconds_in_week+1) # This is just to avoid weird rounding errors
    else:
      print('Sorry, file path and url need to be defined. For usage, use the argument -h')
      
if __name__ == '__main__':
  main_class = MainClass()
  main_class.main(sys.argv[1:])
