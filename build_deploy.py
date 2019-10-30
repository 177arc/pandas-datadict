import logging as log
import glob, os
from shell_utils import shell

log.basicConfig(level=log.INFO, format='%(message)s')

def __execute(command: str):
    return print(shell(command, capture=True, silent=True).stdout)

def unitest():
    log.info('Running unit tests ...')
    __execute('python -m pytest tests/')

def install():
    log.info('Installing package locally ...')
    __execute('pip install .')

def build():
    log.info('Building package ...')
    map(lambda x: os.remove(x), glob.glob('dist/*'))
    __execute('python setup.py sdist bdist_wheel')

def check():
    log.info('Checking package ...')
    __execute('twine check dist/*')

def doc():
    log.info('Generating documentation ...')
    __execute('pdoc --force --html --output-dir docs datadict datadict.jupyter')

def publish(repository='testpypi'):
    log.info(f'Publishing package to {repository} ...')
    __execute(f'twine upload --repository {repository} dist/*')