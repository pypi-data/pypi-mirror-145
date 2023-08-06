import sys,subprocess
subprocess.call(' '.join((sys.executable,'-m tbse',sys.argv[1:])))
