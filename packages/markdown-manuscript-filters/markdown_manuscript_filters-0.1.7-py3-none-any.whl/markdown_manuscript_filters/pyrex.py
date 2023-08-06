import re
import sys


'''
PYthon RegEX 
applies regex to files using python
'''
#%%
# try things out interactively here: https://regex101.com/
#%%
def apply_pyrex(regex, subst, fnin, fnout=None, do_ignore_yaml=True, is_verbose=False):
    if isinstance(is_verbose,str):
        is_verbose = (is_verbose.lower() == "true") 
    if isinstance(do_ignore_yaml, str):
        do_ignore_yaml = (do_ignore_yaml.lower() == "true") 
    test_str = 'error, file not loaded'
    # test_str = '''
    # Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor
    # incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
    # nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
    # Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
    # fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
    # culpa qui officia deserunt mollit anim id est laborum.
    # 
    # Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    # 
    # Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor
    # incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
    # nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
    # Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
    # fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
    # culpa qui officia deserunt mollit anim id est laborum.
    # '''

    if fnin is None:
        str_in = test_str
    else:
        with open(fnin,'r') as f:
            str_in = f.read()
    if fnout is None:
        fnout = 'out.md'


    str_yaml = ''
    if do_ignore_yaml:
        yaml_split = str_in.split('---')
        str_yaml = '---'+''.join(yaml_split[:2])+'---'
        str_in ='\n'.join(yaml_split[2:])



    #%%
    # do the find and replace, matching 
    result = re.sub(regex, subst, str_in, 0, re.MULTILINE)
    matches = re.findall(regex,str_in)

    #%%
    if do_ignore_yaml:
        result = str_yaml + result
    #%%

    if is_verbose:
        print(f'reg:{repr(regex)}, sub:{subst}')
        # print(f'in:{fnin}, out:{fnout}')
        print(matches)
        print('.. substitution done ..\n') if result else print('no matches - no result')
        
    with open(fnout,'w+') as f:
        f.write(result)

# 
def unwrap(fnin,fnout=None,is_verbose=False):
    if fnout is None:
        #defaults to overwriting
        fnout=fnin
    # grab_wrapped_line_breaks = '(?=\w)(?<!\n)\n(\w)'
    # repl_with_space = r' \1'
    grab_wrapped_line_breaks ='([\w,.])\n(\w)'
    repl_with_space =r'\1 \2'
    apply_pyrex(grab_wrapped_line_breaks,repl_with_space,
        fnin=fnin,fnout=fnout,
        do_ignore_yaml=True,is_verbose=is_verbose)
    
def standardize_tex_math(fnin,fnout=None,delims=('\[','\]'),is_verbose=False):
    
    if fnout is None: fnout=fnin
    
    for delim in delims:
        apply_pyrex(re.escape(delim),'$$',
            fnin=fnin,fnout=fnout,
            do_ignore_yaml=True,is_verbose=is_verbose)

    
        
    
#%%
if __name__ == "__main__":
    fnin = None
    fnout = None
    do_ignore_yaml = True 
    is_verbose = None
    regex = r'(\w)'
    subst = r'\1'
    # python pryex `regex` `subst` `fnin` `fnout`

    if len(sys.argv)>1: regex = sys.argv[1]
    if len(sys.argv)>2: subst = sys.argv[2]
    if len(sys.argv)>3: fnin = sys.argv[3]
    if len(sys.argv)>4: fnout = sys.argv[4]
    if len(sys.argv)>5: is_verbose = sys.argv[5]
    
    apply_pyrex(regex=regex, subst=subst, 
        fnin=fnin, fnout=fnout, 
        do_ignore_yaml=do_ignore_yaml,is_verbose=is_verbose)