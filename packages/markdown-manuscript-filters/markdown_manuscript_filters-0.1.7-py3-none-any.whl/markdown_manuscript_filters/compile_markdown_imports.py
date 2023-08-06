import re
import os

def f2str(fn):
    with open(fn,'r') as f:
        return f.read()

def find_in_subdir(name, path):
    if '/' in name:
        prepath = name.rsplit('/')[0]
        name = name.rsplit('/')[1]
        path = os.path.join(prepath,path)
        print('just getting last part of file name')
    # print(os.getcwd())
    # print(f' finding {name} in {path} .')
    for root, dirs, files in os.walk(path):
        # print(files)
        if name in files:
            # print('found')
            return os.path.join(root, name)
        else:
            print(os.getcwd())
            print(dirs)
            print(files)
            raise Exception(f'ERROR, cant find {name} in {path}')
    print(path)
    raise Exception('path contains no dirs')


def f2str_in_subdir(fn, start_dir='./'):
    fn = find_in_subdir(fn, start_dir)
    return f2str(fn)

def compile_markdown_imports(fnin,fnout=None, basedir='',is_recurse=False,is_verbose=False):        
    if fnout is None:
        fnout = fnin.replace('.md','_out.md')
    
    def import_str_to_file(imp_str):
        # not_a_comment = '(?<!'+re.escape('X')+')'
        
        #ONLY matches import statements at the beginning of lines
        find_imports = '^@import "(.*\.md)"'
        is_import = re.search(find_imports, imp_str)
        if "@import" in imp_str and not is_import:
            if is_verbose: 
                print('NOTE: import statement ignored')
                print(imp_str)
            
        if is_import:
            file_to_import = is_import.group(1)
            
            # #TOC imports
            # if '[TOC]' in file_to_import:
            #     return None
                
            return file_to_import
        else:
            return None

    fninin = fnin
    fnin = find_in_subdir(fnin, basedir)
    fnout = os.path.join(basedir,fnout) #write all output to basedir
    
    
    with open(fnin,'r') as f:
        with open(fnout,'w') as fo:
            lines = f.readlines()
            for L in lines:
                file_to_import = import_str_to_file(L)
                if file_to_import is not None:
                    if is_verbose: print('importing:',file_to_import)
                    # write comment describing where content came from
                    L = L.replace('@import','imported from').rstrip('\n')
                    L = f'<!--{L}-->\n'

                    basedir = basedir.rstrip('/')+'/'
                    full_file_to_import =  basedir+file_to_import.lstrip('/')
                    file_tail = full_file_to_import.rsplit('/',1)[1]
                    
                    # print(f'import_str: from {full_file_to_import}')
                    import_str = f2str(full_file_to_import)
                    '''
                    NOTE! this section assumes nested imports use relative paths
                    (needs double checking, cleaning up)
                    '''
                    if '@import' in import_str:
                        if is_verbose: print(f'\n\nRECURSIVE IMPORT -- {full_file_to_import} --')
                        relative_dir = file_to_import.rsplit('/',1)[0]+'/'
                        full_relative_dir = basedir+relative_dir
                        import_str = compile_markdown_imports(
                            fnin=file_tail,
                            basedir=full_relative_dir,
                            is_recurse=True)

                    L += import_str+f'\n<!-- end of import from "{file_tail}" -->\n'    
                    # print('success')
                fo.write(L)
    with open(fnout,'r') as fo:     
        if is_verbose: print('writing compiled file to :',fnout)   
        return fo.read()
#%%
if __name__ == "__main__":
    import sys
    f_in = 'manuscript_v1.md'
    f_out = 'publish/aux/mv1_out.md'
    basedir = '.'
    is_verbose = None
    if len(sys.argv)>0:
        if len(sys.argv)>1: f_in = sys.argv[1]
        if len(sys.argv)>2: f_out = sys.argv[2]
        if len(sys.argv)>3: basedir = sys.argv[3]
        if len(sys.argv)>5: is_verbose = sys.argv[4]

    compile_markdown_imports(fnin=f_in, fnout=f_out, basedir=basedir, is_verbose=is_verbose); 
