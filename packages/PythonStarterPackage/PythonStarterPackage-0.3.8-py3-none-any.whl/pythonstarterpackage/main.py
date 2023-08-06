#!/usr/bin/python3 -B
from .starterpkg import StarterPkg
from .utils.configparser import ConfigParser

def main():
	configparser = ConfigParser()
	starterpkg = StarterPkg(configparser)
	#starterpkg.run()
	#print(configparser.filepath)
	print(configparser.env)

if __name__ == '__main__':
	raise SystemExit(main())