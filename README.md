gvl_commandline_utilities
=========================

Miscellaneous scripts useful for users of the GVL cloud images (CloudMan instances).

run_all.sh
----------

Run all other scripts with correct ordering and permissions.

Any utilities which need to be configured for all users will be configured (currently
only environment modules).

An ordinary user account called "researcher" will be created for non-admin use, 
and configured with the other utilities below.

Usage:
    
    sh run_all.sh
    

toolshed_to_modules.py
----------------------

Look for the env.sh scripts used to set up the environment for Galaxy Toolshed-installed 
tools, and use these to create module files. The resulting modules can be accessed 
using environment module commands such as `module avail` (see 
http://modules.sourceforge.net/man/module.html). Different modules should be available for 
different installed versions of the same tool. 

If a Toolshed-installed tool is uninstalled from Galaxy, running this script should
clean up the module file.

To use run:

    python toolshed_to_modules.py -h
    
Requires superuser permissions.

setup_user.sh
-------------

Run all scripts below which apply to an individual user. This script can be run multiple 
times to create and configure multiple non-sudo user accounts. 

Currently it will create the account; create home-directory symlinks to reference genomes 
and to galaxy; and configure an ipython notebook profile to run securely over the web.

Usage:

    sh setup_user.sh <username>

setup_ipython_server.py
-----------------------

Configure an ipython notebook profile to run the ipython notebook server including 
password-protection and SSL encryption. The notebook server, when running, will be
available on the port specified in this script (9510).

This script does not require sudo and can be run by an individual user to configure
IPython Notebook under their account. It should _not_ be run by the suduer account ubuntu, 
as it is dangerous to launch a notebook server from this account.

Usage (as the appropriate user):

    python setup_ipython_server.py

add_public_html.sh
------------------

Create a public_html directory and redirect for the specified user. 
This script must be run as superuser.

Usage:

    sudo sh add_public_html.sh <username>

This script assumes that you are using a GVL image with pre-configured port_forwarding,
i.e. an existing /usr/nginx/conf/port_forwarding.conf file configured into nginx.conf .

