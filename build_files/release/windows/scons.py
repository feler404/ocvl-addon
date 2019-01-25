import os
import os.path
import subprocess


VERSION_DISPLAY = "1.2.0.0"
VERSION = "1.2"


def nsis_installer(target=None, source=None, env=None):
    print("="*35)
    print(target, source)

    bitness = '64'

    start_dir = os.getcwd()
    rel_dir = os.path.join(start_dir, 'release', 'windows', 'installer')
    install_base_dir = start_dir + os.sep

    bf_installdir = os.path.join(os.getcwd(), env['BF_INSTALLDIR'])
    bf_installdir = os.path.normpath(bf_installdir)

    doneroot = False
    rootdirconts = []
    datafiles = ''
    deldatafiles = ''
    deldatadirs = ''
    len_bf_installdir = len(bf_installdir)

    for dp, dn, df in os.walk(bf_installdir):
        # install
        if not doneroot:
            for f in df:
                rootdirconts.append(os.path.join(dp, f))
            doneroot = True
        else:
            if len(df) > 0:
                datafiles += "\n" + r'SetOutPath $INSTDIR' + dp[len_bf_installdir:] + "\n\n"

                for f in df:
                    outfile = os.path.join(dp, f)
                    datafiles += '  File '+outfile + "\n"

        # uninstall
        deldir = dp[len_bf_installdir+1:]

        if len(deldir) > 0:
            deldatadirs = "RMDir $INSTDIR\\" + deldir + "\n" + deldatadirs
            deldatadirs = "RMDir /r $INSTDIR\\" + deldir + "\\__pycache__\n" + deldatadirs

            for f in df:
                deldatafiles += 'Delete \"$INSTDIR\\' + os.path.join(deldir, f) + "\"\n"

    # change to suit install dir
    inst_dir = install_base_dir + env['BF_INSTALLDIR']


    os.chdir(rel_dir)

    ns = open("00.sconsblender.nsi", "r")

    ns_cnt = str(ns.read())
    ns.close()

    # var replacements
    ns_cnt = ns_cnt.replace("[DISTDIR]", os.path.normpath(inst_dir+os.sep))
    ns_cnt = ns_cnt.replace("[VERSION]", VERSION_DISPLAY)
    ns_cnt = ns_cnt.replace("[SHORTVERSION]", VERSION)
    ns_cnt = ns_cnt.replace("[RELDIR]", os.path.normpath(rel_dir))
    ns_cnt = ns_cnt.replace("[BITNESS]", bitness)

    # do root
    rootlist = []
    for rootitem in rootdirconts:
        rootlist.append("File \"" + rootitem + "\"")
    rootstring = "\n  ".join(rootlist)
    rootstring += "\n\n"
    ns_cnt = ns_cnt.replace("[ROOTDIRCONTS]", rootstring)

    # do delete items
    delrootlist = []
    for rootitem in rootdirconts:
        delrootlist.append("Delete $INSTDIR\\" + rootitem[len_bf_installdir+1:])
    del_root_string = "\n ".join(delrootlist)
    del_root_string += "\n"
    ns_cnt = ns_cnt.replace("[DELROOTDIRCONTS]", del_root_string)

    ns_cnt = ns_cnt.replace("[DODATAFILES]", datafiles)
    ns_cnt = ns_cnt.replace("[DELDATAFILES]", deldatafiles)
    ns_cnt = ns_cnt.replace("[DELDATADIRS]", deldatadirs)

    tmpnsi = os.path.normpath(install_base_dir+os.sep+env['BF_BUILDDIR']+os.sep+"00.blender_tmp.nsi")
    new_nsis = open(tmpnsi, 'w')
    new_nsis.write(ns_cnt)
    new_nsis.close()
    print("NSIS Installer script created")

    os.chdir(start_dir)
    print("Launching 'makensis'")

    cmdline = "makensis " + "\""+tmpnsi+"\""

    startupinfo = subprocess.STARTUPINFO()
    #  startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    proc = subprocess.Popen(
        cmdline,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        startupinfo=startupinfo,
        shell=True
    )
    data, err = proc.communicate()
    rv = proc.wait()

    if rv != 0:
        print(data.strip().split("\n")[-1])
    return rv
