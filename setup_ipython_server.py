
"""
Set up an ipython notebook profile for use over the web on GVL servers.

After running this script, change to your project directory and run

   ipython notebook --profile=nbserver

For security, you should not launch ipython notebook from your home directory, 
as it will have access to files in the directory tree it is run from.
Create a notebook or project directory and launch it from there.

This script will:
* Create a profile (nbserver) to use for the notebook server
* Configure password protection
* Configure HTTPS encryption
* Configure port settings
* Install the Table of Contents plugin
"""

##
# Clare Sloggett, VLSCI, University of Melbourne
# Authored as part of the Genomics Virtual Laboratory project
##

# TODO: at end, tell user how to use
# TODO: add Table of Contents plugin
# TODO: set up readonly as well as interactive server

import os
import IPython.lib
import logging
import subprocess
import stat

profile_name = "nbserver"
interactive_port =  9510
readonly_port = 9560
interactive_location = "/ipython"

profile_config = \
"""
# Configuration file for ipython, intended for notebook server. 
# Generated by GVL setup script.

c = get_config()

# Kernel config
c.IPKernelApp.pylab = 'inline'  # plotting support by default

# Do not open local browser, just run as a server
c.NotebookApp.open_browser = False

# Require password access. 
c.NotebookApp.password = u'{hash}'

# Use a known port, which needs to be open in the security group
c.NotebookApp.port = {port}
c.NotebookApp.port_retries = 0

# Currently we are accessing the notebook directly via open ports.
# We need to do encryption and listen on external interfaces
c.NotebookApp.ip = '*'
c.NotebookApp.certfile = u'{certfile}'
c.NotebookApp.keyfile = u'{keyfile}'
"""

def main():
    """ The body of the script. """

    # Initialise logging to print info to screen
    logging.basicConfig(level=logging.INFO)

    # Get locations
    ipython_dir = IPython.utils.path.get_ipython_dir()
    nginx_dir = "/usr/nginx/conf"
    nginx_conf = os.path.join(nginx_dir, "nginx.conf")

    # Create the nbserver profile
    logging.info("Creating ipython profile for "+profile_name)
    profile_dir = os.path.join(ipython_dir, "profile_"+profile_name)
    run_cmd("ipython profile create "+profile_name)
    #profile_dir = IPython.core.profiledir.ProfileDir.create_profile_dir_by_name(ipython_dir, profile_name)

    # Ask the user for a password; only store the hash
    logging.info("Configuring password")
    print "Enter a password to use for ipython notebook web access:"
    password_hash = IPython.lib.passwd()
    
    # Generate a self-signed certificate
    # We require superuser to write to the config directory
    logging.info("Generating self-signed certificate for SSL encryption")
    certfile_tmp = "./instance_selfsigned_cert.pem.tmp"
    keyfile_tmp = "./instance_selfsigned_key.pem.tmp"
    certfile = os.path.join(profile_dir, "instance_selfsigned_cert.pem")
    keyfile = os.path.join(profile_dir, "instance_selfsigned_key.pem")
    run_cmd("yes '' | openssl req -x509 -nodes -days 3650 -newkey rsa:1024 -keyout "+keyfile_tmp+" -out "+certfile_tmp)
    run_cmd("sudo mv "+certfile_tmp+" "+certfile)
    run_cmd("sudo mv "+keyfile_tmp+" "+keyfile)
    run_cmd("sudo chmod 440 "+keyfile)
    
    # Overwrite the default profile config with ours
    config_file = os.path.join(profile_dir, "ipython_notebook_config.py")
    logging.info("Writing nbserver config file "+config_file)
    with open(config_file, 'wb') as f:
        f.write(profile_config.format(hash = password_hash, 
                                      port = interactive_port, 
                                      location = interactive_location,
                                      certfile = certfile,
                                      keyfile = keyfile))

def run_cmd(command):
    """ Run a shell command. """
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process.communicate()  

if __name__ == "__main__":
    main()
    
