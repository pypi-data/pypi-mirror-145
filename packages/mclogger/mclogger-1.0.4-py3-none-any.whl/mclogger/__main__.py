from mlogger import MLogger
import argparse

def setup_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", "--filename", required=True)
	


def main():
	args = parser.parse_args()

	logger = MLogger( args.filename).getLogger()

	logger.debug("hello world - debug")
	logger.info("hello world - info")
	logger.error("hello world - error")
	logger.warning("hello world - warning")

if __name__ == "__main__":
	setup_args()
	main()