@echo off
set "PATH=C:\tools\miniconda3;C:\tools\miniconda3\Scripts;%PATH%"
call activate.bat

conda install pytorch torchvision cudatoolkit=9.0 -c pytorch -y
