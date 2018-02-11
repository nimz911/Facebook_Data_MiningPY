from distutils.core import setup
setup(
  name = 'Facebook_Data_MiningPY',
  packages = ['Facebook_Data_MiningPY'], # this must be the same as the name above
  version = '1.2.0',
  description = 'read Facebook groups or pages data',
  author = 'Nimrod Zilberstein',
  author_email = 'nimz911@gmail.com',
  url = 'https://github.com/nimz911/Facebook_Data_MiningPY', # use the URL to the github repo
  download_url = 'https://github.com/nimz911/Facebook_Data_MiningPY/archive/1.0.tar.gz', # I'll explain this in a second
  keywords = ['facebook', 'data mining'], # arbitrary keywords
  license='MIT',
  install_requires=['pandas','nltk','facebook-sdk','requests','time','datetime','json'],
  classifiers = ['Programming Language :: Pyhton :: 2',
                 'Programming Language :: Pyhton :: 2.7'],
)
