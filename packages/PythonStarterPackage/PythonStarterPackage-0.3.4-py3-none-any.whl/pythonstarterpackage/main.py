#!/usr/bin/python3 -B
from .starterpkg import StarterPkg
from .utils.configparser import ConfigParser
from pkg_resources import Requirement, resource_filename

def main():
	configparser = ConfigParser()
	starterpkg = StarterPkg(configparser)
	#starterpkg.run()
	print(configparser.filepath)
	resource_filename(Requirement.parse('pythonstarterpackage'),'config')

if __name__ == '__main__':
	raise SystemExit(main())