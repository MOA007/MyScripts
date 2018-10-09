import sys
import os
import subprocess

assoc = {
    '.0-win-64bit-build1': 'PathAdd',
    '.3g2': 'VLC',
    '.3gp': 'VLC',
    '.3gp2': 'VLC',
    '.3gpp': 'VLC',
    '.4-win-x64': 'PathAdd',
    '.aac': 'VLC',
    '.abnf': 'notepad++',
    '.ac3': 'VLC',
    '.aco': 'notepad++',
    '.ahk': 'notepad++',
    '.ai': 'AI',
    '.aliases': 'notepad++',
    '.amr': 'VLC',
    '.amv': 'VLC',
    '.ape': 'VLC',
    '.ase': 'notepad++',
    '.asf': 'VLC',
    '.asp': 'notepad++',
    '.ass': 'VLC',
    '.asset': 'notepad++',
    '.asx': 'VLC',
    '.au3': 'notepad++',
    '.avi': 'VLC',
    '.bak': 'notepad++',
    '.bash_profile': 'notepad++',
    '.bashrc': 'notepad++',
    '.bat': 'notepad++',
    '.bib': 'notepad++',
    '.bin': 'HxD',
    '.bind': 'notepad++',
    '.bmp': 'IrfanView',
    '.bnf': 'notepad++',
    '.c': 'notepad++',
    '.c_': 'notepad++',
    '.cbp': 'notepad++',
    '.cfg': 'notepad++',
    '.cl7': 'notepad++',
    '.classpath': 'notepad++',
    '.cls': 'notepad++',
    '.cmake': 'notepad++',
    '.cmd': 'notepad++',
    '.cmdline': 'notepad++',
    '.cnf': 'notepad++',
    '.conf': 'notepad++',
    '.conffiles': 'notepad++',
    '.config': 'notepad++',
    '.conv': 'notepad++',
    '.cpp': 'notepad++',
    '.cps': 'notepad++',
    '.crash': 'notepad++',
    '.crdownload': 'VLC',
    '.crt': 'notepad++',
    '.cs': 'notepad++',
    '.cson': 'notepad++',
    '.css': 'notepad++',
    '.csv': 'notepad++',
    '.cu': 'notepad++',
    '.cue': 'VLC',
    '.cxx': 'notepad++',
    '.dat': 'VLC',
    '.dbml': 'notepad++',
    '.def': 'notepad++',
    '.desktop': 'notepad++',
    '.divx': 'VLC',
    '.dll': 'PathAdd',
    '.dmskm': 'VLC',
    '.dng': 'IrfanView',
    '.docx': 'LibreOfficeWriter',
    '.downloading': 'VLC',
    '.dpg': 'VLC',
    '.dpl': 'VLC',
    '.driveignore': 'notepad++',
    '.dropbox': 'notepad++',
    '.dtapart': 'VLC',
    '.dts': 'VLC',
    '.dtshd': 'VLC',
    '.dvr-ms': 'VLC',
    '.dxf': 'notepad++',
    '.eac3': 'VLC',
    '.efu': 'notepad++',
    '.ejs': 'notepad++',
    '.el': 'notepad++',
    '.emacs': 'notepad++',
    '.emf': 'notepad++',
    '.eml': 'notepad++',
    '.env': 'notepad++',
    '.eps': 'notepad++',
    '.epub': 'SumatraPDF',
    '.erb': 'notepad++',
    '.evo': 'VLC',
    '.exe': 'PathAdd',
    '.f4v': 'VLC',
    '.ffs_batch': 'notepad++',
    '.ffs_gui': 'notepad++',
    '.flac': 'VLC',
    '.flv': 'VLC',
    '.frag': 'notepad++',
    '.gif': 'IrfanView',
    '.git-credentials': 'notepad++',
    '.gitconfig': 'notepad++',
    '.gitignore': 'notepad++',
    '.gradle': 'notepad++',
    '.grid': 'notepad++',
    '.h': 'notepad++',
    '.h_': 'notepad++',
    '.hpp': 'notepad++',
    '.htk': 'notepad++',
    '.htm': 'notepad++',
    '.html': 'notepad++',
    '.hxx': 'notepad++',
    '.i': 'notepad++',
    '.ico': 'IrfanView',
    '.idc': 'notepad++',
    '.idx': 'VLC',
    '.ifo': 'VLC',
    '.iim': 'notepad++',
    '.iml': 'notepad++',
    '.index': 'notepad++',
    '.inf': 'notepad++',
    '.info': 'notepad++',
    '.ini': 'notepad++',
    '.inl': 'notepad++',
    '.ino': 'notepad++',
    '.ipynb': 'notepad++',
    '.iso': 'VLC',
    '.iss': 'notepad++',
    '.itf': 'notepad++',
    '.jade': 'notepad++',
    '.java': 'notepad++',
    '.jpeg': 'IrfanView',
    '.jpg': 'IrfanView',
    '.js': 'notepad++',
    '.json': 'notepad++',
    '.jsonlz4': 'notepad++',
    '.jsx': 'notepad++',
    '.k3g': 'VLC',
    '.keystore': 'notepad++',
    '.launch': 'notepad++',
    '.less': 'notepad++',
    '.list': 'notepad++',
    '.lmp4': 'VLC',
    '.lnk': 'HxD',
    '.log': 'notepad++',
    '.lrc': 'notepad++',
    '.lyx': 'notepad++',
    '.m1a': 'VLC',
    '.m1v': 'VLC',
    '.m2a': 'VLC',
    '.m2t': 'VLC',
    '.m2ts': 'VLC',
    '.m2v': 'VLC',
    '.m3u': 'VLC',
    '.m3u8': 'VLC',
    '.m4a': 'VLC',
    '.m4b': 'VLC',
    '.m4p': 'VLC',
    '.m4v': 'VLC',
    '.manifest': 'notepad++',
    '.markdown': 'notepad++',
    '.mat': 'notepad++',
    '.md': 'notepad++',
    '.mdt': 'notepad++',
    '.meta': 'notepad++',
    '.mf': 'notepad++',
    '.mk': 'notepad++',
    '.mka': 'VLC',
    '.mkd': 'notepad++',
    '.mkv': 'VLC',
    '.mod': 'VLC',
    '.modules': 'notepad++',
    '.mov': 'VLC',
    '.mp2': 'VLC',
    '.mp2v': 'VLC',
    '.mp3': 'VLC',
    '.mp4': 'VLC',
    '.mpa': 'VLC',
    '.mpc': 'VLC',
    '.mpe': 'VLC',
    '.mpeg': 'VLC',
    '.mpg': 'VLC',
    '.mpl': 'VLC',
    '.mpls': 'VLC',
    '.mpv2': 'VLC',
    '.mqv': 'VLC',
    '.ms11': 'notepad++',
    '.mtl': 'notepad++',
    '.mts': 'VLC',
    '.npy': 'notepad++',
    '.nsh': 'notepad++',
    '.nsi': 'notepad++',
    '.nsr': 'VLC',
    '.nsv': 'VLC',
    '.obj': 'notepad++',
    '.ods': 'LibreOfficeWriter',
    '.odt': 'LibreOfficeWriter',
    '.ogg': 'VLC',
    '.ogm': 'VLC',
    '.ogv': 'VLC',
    '.org': 'notepad++',
    '.out': 'notepad++',
    '.p12': 'notepad++',
    '.pac': 'notepad++',
    '.pak': 'notepad++',
    '.part': 'VLC',
    '.pbtxt': 'notepad++',
    '.pcap': 'notepad++',
    '.pde': 'notepad++',
    '.pdf': 'SumatraPDF',
    '.pem': 'notepad++',
    '.pgc': 'notepad++',
    '.php': 'notepad++',
    '.pkl': 'notepad++',
    '.pl': 'notepad++',
    '.plantuml': 'notepad++',
    '.pls': 'VLC',
    '.png': 'IrfanView',
    '.ppm': 'IrfanView',
    '.ppo': 'notepad++',
    '.prefs': 'notepad++',
    '.pri': 'notepad++',
    '.pro': 'notepad++',
    '.project': 'notepad++',
    '.properties': 'notepad++',
    '.props': 'notepad++',
    '.ps1': 'notepad++',
    '.psm1': 'notepad++',
    '.pub': 'notepad++',
    '.pxd': 'notepad++',
    '.py': 'notepad++',
    '.pyd': 'notepad++',
    '.pyx': 'notepad++',
    '.qsv': 'VLC',
    '.qtpotp': 'VLC',
    '.r': 'notepad++',
    '.ram': 'VLC',
    '.rapotp': 'VLC',
    '.rb': 'notepad++',
    '.record': 'notepad++',
    '.reg': 'notepad++',
    '.res': 'notepad++',
    '.rmpotp': 'VLC',
    '.rmvb': 'VLC',
    '.rpm': 'VLC',
    '.script': 'notepad++',
    '.sdirs': 'notepad++',
    '.sgy': 'notepad++',
    '.sh': 'notepad++',
    '.shader': 'notepad++',
    '.skm': 'VLC',
    '.sln': 'notepad++',
    '.smali': 'notepad++',
    '.smi': 'VLC',
    '.sql': 'notepad++',
    '.srt': 'notepad++',
    '.ssa': 'VLC',
    '.sub': 'VLC',
    '.sublime-menu': 'notepad++',
    '.sublime-package': 'notepad++',
    '.sublime-settings': 'notepad++',
    '.svg': 'IrfanView',
    '.swf': 'VLC',
    '.tak': 'VLC',
    '.td': 'VLC',
    '.tdl': 'VLC',
    '.tex': 'notepad++',
    '.tif': 'IrfanView',
    '.tiff': 'IrfanView',
    '.tmlanguage': 'notepad++',
    '.tmpreferences': 'notepad++',
    '.tp': 'notepad++',
    '.tpl': 'notepad++',
    '.tppotp': 'VLC',
    '.tpr': 'VLC',
    '.trp': 'VLC',
    '.ts': 'notepad++',
    '.tspotp': 'VLC',
    '.tsv': 'notepad++',
    '.tud': 'VLC',
    '.txt': 'notepad++',
    '.ui': 'notepad++',
    '.user': 'notepad++',
    '.vbs': 'notepad++',
    '.vcf': 'notepad++',
    '.vcproj': 'notepad++',
    '.vcxproj': 'notepad++',
    '.vec': 'HxD',
    '.vert': 'notepad++',
    '.vmx': 'notepad++',
    '.vob': 'VLC',
    '.wav': 'VLC',
    '.wax': 'VLC',
    '.wdapk': 'notepad++',
    '.webm': 'VLC',
    '.wma': 'VLC',
    '.wmf': 'notepad++',
    '.wmp': 'VLC',
    '.wmpotp': 'VLC',
    '.wmv': 'VLC',
    '.wmx': 'VLC',
    '.wtv': 'VLC',
    '.wvpotp': 'VLC',
    '.wvx': 'VLC',
    '.x68': 'notepad++',
    '.xls': 'notepad++',
    '.xml': 'notepad++',
    '.xyz': 'notepad++',
    '.yaml': 'notepad++',
    '.yml': 'notepad++',
    '.zim': 'notepad++',
    '.zip': 'GoogleDrive.cmd',
    '.zxp': 'notepad++'
}

program_path = {
    'notepad++': 'notepad++.exe',
    'VLC': 'C:\\Program Files\\VideoLAN\\VLC\\vlc.exe',
    'IrfanView': 'C:\\Program Files\\IrfanView\\i_view64.exe',
    'SumatraPDF': 'SumatraPDF.exe'
}


def main():
    file_path = sys.argv[1]
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in assoc:
        raise '%s is not defined' % ext

    program = assoc[ext]
    if program not in program_path:
        raise Exception('%s not found' % program)
    program = program_path[program]

    subprocess.Popen([program, file_path])


try:
    main()
except Exception as e:
    print(e)
    input()
