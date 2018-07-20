# -*- coding: utf-8 -*-
"""
Copyright information.
"""
def choose_copyright_permission():
    """ uses recommended permissions settings for oVert TCN """
    CopyrightPermission = ["Copyright permission not set",
    "Person loading media owns copyright and grants permission for use of media on MorphoSource",
    "Permission to use media on MorphoSource granted by copyright holder",
    "Permission pending",
    "Copyright expired or work otherwise in public domain",
    "Copyright permission not yet requested"]
    print()
    print()
    print()
    print("### Copyright Permission Options:")
    for i in range(len(CopyrightPermission)):
        print(str(i) + ": " + CopyrightPermission[i])
    PermissionChoice = input("Select copyright permission (often choice 2):")
    return CopyrightPermission[int(PermissionChoice)]

def choose_media_policy():
    """ uses recommended permissions settings for oVert TCN """
    MediaPolicy = ["Media reuse policy not set",
    "CC0 - relinquish copyright",
    "Attribution CC BY - reuse with attribution",
    "Attribution-NonCommercial CC BY-NC - reuse but noncommercial",
    "Attribution-ShareAlike CC BY-SA - reuse here and applied to future uses",
    "Attribution- CC BY-NC-SA - reuse here and applied to future uses but noncommercial",
    "Attribution-NoDerivs CC BY-ND - reuse but no changes",
    "Attribution-NonCommercial-NoDerivs CC BY-NC-ND - reuse noncommerical no changes",
    "Media released for onetime use, no reuse without permission",
    "Unknown - Will set before project publication"]
    print()
    print()
    print()
    print("### Media Policy Options:")
    for i in range(len(MediaPolicy)):
        print(str(i) + ": " + MediaPolicy[i])
    PermissionChoice = input("Select media policy (oVert prefers 5, but check with your institution):")
    return MediaPolicy[int(PermissionChoice)]