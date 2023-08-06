# coding: utf-8
from setuptools import setup, find_packages

setup(name='coilcraft',  #打包后的包文件名
      version='1.1',
      description='coilcraft_loss', #说明
      author='felix',
      author_email='qiyu_sjtu@163.com',
      packages=find_packages(),
      url='',
      include_package_data=True,
      # package_data={'': ['./coilcraft/model/*.txt','model/*.txt']},
      py_modules=['coilcraft.coilcraft_loss'],   #你要打包的文件
)