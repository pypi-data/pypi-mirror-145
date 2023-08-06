

import os
import subprocess


def _runCmd(cmd):
    subprocess_result = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE)
    subprocess_return = subprocess_result.stdout.read()
    return subprocess_return.decode('utf-8')


print(os.popen("git status").read())


print('-----------------')
print(_runCmd('git status -s') == '')
print('-----------------')
