from _shutil import *


# Simplify / subset font by specify characters to include.
cd(gettempdir())
f = download(
    'https://raw.githubusercontent.com/DavidSheh/CommonChineseCharacter/master/3500%E5%B8%B8%E7%94%A8%E5%AD%97.txt')
print(f)
text = open(f, encoding='utf-8').read()
subprocess.check_call(['pyftsubset',
                       r"C:\Users\Ross\Downloads\SourceHanSansCN\SourceHanSansCN-Bold.ttf",
                       f'--text={text}'])
