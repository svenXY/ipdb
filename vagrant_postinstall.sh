# install and configure python 2.7 and some modules

PYTHONVER='2.7.6'
DISTRIBVER='0.7.3'

if [ ! "$USER" == "vagrant" ]; then
	echo "Please only ever run this within vagrant as user vagrant"
	exit 99
fi

export PATH=$PATH:/usr/local/bin
cd

echo "Install devel packages with sudo yum..."
sudo yum install -y zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel wget git vim

if [ ! -f /usr/local/bin/python2.7 ]; then
	echo "Install python2.7"
	wget http://python.org/ftp/python/${PYTHONVER}/Python-${PYTHONVER}.tar.bz2
	tar xf Python-${PYTHONVER}.tar.bz2
	cd Python-${PYTHONVER}
	./configure --prefix=/usr/local
	make && sudo make altinstall
        cd .. 
	rm -rf Python-${PYTHONVER}
fi

if [ ! -f /usr/local/bin/easy_install-2.7 ]; then
	echo "Install distribute"
	wget --no-check-certificate http://pypi.python.org/packages/source/d/distribute/distribute-${DISTRIBVER}.tar.gz
	tar xf distribute-${DISTRIBVER}.tar.gz
	cd distribute-${DISTRIBVER}
	sudo /usr/local/bin/python2.7 setup.py install
        cd .. 
        rm -rf distribute-${DISTRIBVER}
fi

if [ ! -f /usr/local/bin/virtualenv-2.7 ]; then
	sudo /usr/local/bin/easy_install-2.7 virtualenv
fi

if [ ! -d $HOME/django ]; then
	/usr/local/bin/virtualenv-2.7  $HOME/django
fi

source $HOME/django/bin/activate

pip install Django
pip install django-mptt
pip install ipaddress
pip install ipython

echo "All set up, now type 'source $HOME/django/bin/activate' to activate the new virtualenv"
