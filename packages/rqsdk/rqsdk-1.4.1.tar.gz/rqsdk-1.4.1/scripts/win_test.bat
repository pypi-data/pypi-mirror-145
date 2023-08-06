set PROJECT_NAME=%1
set py_env=%2
set env_name=%1%2
echo %env_name%
C:\Users\rice\Miniconda3\Scripts\conda.exe create -n %env_name% python=%py_env% -y
C:\Users\rice\Miniconda3\envs\%env_name%\Scripts\pip.exe install --extra-index-url https://rquser:Ricequant8@pypi2.ricequant.com/simple/ -e . pytest
C:\Users\rice\Miniconda3\envs\%env_name%\python.exe -m pytest --doctest-modules