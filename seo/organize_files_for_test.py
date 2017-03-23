import sys
import os
import subprocess

def run_command(command):
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         shell=True)
    return iter(p.stdout.readline, b'')

if __name__=="__main__":
    folder = sys.argv[1]
    for folders in os.walk(folder):
        if not folders[1]:
            for file in folders[2]:
                file_name = folders[0]+"/"+file
                temp = folders[0]+"/temp.txt"

                command = "sort -t ':' -nk 2,2 "  + file_name+ " > " + temp

                for line in run_command(command):
                    print line

                os.remove(file_name)
                command="cp temp.txt "+file_name
                for line in run_command(command):
                    print line
                os.remove(temp)


