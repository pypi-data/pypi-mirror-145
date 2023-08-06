import setuptools

with open( "README.md" , 'r', encoding="utf-8") as fh:
    long_description = fh.read()

    # print( long_description )
    
setuptools.setup(
    name = "HackerGprat",
    version = "0.3.4",
    author = "HackerGprat",
    author_email = "Sorry@gmail.com",   # "https://youtube.com/HackerGprat" # test it working or not
    description = "Here You can find Userfull fucntion which you need in your every python packages.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/HackerGprat/HackerGprat-PIP-Library/",
    
    install_requires =['numpy',
                       'pandas',
                       'matplotlib',
                       'scipy',
                       'binance',
                       'python-binance',
                       'pillow',
                       'setuptools',
                       'wheel',
                       'requests',
                       'ipython',
                       'scikit-learn',
                       'sklearn',
                       'seaborn',
                       'bs4',
                       'plyer'
                    #    '--upgrade pip' error while buidling dont use this
        ],
    
    project_urls={
        "Bug Tracker" : "https://github.com/HackerGprat/HackerGprat-PIP-Library/issues",
        "Website" : "https://hackergprat.github.io",
        "Instagram": "https://instagram.com/HackerGprat",
        "YouTube" : "https://youtube.com/HackerGprat"
    },
    
    classifiers = [
        "Programming Language :: Python :: 3", 
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    # test it before upload / working or not?
    # Testing = [
    #     "Cool Name :: HackerGprat"
    #     "Cool Nam1 :: HackerGprat1"
    #     "Cool Nam2 :: HackerGprat2"
    # ],
    
    
    package_dir = { "" : "src" },
    packages = setuptools.find_packages( where="src" ),
    python_requires =">=3.6",
    
)


    
    
