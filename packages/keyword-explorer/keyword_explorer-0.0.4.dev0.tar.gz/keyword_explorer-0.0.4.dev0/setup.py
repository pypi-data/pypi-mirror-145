from  distutils.core import  setup

setup(
    name='keyword_explorer',
    version= "0.0.4.dev",
    packages=['keyword_explorer',
              'keyword_explorer.utils',
              'keyword_explorer.TwitterV2',
              'keyword_explorer.tkUtils',
              'keyword_explorer.OpenAI',
              'keyword_explorer.Apps'],
    url='https://github.com/pgfeldman/KeywordExplorer',
    license='MIT',
    author='Philip Feldman',
    author_email='phil@philfeldman.com',
    description='A tool for producing and exploring keywords',
    long_description='A tool for producing and exploring keywords',
    install_requires=[
        'pandas~=1.3.5',
        'matplotlib~=3.2.2',
        'numpy~=1.19.5',
        'sklearn~=0.0',
        'scikit-learn~=0.24.2',
        'requests~=2.27.1',
        'wikipedia~=1.4.0',
        'openai~=0.11.5',
        'networkx~=2.6.2',
        'tkinterweb~=3.12.2'],

    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

