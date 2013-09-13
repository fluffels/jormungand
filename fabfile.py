from fabric.api import run, settings, sudo, env, cd

__author__ = 'aj@springlab.co.'


def staging():
    """
    Set env parameters for the staging environment.
    """

    env.hosts = ['197.221.50.178']
    env.envname = 'staging'
    env.user = 'root'
    env.group = 'root'
    env.working_dir = '~/data-extraction'
    print("STAGING ENVIRONMENT\n")


def setup():
    """ Configure execution environment, install dependencies, create an application directory """

    with settings(warn_only=True):
        if run("test -d %s" % env.working_dir).failed:
            run('mkdir %s' % env.working_dir)

    # Install basic system packages
    sudo('apt-get install git')

    with cd(env.working_dir):
        run('git clone https://github.com/OOPMan/extraction.git')


def update():
    """
    """
    with cd(env.working_dir):
        with cd('extraction'):
            run('git pull --rebase')

