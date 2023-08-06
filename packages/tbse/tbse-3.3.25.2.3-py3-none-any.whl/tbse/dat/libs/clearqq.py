import os

def clearqq():
    try:
        for root,dirs,files in os.walk("/sdcard"):
            for file in files:
                tn=file.split(os.sep)[-1]
                tn=tn.split(".")[-1]
                if tn.lower() in ("log","tmp","_mp","gid","chk","old","bak","xlk","cache","temp","lock"):
                    try:
                        os.remove(os.path.join(root,file))
                        print(f"\r\033[95;1mSuccessfuly\033[0m: remove file {os.path.join(root,file)} [COUNT {successfuly}]")
                        try:
                            os.rmdir(root)
                            print(f"\r\033[95;1mSuccessfuly\033[0m: remove directory {root} [COUNT {successfuly}]")
                        except:
                            pass
                    except:
                        print(f"\r\033[91;1mFailed\033[0m: cannot remove {os.path.join(root,file)}")
                elif "/sdcard/Android/" in root: # and tn in ("log","tmp","_mp","gid","chk","old","bak","xlk","cache","temp","lock","jpg","jpeg","mp4","png","webp","gif","mp3","xml","json","dat","db","so","txt",'',"yml"):
                    try:
                        os.remove(os.path.join(root,file))
                        print(f"\r\033[95;1mSuccessfuly\033[0m: remove file {os.path.join(root,file)} [COUNT {successfuly}]")
                        try:
                            os.rmdir(root)
                            print(f"\r\033[95;1mSuccessfuly\033[0m: remove directory {root} [COUNT {successfuly}]")
                        except:
                            pass
                    except:
                        print(f"\r\033[91;1mFailed\033[0m: cannot remove {os.path.join(root,file)}")
    except:pass