# Environment Setup

## Common Steps

1. Setup python. For Windows, python27 is required, because *twisted* doesn't support python3 in Windows.
2. Setup virtualenv: `pip install virtualenv`
3. Setup venv: cd into the ScholarBar repo folder first

    In Ubuntu, run

    ```bash
    virtualenv venv
    source venv/bin/activate
    ````

    In Windows, if you use multiple versions of python, you should run
    ```bash
    virtualenv -p <python27 executable path> venv # example: virtualenv -p C:/Python27/python.exe venv
    venv/Scripts/activate
    ```

## Setup scrapy

Do as Common Steps first.

### For Ubuntu
```bash
sudo apt-get install openssl libssl-dev
pip install scrapy
````

### For Windows

1. Install [Microsoft Visual C++ Build Tools](https://www.microsoft.com/en-us/download/details.aspx?id=48159)
2. Install [Microsoft Visual C++ Compiler for Python 2.7](https://www.microsoft.com/en-us/download/details.aspx?id=44266)
3. Install lxml: `pip install src/contrib/lxml-3.7.1-cp27-cp27m-win_amd64.whl`
4. Install scrapy: `pip install scrapy`
5. Install win32api: unzip and copy `src/contrib/site-packages/*` into `venv/Lib/site-packages/`

