from fabric.api import run, settings, sudo

__author__ = 'aj@springlab.co.'


def install_pip_packages():
    """ Instruct PIP to install required Python packages """
    sudo('pip install Yapsy==1.9.2')
    sudo('pip install SQLAlchemy==0.8.2')
    sudo('pip install openpyxl==1.6.2')


def setup():
    """ Configure execution environment, install dependencies, create an application directory """

    install_pip_packages()

