from __future__ import print_function

import idaapi
import idautils
import idc
import sys

def GetFilePath():
    return "C:\\Games\\SkyrimMods\\RETools\\Data\\"

def IsUserName(ea):
    flags = ida_bytes.get_full_flags(ea)
    functionFlags = idc.get_func_attr(ea, idc.FUNCATTR_FLAGS)
    if ida_bytes.is_func(flags) and (functionFlags & idc.FUNC_LIB or functionFlags & idc.FUNC_THUNK):
        return False
    return ida_bytes.has_user_name(flags)

def IsAutoGenerated(value):
    if value.startswith("jpt_") or value.startswith("def_") or value.startswith("funcs_"):
        return True
    if value.find("__crt") != -1:
        return True
    if not value.startswith("??_") and value.find("@std") != -1:
        return True
    return False

def GetStr(num):
    return "%X" % num

if __name__ == '__main__':
    if idaapi.IDA_SDK_VERSION < 700:
        sys.exit("This script is not backwards compatible with IDAPython 6.x.")

    print("Beginning export\n")

    handle = open(GetFilePath() + "idanames.txt", "w")
    handle.truncate()
    for key, value in Names():
        if IsUserName(key) != True:
            continue
        if IsAutoGenerated(value):
            continue
        handle.write(GetStr(key))
        handle.write("\t")
        handle.write(value)
        handle.write("\t")
        name_str = idc.demangle_name(value, idc.get_inf_attr(INF_SHORT_DN))
        if name_str:
            handle.write(name_str)
        handle.write("\n")
    handle.close()

    print("Done with export\n")
