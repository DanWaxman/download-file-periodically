#!/usr/bin/python

from urllib.request import urlretrieve
import time
import getopt
import sys
import validators
import os

''' 
I store these as global variables so they can be accessed by every class and there's 
not chance of using the wrong one.
These are initialized to None so I can make sure they're specified by the user.
'''
FILE_PATH = None
URL = None
# Hold time mode -- 'w' is week, 'd' is day, and 'h' is hour.
# Defaults to week.
TIME_MODE = 'w'
# Dictionary that holds seconds during each mode so they can easily be accessed by TIME_DURING[TIME_MODE]
TIME_DURING = {
    'w': 604800,
    'd': 86400,
    'h': 3600}
# Made for readability
USAGE = '-h/--help -- prints out usage\n-u/--url -- defines url to retrieve file from\n-f/--file -- defines output file path\n-t/--time -- specifies the amount of time between downloads. h is hour, d is day, w is week. Defaults to week.'


class GetFiles:
  def __init__(self):
    # declare the global variables to class instance variables for easier access
    self.file_path = FILE_PATH
    self.url = URL
  def get_file(self):
    '''
    Downloads the file.
    Param free since the script is using global variables.
    Files are named by the convention master-%weekday-%month-%year-%hour-%minute.
    Next run time is calculated as well and stored in next_run.txt.
    '''
    self.file_name = time.strftime('master-%a-%b-%d-%Y-%H-%M', time.localtime())
    print('Downloading...')
    urlretrieve(self.url, self.file_path + '/' + self.file_name)
    print('Downloaded.')
    self.next_run = int(time.time()) + TIME_DURING[TIME_MODE]
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
    global USAGE
    global URL
    global FILE_PATH
    global TIME_MODE
    try:
      opts, args = getopt.getopt(argv, "u:f:t:h", ["url=", "file=", "time=", "help"])
    except getopt.GetoptError: # Exception for invalid args
      print(USAGE)
      sys.exit(2)
    for opt, arg in opts:
      if opt in ('-h', '--help'):
        print(USAGE)
        sys.exit(2)
      elif opt in ('-u', '--url'):
        URL = arg
        if not validators.url(URL):
          print('Sorry, invalid url!')
          sys.exit(2)
        print('url set to ' + URL)
      elif opt in ('-f', '--file'):
        FILE_PATH = arg
        if not os.path.exists(FILE_PATH):
          os.makedirs(FILE_PATH)
        print('file path set to ' + FILE_PATH)
      elif opt in ('-t', '--time'):
        TIME_MODE = arg
        if arg not in ('w', 'd', 'h'):
          print('ERROR: Invalid time argument. Type -h for proper usage.')
          sys.exit(2)
        print('Time mode is set to ' + TIME_MODE)

    self.get_files = GetFiles()
    self.time_check = TimeCheck()

    # Global values are all initiated to none. If they're not initiated, they're not specified.
    if FILE_PATH is not None and URL is not None:
      while True:
        if(self.time_check.check_time() == True):
          self.get_files.get_file()
        print('Sleeping...')

        time.sleep(TIME_DURING[TIME_MODE] + 1) # This is just to avoid weird rounding errors
    else:
      print('Sorry, file path and url need to be defined. For usage, use the argument -h')
      
if __name__ == '__main__':
  main_class = MainClass()
  main_class.main(sys.argv[1:])
