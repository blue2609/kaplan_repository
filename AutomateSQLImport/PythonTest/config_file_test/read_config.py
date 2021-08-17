import configparser 

config = configparser.ConfigParser()
config.sections()

config.read('example.ini')
# print(config.sections())

# print('bitbucket.org' in config)
for key in config['bitbucket.org']:
	print(key)