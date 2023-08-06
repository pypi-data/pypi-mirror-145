import sys
def remove_yaml(src,targ=None,is_verbose=False):
    '''
    put the yaml block from the top of one file at the top of the other 
    '''
    if targ is None:
        targ = src 
        
    with open(src,'r') as fsrc:
        
        content = fsrc.read()
        '''
        pastes the first yaml block, even if its not at the beginning of the source...
        '''
        sections = content.split('---')
        # print(sections[0])
        
        if len(sections) > 2:
            yaml_block = sections[1]
            yaml_block = f'---{yaml_block}---\n'
            src_content = ''.join(sections[2:])
        else:
            if is_verbose: print('no yaml to remove!')
            src_content = content
        src_content = src_content.lstrip('\n')
        # print(sections)
        
    with open(targ,'w') as ftarg:
        # targcontent = ftarg.read()
        ftarg.seek(0)
        ftarg.write(src_content)
        
#%%
def transplant_yaml(src,targ):
    with open(src,'r') as fsrc:
        
        content = fsrc.read()
        '''
        pastes the first yaml block, even if its not at the beginning of the source...
        '''
        sections = content.split('---')
        # print(sections[0])
        yaml_block = sections[1]
        yaml_block = f'---{yaml_block}---\n'
        
        if yaml_block:
            with open(targ,'r+') as ftarg:
                targcontent = ftarg.read()
                ftarg.seek(0)
                ftarg.write(yaml_block+targcontent)
