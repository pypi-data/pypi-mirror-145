from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: POSIX :: Linux',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.8'
]

setup(
    name='ktuhope',
    version='0.0.1',
    description='Programs on Data Sceince & Machine Learning',
    long_description=open('README.txt').read() + '\n\n' +
    open('CHANGELOG.txt').read(),
    url='',
    author='Zhongli',
    author_email='',
    license='MIT',
    classifiers=classifiers,
    keywords='DataScience KTU DSLab',
    packages=find_packages(),
    install_requires=['numpy', 
                    'pandas', 
                    'sklearn', 
                    'seaborn', 
                    'scipy', 
                    'lxml', 
                    'requests',
                    'bs4',
                    'beautifulsoup4', 
                    'nltk', 
                    'matplotlib', 
                    'math']
)
