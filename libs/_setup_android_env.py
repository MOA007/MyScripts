from _shutil import *


def setup_android_env():
    ADK_SEARCH_PATH = [
        # Installed by choco
        r'C:\Android\android-sdk',

        # Default SDK path installed by Android Studio
        os.path.abspath(os.getenv('LOCALAPPDATA') + '/Android/Sdk')
    ]

    # ANDROID_HOME
    for p in ADK_SEARCH_PATH:
        if os.path.exists(p):
            env['ANDROID_HOME'] = p
            print('Set ANDROID_HOME to %s' % p)
            break

    # NDK
    env['ANDROID_NDK_HOME'] = \
        env['ANDROID_NDK_ROOT'] = \
        env['NDKROOT'] = \
        env['NDK_ROOT'] = \
        env['ANDROID_HOME'] + '/ndk-bundle'

    # Android build tools (latest)
    build_tools_path = sorted(list(glob.glob(env['ANDROID_HOME'] + '\\build-tools\\*')))[-1]

    # Set PATH environ
    jdk_path = sorted(glob.glob(r'C:\Program Files\Java\jdk*'), reverse=True)[0] + '\\bin'
    path = [
        env['ANDROID_HOME'] + '/platform-tools',
        build_tools_path,
        env['ANDROID_HOME'] + '/tools',
        env['ANDROID_HOME'] + '/tools/bin',
        env['ANDROID_HOME'] + '/ndk-bundle',
        jdk_path,
    ]
    prepend_to_path(path)


# setup_android_env()
studio = r'C:\Program Files\Android\Android Studio\bin\studio64.exe'
