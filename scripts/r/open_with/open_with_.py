import sys
import os
import subprocess
import traceback
import _appmanager

assoc = {
    '.0-win-64bit-build1': ['PathAdd'],
    '.3g2': ['VLC', 'mpv'],
    '.3gp': ['VLC', 'mpv'],
    '.3gp2': ['VLC', 'mpv'],
    '.3gpp': ['VLC', 'mpv'],
    '.4-win-x64': ['PathAdd'],
    '.aac': ['VLC', 'mpv'],
    '.abnf': ['notepad++', 'vscode'],
    '.ac3': ['VLC', 'mpv'],
    '.aco': ['notepad++', 'vscode'],
    '.ahk': ['notepad++', 'vscode'],
    '.ai': ['AI'],
    '.aliases': ['notepad++', 'vscode'],
    '.amr': ['VLC', 'mpv'],
    '.amv': ['VLC', 'mpv'],
    '.ape': ['VLC', 'mpv'],
    '.ase': ['notepad++', 'vscode'],
    '.asf': ['VLC', 'mpv'],
    '.asp': ['notepad++', 'vscode'],
    '.ass': ['VLC', 'mpv'],
    '.asset': ['notepad++', 'vscode'],
    '.asx': ['VLC', 'mpv'],
    '.au3': ['notepad++', 'vscode'],
    '.avi': ['VLC', 'mpv'],
    '.bak': ['notepad++', 'vscode'],
    '.bash_profile': ['notepad++', 'vscode'],
    '.bashrc': ['notepad++', 'vscode'],
    '.bat': ['notepad++', 'vscode'],
    '.bib': ['notepad++', 'vscode'],
    '.bin': ['HxD'],
    '.bind': ['notepad++', 'vscode'],
    '.bmp': ['IrfanView'],
    '.bnf': ['notepad++', 'vscode'],
    '.c': ['notepad++', 'vscode'],
    '.c_': ['notepad++', 'vscode'],
    '.cbp': ['notepad++', 'vscode'],
    '.cfg': ['notepad++', 'vscode'],
    '.cl7': ['notepad++', 'vscode'],
    '.classpath': ['notepad++', 'vscode'],
    '.cls': ['notepad++', 'vscode'],
    '.cmake': ['notepad++', 'vscode'],
    '.cmd': ['notepad++', 'vscode'],
    '.cmdline': ['notepad++', 'vscode'],
    '.cnf': ['notepad++', 'vscode'],
    '.conf': ['notepad++', 'vscode'],
    '.conffiles': ['notepad++', 'vscode'],
    '.config': ['notepad++', 'vscode'],
    '.conv': ['notepad++', 'vscode'],
    '.cpp': ['notepad++', 'vscode'],
    '.cps': ['notepad++', 'vscode'],
    '.crash': ['notepad++', 'vscode'],
    '.crdownload': ['VLC', 'mpv'],
    '.crt': ['notepad++', 'vscode'],
    '.cs': ['notepad++', 'vscode'],
    '.cson': ['notepad++', 'vscode'],
    '.css': ['notepad++', 'vscode'],
    '.csv': ['notepad++', 'tad'],
    '.cu': ['notepad++', 'vscode'],
    '.cue': ['VLC', 'mpv'],
    '.cxx': ['notepad++', 'vscode'],
    '.dat': ['VLC', 'mpv'],
    '.dbml': ['notepad++', 'vscode'],
    '.def': ['notepad++', 'vscode'],
    '.desktop': ['notepad++', 'vscode'],
    '.divx': ['VLC', 'mpv'],
    '.dll': ['PathAdd'],
    '.dmskm': ['VLC', 'mpv'],
    '.dng': ['IrfanView'],
    '.docx': ['LibreOfficeWriter'],
    '.downloading': ['VLC', 'mpv'],
    '.dpg': ['VLC', 'mpv'],
    '.dpl': ['VLC', 'mpv'],
    '.driveignore': ['notepad++', 'vscode'],
    '.dropbox': ['notepad++', 'vscode'],
    '.dtapart': ['VLC', 'mpv'],
    '.dts': ['VLC', 'mpv'],
    '.dtshd': ['VLC', 'mpv'],
    '.dvr-ms': ['VLC', 'mpv'],
    '.dxf': ['notepad++', 'vscode'],
    '.dot': ['notepad++', 'vscode'],
    '.eac3': ['VLC', 'mpv'],
    '.efu': ['notepad++', 'vscode'],
    '.ejs': ['notepad++', 'vscode'],
    '.el': ['notepad++', 'vscode'],
    '.emacs': ['notepad++', 'vscode'],
    '.emf': ['notepad++', 'vscode'],
    '.eml': ['notepad++', 'vscode'],
    '.env': ['notepad++', 'vscode'],
    '.eps': ['notepad++', 'vscode'],
    '.epub': ['SumatraPDF', 'adobereader'],
    '.erb': ['notepad++', 'vscode'],
    '.evo': ['VLC', 'mpv'],
    '.exe': ['PathAdd'],
    '.f4v': ['VLC', 'mpv'],
    '.ffs_batch': ['notepad++', 'vscode'],
    '.ffs_gui': ['notepad++', 'vscode'],
    '.flac': ['VLC', 'mpv'],
    '.flv': ['VLC', 'mpv'],
    '.frag': ['notepad++', 'vscode'],
    '.gif': ['IrfanView'],
    '.git-credentials': ['notepad++', 'vscode'],
    '.gitconfig': ['notepad++', 'vscode'],
    '.gitignore': ['notepad++', 'vscode'],
    '.gradle': ['notepad++', 'vscode'],
    '.grid': ['notepad++', 'vscode'],
    '.h': ['notepad++', 'vscode'],
    '.h_': ['notepad++', 'vscode'],
    '.hpp': ['notepad++', 'vscode'],
    '.htk': ['notepad++', 'vscode'],
    '.htm': ['notepad++', 'vscode'],
    '.html': ['notepad++', 'vscode'],
    '.hxx': ['notepad++', 'vscode'],
    '.i': ['notepad++', 'vscode'],
    '.ico': ['IrfanView'],
    '.idc': ['notepad++', 'vscode'],
    '.idx': ['VLC', 'mpv'],
    '.ifo': ['VLC', 'mpv'],
    '.iim': ['notepad++', 'vscode'],
    '.iml': ['notepad++', 'vscode'],
    '.index': ['notepad++', 'vscode'],
    '.inf': ['notepad++', 'vscode'],
    '.info': ['notepad++', 'vscode'],
    '.ini': ['notepad++', 'vscode'],
    '.inl': ['notepad++', 'vscode'],
    '.ino': ['notepad++', 'vscode'],
    '.ipynb': ['notepad++', 'vscode'],
    '.iso': ['VLC', 'mpv'],
    '.iss': ['notepad++', 'vscode'],
    '.itf': ['notepad++', 'vscode'],
    '.jade': ['notepad++', 'vscode'],
    '.java': ['notepad++', 'vscode'],
    '.jpeg': ['IrfanView'],
    '.jpg': ['IrfanView'],
    '.js': ['notepad++', 'vscode'],
    '.json': ['notepad++', 'vscode'],
    '.jsonlz4': ['notepad++', 'vscode'],
    '.jsx': ['notepad++', 'vscode'],
    '.k3g': ['VLC', 'mpv'],
    '.keystore': ['notepad++', 'vscode'],
    '.launch': ['notepad++', 'vscode'],
    '.less': ['notepad++', 'vscode'],
    '.list': ['notepad++', 'vscode'],
    '.lmp4': ['VLC', 'mpv'],
    '.lnk': ['HxD'],
    '.log': ['notepad++', 'vscode'],
    '.lrc': ['notepad++', 'vscode'],
    '.lyx': ['notepad++', 'vscode'],
    '.lua': ['notepad++', 'vscode'],
    '.m1a': ['VLC', 'mpv'],
    '.m1v': ['VLC', 'mpv'],
    '.m2a': ['VLC', 'mpv'],
    '.m2t': ['VLC', 'mpv'],
    '.m2ts': ['VLC', 'mpv'],
    '.m2v': ['VLC', 'mpv'],
    '.m3u': ['VLC', 'mpv'],
    '.m3u8': ['VLC', 'mpv'],
    '.m4a': ['VLC', 'mpv'],
    '.m4b': ['VLC', 'mpv'],
    '.m4p': ['VLC', 'mpv'],
    '.m4v': ['VLC', 'mpv'],
    '.manifest': ['notepad++', 'vscode'],
    '.markdown': ['notepad++', 'vscode'],
    '.mat': ['notepad++', 'vscode'],
    '.md': ['notepad++', 'vscode'],
    '.mdt': ['notepad++', 'vscode'],
    '.meta': ['notepad++', 'vscode'],
    '.mf': ['notepad++', 'vscode'],
    '.mk': ['notepad++', 'vscode'],
    '.mka': ['VLC', 'mpv'],
    '.mkd': ['notepad++', 'vscode'],
    '.mkv': ['VLC', 'mpv'],
    '.mod': ['VLC', 'mpv'],
    '.modules': ['notepad++', 'vscode'],
    '.mov': ['VLC', 'mpv'],
    '.mp2': ['VLC', 'mpv'],
    '.mp2v': ['VLC', 'mpv'],
    '.mp3': ['VLC', 'Audacity'],
    '.mp4': ['VLC', 'mpv'],
    '.mpa': ['VLC', 'mpv'],
    '.mpc': ['VLC', 'mpv'],
    '.mpe': ['VLC', 'mpv'],
    '.mpeg': ['VLC', 'mpv'],
    '.mpg': ['VLC', 'mpv'],
    '.mpl': ['VLC', 'mpv'],
    '.mpls': ['VLC', 'mpv'],
    '.mpv2': ['VLC', 'mpv'],
    '.mqv': ['VLC', 'mpv'],
    '.ms11': ['notepad++', 'vscode'],
    '.mtl': ['notepad++', 'vscode'],
    '.mts': ['VLC', 'mpv'],
    '.npy': ['notepad++', 'vscode'],
    '.nsh': ['notepad++', 'vscode'],
    '.nsi': ['notepad++', 'vscode'],
    '.nsr': ['VLC', 'mpv'],
    '.nsv': ['VLC', 'mpv'],
    '.obj': ['notepad++', 'vscode'],
    '.ods': ['LibreOfficeWriter'],
    '.odt': ['LibreOfficeWriter'],
    '.ogg': ['VLC', 'mpv'],
    '.ogm': ['VLC', 'mpv'],
    '.ogv': ['VLC', 'mpv'],
    '.org': ['notepad++', 'vscode'],
    '.out': ['notepad++', 'vscode'],
    '.p12': ['notepad++', 'vscode'],
    '.pac': ['notepad++', 'vscode'],
    '.pak': ['notepad++', 'vscode'],
    '.part': ['VLC', 'mpv'],
    '.pbtxt': ['notepad++', 'vscode'],
    '.pcap': ['notepad++', 'vscode'],
    '.pde': ['notepad++', 'vscode'],
    '.pdf': ['SumatraPDF', 'adobereader'],
    '.pem': ['notepad++', 'vscode'],
    '.pgc': ['notepad++', 'vscode'],
    '.php': ['notepad++', 'vscode'],
    '.pkl': ['notepad++', 'vscode'],
    '.pl': ['notepad++', 'vscode'],
    '.plantuml': ['notepad++', 'vscode'],
    '.pls': ['VLC', 'mpv'],
    '.png': ['IrfanView'],
    '.ppm': ['IrfanView'],
    '.ppo': ['notepad++', 'vscode'],
    '.prefs': ['notepad++', 'vscode'],
    '.pri': ['notepad++', 'vscode'],
    '.pro': ['notepad++', 'vscode'],
    '.project': ['notepad++', 'vscode'],
    '.properties': ['notepad++', 'vscode'],
    '.props': ['notepad++', 'vscode'],
    '.ps1': ['notepad++', 'vscode'],
    '.psm1': ['notepad++', 'vscode'],
    '.pub': ['notepad++', 'vscode'],
    '.pxd': ['notepad++', 'vscode'],
    '.py': ['notepad++', 'vscode'],
    '.pyd': ['notepad++', 'vscode'],
    '.pyx': ['notepad++', 'vscode'],
    '.qsv': ['VLC', 'mpv'],
    '.qtpotp': ['VLC', 'mpv'],
    '.r': ['notepad++', 'vscode'],
    '.ram': ['VLC', 'mpv'],
    '.rapotp': ['VLC', 'mpv'],
    '.rb': ['notepad++', 'vscode'],
    '.record': ['notepad++', 'vscode'],
    '.reg': ['notepad++', 'vscode'],
    '.res': ['notepad++', 'vscode'],
    '.rmpotp': ['VLC', 'mpv'],
    '.rmvb': ['VLC', 'mpv'],
    '.rpm': ['VLC', 'mpv'],
    '.script': ['notepad++', 'vscode'],
    '.sdirs': ['notepad++', 'vscode'],
    '.sgy': ['notepad++', 'vscode'],
    '.sh': ['notepad++', 'vscode'],
    '.shader': ['notepad++', 'vscode'],
    '.skm': ['VLC', 'mpv'],
    '.sln': ['notepad++', 'vscode'],
    '.smali': ['notepad++', 'vscode'],
    '.smi': ['VLC', 'mpv'],
    '.sql': ['notepad++', 'vscode'],
    '.srt': ['notepad++', 'vscode'],
    '.ssa': ['VLC', 'mpv'],
    '.sub': ['VLC', 'mpv'],
    '.sublime-menu': ['notepad++', 'vscode'],
    '.sublime-package': ['notepad++', 'vscode'],
    '.sublime-settings': ['notepad++', 'vscode'],
    '.svg': ['IrfanView'],
    '.swf': ['VLC', 'mpv'],
    '.tak': ['VLC', 'mpv'],
    '.td': ['VLC', 'mpv'],
    '.tdl': ['VLC', 'mpv'],
    '.tex': ['notepad++', 'vscode'],
    '.tif': ['IrfanView'],
    '.tiff': ['IrfanView'],
    '.tmlanguage': ['notepad++', 'vscode'],
    '.tmpreferences': ['notepad++', 'vscode'],
    '.tp': ['notepad++', 'vscode'],
    '.tpl': ['notepad++', 'vscode'],
    '.tppotp': ['VLC', 'mpv'],
    '.tpr': ['VLC', 'mpv'],
    '.trp': ['VLC', 'mpv'],
    '.ts': ['notepad++', 'vscode'],
    '.tspotp': ['VLC', 'mpv'],
    '.tsv': ['notepad++', 'vscode'],
    '.tud': ['VLC', 'mpv'],
    '.txt': ['notepad++', 'vscode'],
    '.ui': ['notepad++', 'vscode'],
    '.user': ['notepad++', 'vscode'],
    '.vbs': ['notepad++', 'vscode'],
    '.vcf': ['notepad++', 'vscode'],
    '.vcproj': ['notepad++', 'vscode'],
    '.vcxproj': ['notepad++', 'vscode'],
    '.vec': ['HxD'],
    '.vert': ['notepad++', 'vscode'],
    '.vmx': ['notepad++', 'vscode'],
    '.vob': ['VLC', 'mpv'],
    '.wav': ['VLC', 'Audacity'],
    '.wax': ['VLC', 'mpv'],
    '.wdapk': ['notepad++', 'vscode'],
    '.webm': ['VLC', 'mpv'],
    '.wma': ['VLC', 'mpv'],
    '.wmf': ['notepad++', 'vscode'],
    '.wmp': ['VLC', 'mpv'],
    '.wmpotp': ['VLC', 'mpv'],
    '.wmv': ['VLC', 'mpv'],
    '.wmx': ['VLC', 'mpv'],
    '.wtv': ['VLC', 'mpv'],
    '.wvpotp': ['VLC', 'mpv'],
    '.wvx': ['VLC', 'mpv'],
    '.x68': ['notepad++', 'vscode'],
    '.xls': ['notepad++', 'vscode'],
    '.xml': ['notepad++', 'vscode'],
    '.xyz': ['notepad++', 'vscode'],
    '.yaml': ['notepad++', 'vscode'],
    '.yml': ['notepad++', 'vscode'],
    '.zim': ['notepad++', 'vscode'],
    '.zip': ['7zFM'],
    '.zxp': ['notepad++', 'vscode'],
    '.gz': ['7zFM'],
    '.usf': ['notepad++', 'vscode'],
    '.tar': ['7zFM'],
}


def main():
    file_path = sys.argv[1]
    program_id = int(sys.argv[2])

    ext = os.path.splitext(file_path)[1].lower()
    if ext not in assoc:
        raise Exception('%s is not defined' % ext)

    program = assoc[ext][program_id]
    args = [_appmanager.get_executable(program), file_path]
    subprocess.Popen(args)


try:
    main()
except Exception as e:
    traceback.print_exc(file=sys.stdout)
    print(e)
    input()
