#!/usr/bin/env python
# encoding: utf-8

import getopt, sys
import os
import shutil

def usage():
    print 'Usage info:'

def is_already_linked(link_to_check, check_against_file):
    '''
    Determine if 'file' is actually a link to the dot-files directory
    '''
    if os.path.islink(link_to_check):
        if os.path.realpath(link_to_check) == check_against_file:
            return True
    return False

def is_dot_file(directory, item):
    if os.path.isfile(os.path.join(directory, item)):
        if item.startswith('.'):
            return !item.startswith('.git')
    return False

def link_files(home_dir, working_dir):
    for item in os.listdir(working_dir):
        home_file = os.path.join(home_dir, item)
        dot_file = os.path.join(working_dir, item)
        if is_dot_file(working_dir, item):
            if os.path.islink(home_file):
                os.remove(home_file)
            else:
                if is_dot_file(home_dir, item):
                    print 'Backing up: ' + home_file
                    shutil.move(home_file, home_file + '.bak')
            print 'Creating link: ' + dot_file + ' >> ' + home_file
            os.symlink(dot_file, home_file)
        else:
            print 'Skipping: ' +  dot_file

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:d:h", ["help", "output="])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
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
    if len(profile) > 0 && os.path.isdir(profile_dir):
        print 'Using profile: ' + profile
    else:
        print 'Profile \'' + profile + '\' does not exist'
        sys.exit(2)
    print 'Dotfiles directory: ' + working_dir
    link_files(home_dir, working_dir)
    if os.path.isdir(profile_dir):
        link_files(home_dir, profile_dir)

if __name__ == '__main__':
    main()
