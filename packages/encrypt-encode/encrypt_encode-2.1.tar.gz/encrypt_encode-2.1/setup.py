from setuptools import setup,find_packages

with open("README.md", "r", encoding="utf8") as f:
    long_description = f.read()

setup(name='encrypt_encode',
      version='2.1',
      description="encrypt encode text",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/keegang6705/encrypt_encode',
      author='keegang_6705',
      author_email='darunphobwi@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires= [''],
      python_requires='>=3.0',
      zip_safe=False)