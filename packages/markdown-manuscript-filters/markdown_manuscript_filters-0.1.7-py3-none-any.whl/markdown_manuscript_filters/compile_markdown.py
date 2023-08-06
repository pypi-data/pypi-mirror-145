#!/usr/bin/env python3

"""
Converts markdown with @import statements to all-in-one markdown file 
- then filters out common annotation 
- then converts to pdf with pandoc
"""

import sys, os
import yaml_funs as yf
import compile_markdown_imports as cmi
import pyrex
import latex_to_speech

import subprocess
import shlex
import argparse
import shutil


from termcolor import colored
#%%

do_open_pdf_if_successful = False #-o
is_verbose = True #-v
do_halt_on_err = True #-e
do_halt_on_warn = False

start_dir = './'
aux_dir = 'publish/aux/'
out_dir = 'publish/output/'
# filter_dir = 'publish/scripts/'

manu = 'manuscript_v1'
mv = 'mv1'

is_run_from_commandline = False
#%%
try:
    __IPYTHON__
    # if running from this script, modify path to be relative
    start_dir = '../tests/'
    is_run_from_commandline = False
except:
    is_run_from_commandline = True
    # print(colored('not in IPython','blue'))
    pass
#%%
# PROCESS command line arguments
# inspired by: https://gist.github.com/nhoffman/3006600
args_in = sys.argv[1:]

if is_run_from_commandline and len(sys.argv) > 1:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument('src_file',  help='source markdown file (with @imports)',type=str)
    parser.add_argument('--dir',   help='starting directory',type=str)
    parser.add_argument('--aux',   help='directory for auxiliary files',type=str)
    parser.add_argument('--out',   help='directory for outputs (i.e. pdf)',type=str)
    parser.add_argument('--filter',help='directory for pandoc/panflute filters',type=str)

    parser.add_argument('-p',action='store_true',       help='open (p)df after successful compile')
    parser.add_argument('-v',action='store_true',       help='(v)erbose')
    parser.add_argument('-e',action='store_true',       help='halt (e)xecution if a step errors')
    parser.add_argument('-w',action='store_true',       help='halt execution if any (w)arnings -- implies -e')
    parser.add_argument('-f',action='store_true',       help='filter out annotations from file')
    # parser.add_argument('-c',action='store_true',       help='(c)lean aux files after running')


    
    args = parser.parse_args()
    
    if args.src_file: 
        manu = args.src_file.rstrip('.md')
        mv = manu[0]+manu[-2]+manu[-1]
    if args.dir: start_dir = args.dir
    if args.aux: aux_dir = args.aux
    if args.out: out_dir = args.out
    
    # flags
    if args.v: 
        is_verbose = True 
    else:
        is_verbose = False
        
    do_halt_on_err = True if args.e else False
    if args.w:
        do_halt_on_warn = True 
        do_halt_on_err = True
    else:
        do_halt_on_warn = False

    do_open_pdf_if_successful = True if args.p else False

    
#%%    


manu_out = f'{mv}_out.md'
manu_filt = f'{mv}_filtered.md'

src_doc = f'{manu}.md'
compiled_doc = aux_dir+manu_out
filtered_doc = aux_dir+manu_filt
pdf_doc = out_dir+f'{manu}.pdf'

#%%

def start(path):
    return start_dir+path

def __run_in_shell(cmd, fail_on_warn=do_halt_on_warn):
    '''
    TODO: need to triple check this for security vulnerabilities... 
    - should sanitize command if possible
    '''
    res = subprocess.run(shlex.split(cmd),capture_output=True)
    if res.stdout:
        print(res.stdout.decode("utf-8"))
    if res.stderr:
        print(colored(res.stderr.decode("utf-8"),'yellow',attrs=['bold']))
        
        if fail_on_warn:
            return False 
        
        # if not fail_on_warn, check all lines are /only/ warnings
        # fail on anything else    
        for a_line in res.stderr.decode("utf-8").splitlines():
            if '[WARNING]' not in a_line:
                print('non warning output:')
                print(a_line)
                return False
        # at this point everything was probably a warning, might be fine to ignore
        return True
            
    else:
        return True
        
def __open_pdf(pdf_path):
    subprocess.Popen(f'open {pdf_path}', shell=True)
def __print_then_exit(warn):
    print(colored(warn,'red',attrs=['bold']))
    raise Exception(warn)

#%%
if is_verbose: print('.. compiling @imports ..')
cmi.compile_markdown_imports(fnin=src_doc, fnout=compiled_doc,
    basedir=start_dir, is_verbose=is_verbose)

# if is_verbose: print('.. re-adding yaml ..')
# yf.transplant_yaml(start(src_doc), start(compiled_doc))

if args.f:
    pyrex.standardize_tex_math(fnin=start(compiled_doc))

# Concatenated markdown file → clean, minimal, human-readable markdown
# math_render = '+tex_math_double_backslash' # doesnt seem to do anything...

math_render = ''

pandoc_compile_to_filtered = f'pandoc -f markdown+yaml_metadata_block{math_render} '
if args.f:
    # hacky ... relies on relative location of modules cleanup_filter 
    filter_path = __file__.rsplit('/',1)[0]+'/panflute/cleanup_filter.py'
    pandoc_compile_to_filtered+= f'--filter={filter_path} '
pandoc_compile_to_filtered+= f'-o {start(filtered_doc)} {start(compiled_doc)}'

if is_verbose:
    print('.. filtering markdown with pandoc:')
    print('   '+pandoc_compile_to_filtered)

filter_worked = __run_in_shell(pandoc_compile_to_filtered)
if is_verbose:
    if not filter_worked:
        print(colored("!! WARNING: filtering markdown failed !!",'red'))
        
if do_halt_on_err and not filter_worked:
    # raise Exception('!! filtering markdown failed !! -- exiting...')
    __print_then_exit('!! filtering markdown failed !! -- exiting...')

if is_verbose: print('.. re-adding yaml, again ..')
yf.transplant_yaml(start(src_doc), start(filtered_doc))

# undo softwrap - calls pyrex 
if is_verbose: print('.. undoing line wrap ..')
pyrex.unwrap(start(filtered_doc),is_verbose=False)


#%%
if is_verbose: print('.. starting pdf conversion with pandoc ..')
import re

pandoc_filtered_to_pdf = f'pandoc -f markdown{math_render} -o {start(pdf_doc)} --pdf-engine=xelatex {start(filtered_doc)}'
if is_verbose:
    print('   '+pandoc_filtered_to_pdf)
pdf_worked = __run_in_shell(pandoc_filtered_to_pdf)

if is_verbose:
    if pdf_worked:
        print(colored(f"☼☼ PDF export complete ☼☼\n☼☼ available at {start(pdf_doc)} ☼☼",'green',attrs=['bold']))
    else:
        print(colored("!! WARNING: pdf export failed !!",'red'))
        if do_halt_on_err:
            __print_then_exit("!! WARNING: pdf export failed !! -- exiting..")
            
if do_open_pdf_if_successful and pdf_worked:
    __open_pdf(start(pdf_doc))

#%%

