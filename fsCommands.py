import os
import time

PFS_FILENAME = "private.pfs"

#generates current timestamp
def get_timestamp():
    return time.strftime("%Y%m%dT%H%M")

#mark a record as deleted
def mark_as_deleted(offset):
    with open(PFS_FILENAME, "r+b") as f:
        f.seek(offset)
        f.write(b"X")

# read all valid records (ignoring deleted entries marked 'X')
def read_all_records():
    records = []
    with open(PFS_FILENAME, "r") as f:
        for offset, line in enumerate(f):
            if not line.startswith("X"):
                records.append((offset, line.strip()))
    return records

# cp command 
def fs_cp(source, destination):
    """
    Copy from a normal or supplemental file to supplemental FS stored in private.pfs 
    """
    content = ''
    if source.startswith("+"):
        source = source[1:] #skip +
        found = False 
        with open(PFS_FILENAME, "r") as fs:
            for line in fs:
                if line.startswith("F|") and not line.startswith("X|"):
                    parts = line.strip().split("|")
                    if parts[1] == source:
                        content = parts[-1]
                        found = True
                        break 
        
        if not found:
            print(f"cp error: supplemental file '{source}' not found.")
            return 
    else:
        try:
            with open(source, "r") as normalFile:
                content = normalFile.read().strip()
        except FileNotFoundError:
            print(f"cp error: Normal file '{source}' not found.")
            return

    #create new supplemental file record 
    record = f"F|{destination[1:]}|{get_timestamp()}|{len(content)}|{content}\n" 

    with open(PFS_FILENAME, "a") as fs:
        fs.write(record)

    print(f"cp: copied to {destination}")
        
                        

    pass

# Command: show

def fs_show(file):
    """
    Display the content of a supplemental file
    """
    pass

# Command: merge

def fs_merge(file1, file2, destination):
    """
    Merge contents of two supplemental files into a new one
    """
    pass

# Command: rm

def fs_rm(file):
    """
    Mark a file as deleted in private.pfs
    """
    pass

# Command: mkdir

def fs_mkdir(directory_name):
    """
    Create a new directory record in private.pfs
    """
    pass

# Command: rmdir

def fs_rmdir(directory_name):
    """
    Remove a directory if it's empty
    """
    pass

# Command: ls

def fs_ls(target):
    """
    List file info or directory contents
    """
    pass
