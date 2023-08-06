import logging, sys, re
from colorama import Fore, Style
import coloredlogs, tailer

########################################################################################################################
# Create colors for the output
class MyFormatter(logging.Formatter):
    prefix = "%(asctime)s [%(filename)s:%(lineno)s - %(funcName)5s() ] [%(levelname)-5.5s] "
    FORMATS = {
        logging.ERROR: Fore.RED + prefix + Style.RESET_ALL + "%(message)s", 
        logging.DEBUG: Fore.BLUE + prefix + Style.RESET_ALL + "%(message)s",
        logging.WARNING: Fore.YELLOW + prefix + Style.RESET_ALL + "%(message)s",
        "DEFAULT": Fore.CYAN + prefix + Style.RESET_ALL + "%(message)s",
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.FORMATS['DEFAULT'])
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record) 


########################################################################################################################
# Log to console and to file
class MCLogger(object):
	logInst = None 
	logfilepath = ""
	config = []

	# def read_file(last_n_rows):
	def __init__(self, out_filename):
		self._filename = out_filename

	################################################################################################
	# Get last n_rows from the log
	def read_log_file(self, last_n_rows = 20):
		with open(self._filename, 'r') as file:
			last_lines = tailer.tail(file, last_n_rows)
		return last_lines
	
	################################################################################################
	# Get last n_rows from the log
	def read_log_file_as_text(self, last_n_rows = 20):
		last_lines = self.read_log_file(last_n_rows)
		for index, line in enumerate(last_lines):
			last_lines[index] = re.sub(r'\x1b\[.+?m', '', last_lines[index], flags=re.MULTILINE )
		return last_lines

	################################################################################################
	# Configure logger
	def _setupLogger(self):
		logInst = logging.getLogger(__name__)

		custom_formatter = MyFormatter()
		logInst.setLevel(logging.DEBUG)

		fileHandler = logging.FileHandler( self._filename)
		fileHandler.setFormatter(custom_formatter)
		logInst.addHandler(fileHandler)

		consoleHandler = logging.StreamHandler(sys.stdout)
		consoleHandler.setFormatter(custom_formatter)
		logInst.addHandler(consoleHandler)
		logInst.read_log_file_as_text = self.read_log_file_as_text
		logInst.read_log_file  = self.read_log_file  

		return logInst

	################################################################################################
	# Main function to call
	def getLogger(self): 
		if self.logInst	== None:
			self.logInst	= self._setupLogger( )
		return self.logInst	 	