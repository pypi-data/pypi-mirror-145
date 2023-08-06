from setuptools import setup, find_packages


setup(
    name='sfsd-py',
    version='1.0',
    license='MIT',
    author="Ouassim Hamdani",
    description="A python module made for the educational course 'SFSD' which represents 'Files structures and file handeling', this course is for 2nd year students at the grand schools of computer science, and can be used by any engineer looking to handle files at their base level, Made by Ouassim Hamdani",
    author_email='o_hamdani@estin.dz',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Ouassim-Hamdani/SFSD',
    keywords='SFSD,file structure, ouassim, hamdani, python file,file handle',
    install_requires=[
          'texttable',
      ],

)
