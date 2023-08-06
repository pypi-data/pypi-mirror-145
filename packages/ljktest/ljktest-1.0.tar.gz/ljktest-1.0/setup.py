from distutils.core import  setup
import setuptools
packages = ['ljktest']# 唯一的包名，自己取名
setup(name='ljktest',
	version='1.0',
	author='aubreyliu',
    packages=packages,
    package_dir={'requests': 'requests'},)