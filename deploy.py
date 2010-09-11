#!/usr/bin/env python
# encoding: utf-8
"""
deployer.py
Script for deployment of dot files using system specific profiles.

Created by Luke Kirkpatrick on 11-10-2010
"""

import getopt, sys
import os
import shutil

# Print help message
def usage():
    print 'Usage: python deployer.py [options]'
    print 'Options:'
    print '\t-d, --directory Path to dot files directory if not current directory'
    print '\t-h, --help Print this message and exit'
    print '\t-p, --profile Profile folder, files in this folder will override default files'
    print 'Report bugs to <byakuya41@gmail.com>'

# Check file is a valid dot file
def is_dot_file(directory, item):
    if os.path.isfile(os.path.join(directory, item)):
        if item.startswith('.'):
            return not item.startswith('.git')
    return False

# Create links for all dot files in directory
def link_files(home_dir, working_dir):
    for item in os.listdir(working_dir):
        home_file = os.path.join(home_dir, item)
        dot_file = os.path.join(working_dir, item)
        if is_dot_file(working_dir, item):
            if os.path.islink(home_file):
                '''
                Remove if is existing symlink
                '''
                os.remove(home_file)
            else:
                if is_dot_file(home_dir, item):
                    '''
                    Backup existing file
                    '''
                    print 'Backing up: ' + home_file
                    shutil.move(home_file, home_file + '.bak')
            '''
            Create symlink
            '''
            print 'Linking ' + dot_file + ' >> ' + home_file
            os.symlink(dot_file, home_file)

#main
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:d:h", ["help", "output="])
    except getopt.GetoptError, err:
        '''
        print help then exit
        '''
        print str(err)
        usage()
        sys.exit(2)
    
    profile = ''
    home_dir = os.path.expanduser('~')
    working_dir = os.getcwd()

    for opt, arg in opts:
        if opt in ("-p", "--profile"):
            profile = arg
        elif opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-d", "--directory"):
            working_dir = arg
        else:
            assert False, "unhandled option"
    profile_dir = os.path.join(working_dir, profile)
    print '-- Dotfile Deployment --'
    if len(profile) > 0:
        if os.path.isdir(profile_dir):
            print 'Using profile: ' + profile
        else:
            print 'Profile \'' + profile + '\' does not exist'
            sys.exit(2)
    print 'Dotfiles directory: ' + working_dir
    print '------------------------'
    link_files(home_dir, working_dir)
    '''
    If a profile was used, link the files from the profile
    '''
    if os.path.isdir(profile_dir):
        link_files(home_dir, profile_dir)

if __name__ == '__main__':
    main()
