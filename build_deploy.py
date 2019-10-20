import logging as log
import shutil
from shell_utils import shell

log.basicConfig(level=log.INFO, format='%(message)s')

def unitest():
    log.info('Running unit tests ...')
    print(shell('python -m unittest discover -s tests', capture=True, silent=True).stdout)

def build():
    log.info('Building package ...')
    shutil.rmtree('dist', ignore_errors=True)
    print(shell('python setup.py sdist bdist_wheel', capture=True, silent=True).stdout)

def check():
    log.info('Checking package ...')
    print(shell('twine check dist/*', capture=True, silent=True, check=False).stdout)

def doc():
    log.info('Generating documentation ...')
    print(shell('pdoc --force --html --output-dir docs datadict datadict.jupyter', capture=True, silent=True).stdout)

def publish(repository='testpypi'):
    log.info(f'Publishing package to {repository} ...')
    print(shell(f'twine upload --repository {repository} dist/*', capture=True, silent=True).stdout)