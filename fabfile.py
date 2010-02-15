import os

import fabric.api as _fab
from fabric.contrib.console import confirm

_fab.env.hosts = ['eventrevolution.net']

def test():
    print "No tests yet"

def do_del_tmp():
    """Remove temporary files from the project dir"""
    _fab.local("find %s -name '*.pyc' -depth -delete" % (
        os.path.dirname(__file__),))
    _fab.local("find %s -name '.*sw*' -depth -delete" % (
        os.path.dirname(__file__),))

def pack():
    
    do_del_tmp()
    _fab.local('cd ./$(git rev-parse --show-cdup) && git archive --prefix="conman/" --format=tar HEAD | gzip > /tmp/conman_head.tar.gz')
    # can do tags and versions too
    #_fab.local('cd ./$(git rev-parse --show-cdup) && git archive --prefix=conman-$(git-version)/" --format=tar v1.4.0 | gzip > /tmp/conman_head.tar.gz')

def prepare_deploy ():
    # run tests
    test()
    pack()

def _put_and_expand():
    _fab.put('/tmp/conman_head.tar.gz', '/tmp')
    with _fab.cd('/var/www/er.net/www/'):
        _fab.run('tar xf /tmp/conman_head.tar.gz')

def do_deps():
    _fab.run('wget http://sorl-thumbnail.googlecode.com/files/sorl-thumbnail-3.2.5.tar.gz -O /tmp/sorl-thumbnail-3.2.5.tar.gz')
    _fab.run("tar xf /tmp/sorl-thumbnail-3.2.5.tar.gz -C /tmp")
    with _fab.cd('/tmp/sorl-thumbnail-3.2.5/'):
        _fab.sudo("python setup.py install")

def do_sync_db():
    with _fab.cd('/var/www/er.net/www/'):
        _fab.run('./manage.py syncdb')

def do_httpd_restart():
    _fab.sudo('/etc/init.d/httpd restart')

def deploy_develop():
    """Deploy the latest conman release from HEAD"""
    _put_and_expand()
    _build_new_db()
    httpd_restart()

