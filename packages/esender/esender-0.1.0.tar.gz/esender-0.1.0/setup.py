from setuptools import setup
setup(name='esender',
      version='0.1.0',
      description='send email for notification',
      url=' ',
      author='Jiesi',
      author_email='jiesihu@usc.com',
      license='MIT',
      packages=['esender'],
      install_requires=[
            'yagmail>=0.15.277',  
            ],
      zip_safe=False)