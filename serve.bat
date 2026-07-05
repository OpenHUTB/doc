:: 启动mkdocs虚拟环境（注意替换为本地的anaconda3目录、虚拟环境名为mkdocs）
rem 判断 conda 中是否存在 mkdocs 虚拟环境，如果不存在则创建
conda env list | findstr mkdocs >nul
if %errorlevel% neq 0 (
    conda create --name mkdocs python=3.10 -y
    conda activate mkdocs
    pip install -r requirements.txt
)
rem exit /b 0


%WINDIR%\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy ByPass -NoExit -Command "& 'D:\hutb\Build\dependencies\prerequisites\miniconda3\shell\condabin\conda-hook.ps1' ; conda activate 'D:\hutb\Build\dependencies\prerequisites\miniconda3' "; conda activate mkdocs; mkdocs serve --livereload;

