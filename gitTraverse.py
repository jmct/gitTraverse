#! /usr/bin/env python
import argparse
import os
from subprocess import *

argParser = argparse.ArgumentParser(description='\
    This script allows you to collect all intermediate PDFs \
    for a LaTeX project from each commit in a git repository\'s history.')
argParser.add_argument('inputFile')
argParser.add_argument('-d', '--directory', nargs='?', default='gitTraversePDFs')
argParser.add_argument('latexBinary', nargs='?', default='pdflatex')
argParser.add_argument('latexFlags', nargs='?', default='-halt-on-error')

#Parse the arguments and instantiate object contatining argument values
args = argParser.parse_args()

#Give sensical names to each important argument.
command = args.latexBinary #The command to be run on each commit
flags = args.latexFlags    #Flags to pass to the latex builder
outputDir = '--output-directory=' +  args.directory
inputFile = args.inputFile

#The arguments for the git rev-list call
revList = ['git', 'rev-list', '--reverse', 'HEAD']

#The arguments in order to get the date of the current commit
commitDate = ['git', 'show', '-s', '--format=\"%ct\"']

#The list of SHA-1's that need to be checked-out
commitList = filter(None, check_output(revList).split("\n"))

#Ensure that the appropriate output directory is available
tempDir = os.path.dirname(args.directory + '/')
if not os.path.exists(tempDir):
    os.makedirs(tempDir)

for commit in commitList:
    check_output(['git', 'checkout', commit])
    outputFile = ('--jobname=' + check_output(commitDate)).rstrip()
    call([command, flags, outputFile, outputDir, inputFile])

#Cleanup and checkout master   
cleanupDir = args.directory + '/'
call('rm ' + cleanupDir + '*.aux', shell=True)
call('rm ' + cleanupDir + '*.log', shell=True)


check_output(['git', 'checkout', 'master'])
