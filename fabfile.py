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
    sudo('apt-get install python-pip')
    sudo('apt-get install python-virtualenv')

    with cd(env.working_dir):
        run('virtualenv -p /usr/bin/python2.7 ENV_extraction')
        run('ENV_extraction/bin/pip install Yapsy==1.9.2')
        run('ENV_extraction/bin/pip install SQLAlchemy==0.8.2')

