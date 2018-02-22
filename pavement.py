import os

from paver.easy import *


@task
def develop():
    sh('pip install -r requirements.txt')
    sh('python setup.py develop')


@task
def dependency_compile():
    sh('pip-compile --generate-hashes '
       '--output-file requirements.txt requirements.in')


@task
def dependency_upgrade():
    sh('pip-compile --generate-hashes --upgrade '
       '--output-file requirements.txt requirements.in')
    sh('pip install -r requirements.txt')


@task
def test():
    sh('py.test -s tests/')


@task
def lint():
    sh('flake8 jsom')


@task
def build():
    call_task('test')
    call_task('lint')
