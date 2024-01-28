import cx_Freeze

executables = [cx_Freeze.Executable("tic-tac-toe.py", icon="icon.ico", base=None, target_name='tic-tac-toe.exe')]

cx_Freeze.setup(
    name="TicTacToe Lite",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["assets/"], "excludes":["anyio","argon2-cffi","argon2-cffi-bindings","asttokens","attrs","Babel","backcall","beautifulsoup4","bleach","certifi","cffi","charset-normalizer","click","colorama","cx-Freeze","cx-Logging","debugpy","decorator","defusedxml","entrypoints","et-xmlfile","executing","ftfy","idna","ipykernel","ipython","ipython-genutils","jedi","Jinja2","joblib","json5","jsonschema","jupyter-client","jupyter-core","jupyter-server","jupyterlab","jupyterlab-pygments","jupyterlab-server","langcodes","lief","MarkupSafe","matplotlib-inline","mistune","msgpack","nbclassic","nbclient","nbconvert","nbformat","nest-asyncio","nltk","notebook","notebook-shim","openpyxl","packaging","pandocfilters","parso","pickleshare","pip","prometheus-client","prompt-toolkit","psutil","pure-eval","pycparser","pydub","Pygments","pyparsing","pypinyin","pyrsistent","python-dateutil","pytz","pywin32","pywinpty","pyzmq","regex","requests","Send2Trash","setuptools","six","sniffio","soupsieve","stack-data","terminado","testpath","tornado","tqdm","traitlets","urllib3","wcwidth","webencodings","websocket-client","wget","wordfreq","you-get"]}},
    executables = executables)