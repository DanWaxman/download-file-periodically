# download-file-periodically
This is a python script to download a file periodically (either weekly, daily, or hourly).
The script requires Python 3 and usage is as follows:

#Usage:
`$ python3 download-file-periodically.py -u/--url -f/--file -t/--time -h/--help`

Where:  
>-u or --url is the url to download a file from. **This is a required flag and must have a valid url as the argument following it.**  
>-f or --file is the directory for the downloading file to be saved in. **This is a required flag and must have an argument following it.**  
>-h or --help describes usage to the user. This flag is optional and the program will not execute if this flag is set.  
>-t or --time specifies the time period over which the file is downloaded. **This option accepts three arguments: w for weekly, d for daily, and h for hourly. This defaults to week.**  

#Requirements:
The validators module must be installed.
