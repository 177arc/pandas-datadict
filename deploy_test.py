import subprocess

import logging as log
import shutil

def execute(cmd: str) -> int:
    process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
    while True:
        line = process.stdout.readline()
        if not line: break
        print(line.decode('utf-8').replace('\n', ''))

    return process.returncode

log.basicConfig(level=log.INFO, format='%(message)s')
log.info('Building package ...')
shutil.rmtree('dist', ignore_errors=True)
execute('python setup.py sdist bdist_wheel')

log.info('Checking package ...')
execute('twine check dist/*')

log.info('Generating documentation ...')
execute('pdoc --force --html --output-dir docs datadict datadict.jupyter')

log.info('Uploading package ...')
execute('twine upload --repository testpypi dist/*')
