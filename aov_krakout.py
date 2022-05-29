import nuke,os,fnmatch
from difflib import SequenceMatcher

#aov_krakout
#Creates a tree of lightgroups or illumination passes and recombines them
#https://github.com/dharkness/aov_krakout
#v007 @dharkness 2022-05-29

class aov_tree:
    def __init__(self, aov, xy, dir_mult, x_offset, y_offset_small, y_offset_large, x_offset_mult, is_last_tree=None, orphan_buffer=None):
        self.aov = aov
        self.div_aov = None
        self.mult_aov = None
        self.x_offset_mult = 1 
        if aov:        
            if '/' in aov:
                self.div_aov = aov.split('/')[1]
                self.mult_aov = aov.split('/')[1]
                self.aov = aov.split('/')[0]
                self.x_offset_mult = x_offset_mult
            if '^' in aov:
                self.mult_aov = aov.split('^')[1]
                self.aov = aov.split('^')[0] 
                self.x_offset_mult = x_offset_mult
        self.x = xy[0]
        self.y = xy[1] 
        self.dir_mult=dir_mult
        self.x_offset = x_offset
        self.y_offset_small = y_offset_small
        self.y_offset_large = y_offset_large
        if is_last_tree == None:
            is_last_tree = False  
        self.is_last_tree = is_last_tree
        if orphan_buffer == None:
            orphan_buffer = False
        self.orphan_buffer=orphan_buffer    
        self.top_input = None
        self.top_output = None
        self.subtract_node = None
        self.bottom_output = None
        if self.aov: 
            self.build_aov_tree()
        else:
            self.build_orphan_tree()
        
    def build_aov_tree(self):
        pref = nuke.toNode('preferences')
        ds=int(pref['dot_node_scale'].value())*6
        tw=int(pref['TileWidth'].value())
        th=int(pref['TileHeight'].value())
        x_offset = 0
        
        if self.x_offset_mult!=1:
            self.x=self.x-self.x_offset*self.x_offset_mult
            self.x_offset = self.x_offset*self.x_offset_mult       
        tx=int(self.x-tw/2)
               
        if self.mult_aov:
            self.top_input = nuke.nodes.Dot(xpos=self.x-ds,ypos=self.y-ds)
            x_offset = self.x_offset
        self.top_output = nuke.nodes.Dot(xpos=self.x+x_offset-ds,ypos=self.y-ds)
        if self.mult_aov: self.top_output.setInput(0,self.top_input)
        if not self.mult_aov: self.top_input=self.top_output
        
        shuffle_out = nuke.nodes.Shuffle(xpos=tx+x_offset, ypos=self.top_input.ypos()+self.y_offset_small+ds)
        shuffle_out['label'].setValue('<b>[value in] -> [value out]')
        shuffle_out['in'].setValue(self.aov)
        shuffle_out['out'].setValue('rgb')
        shuffle_out.setInput(0,self.top_output)
        shuffle_out.setYpos(int(shuffle_out.ypos()-th+shuffle_out.screenHeight()))
    
        unpremult = nuke.nodes.Unpremult( xpos=tx+x_offset, ypos=int(shuffle_out.ypos()+self.y_offset_small+th/2))
        unpremult.setInput(0,shuffle_out)
        self.subtract_node = unpremult
        
        if self.orphan_buffer:
            unp_dot = nuke.nodes.Dot( xpos=self.x+x_offset-ds, ypos=unpremult.ypos()+self.y_offset_small+ds/2)
            unp_dot.setInput(0,unpremult)
            unp_exit_node=unp_dot
        else:
            unp_exit_node=unpremult    
        
        if self.mult_aov:    
            if self.div_aov:
                div_merge = nuke.nodes.Merge2( xpos=tx+x_offset, ypos=unp_exit_node.ypos()+self.y_offset_small)
                div_merge['operation'].setValue('divide')
                div_merge['Achannels'].setValue('rgb')
                div_merge['Bchannels'].setValue('rgb')
                div_merge['output'].setValue('rgb')
                div_merge.setInput(1,unp_exit_node)            
                
                divmult_shuffle_out = nuke.nodes.Shuffle(xpos=tx, ypos=self.top_input.ypos()+self.y_offset_small+ds)
                divmult_shuffle_out['label'].setValue('<b>[value in] -> [value out]')
                divmult_shuffle_out['in'].setValue(self.div_aov)
                divmult_shuffle_out['out'].setValue('rgb')
                divmult_shuffle_out.setInput(0,self.top_input)
                divmult_shuffle_out.setYpos(int(divmult_shuffle_out.ypos()-th+divmult_shuffle_out.screenHeight()))
            
                divmult_unpremult = nuke.nodes.Unpremult( xpos=tx, ypos=int(divmult_shuffle_out.ypos()+self.y_offset_small+th/2))
                divmult_unpremult.setInput(0,divmult_shuffle_out)
                
                div_dot = nuke.nodes.Dot( xpos=self.x-ds, ypos=div_merge.ypos()+ds/2)
                div_dot.setInput(0,divmult_unpremult)
                div_merge.setInput(0,div_dot)                                        
            else:
                divmult_shuffle_out = nuke.nodes.Shuffle(xpos=tx, ypos=self.top_input.ypos()+self.y_offset_small+ds)
                divmult_shuffle_out['label'].setValue('<b>[value in] -> [value out]')
                divmult_shuffle_out['in'].setValue(self.mult_aov)
                divmult_shuffle_out['out'].setValue('rgb')
                divmult_shuffle_out.setInput(0,self.top_input)
                divmult_shuffle_out.setYpos(int(divmult_shuffle_out.ypos()-th+divmult_shuffle_out.screenHeight()))
            
                divmult_unpremult = nuke.nodes.Unpremult( xpos=tx, ypos=int(divmult_shuffle_out.ypos()+self.y_offset_small+th/2))
                divmult_unpremult.setInput(0,divmult_shuffle_out)
             
        inject_aov=self.aov             
        if not self.div_aov and self.mult_aov:
            match=SequenceMatcher(None, self.aov, self.mult_aov).find_longest_match(0, len(self.aov), 0, len(self.mult_aov))
            inject_aov=self.aov[match.a:match.a + match.size]
            
        shuffle_in = nuke.nodes.Shuffle(xpos=tx+x_offset, ypos=unp_exit_node.ypos()+self.y_offset_large+ds)
        shuffle_in['label'].setValue('<b>[value in] -> [value out]')
        shuffle_in['out'].setValue(inject_aov)
        shuffle_in['in'].setValue('rgb')
        shuffle_in.setInput(0,unp_exit_node)
        if self.div_aov: shuffle_in.setInput(0,div_merge)
        shuffle_in.setYpos(int(shuffle_in.ypos()-th+shuffle_in.screenHeight()))
    
        premult = nuke.nodes.Premult( xpos=tx+x_offset, ypos=shuffle_in.ypos()+self.y_offset_small+th/3)
        premult['channels'].setValue(inject_aov)
        premult.setInput(0,shuffle_in)
        
        if self.is_last_tree:
            self.bottom_output = nuke.nodes.Remove( xpos=tx+x_offset, ypos=premult.ypos()+self.y_offset_small-th*0.1)
            self.bottom_output['operation'].setValue('keep')
            self.bottom_output['channels'].setValue('rgba')
            self.bottom_output['label'].setValue('keep [value channels]')            
            self.bottom_output.setInput(0,premult)
        else:
            self.bottom_output = nuke.nodes.Merge2( xpos=tx+x_offset, ypos=premult.ypos()+self.y_offset_small-th*0.1)
            self.bottom_output['operation'].setValue('plus')
            self.bottom_output['Achannels'].setValue('rgb')
            self.bottom_output['Bchannels'].setValue('rgb')
            self.bottom_output['output'].setValue('rgb')
            self.bottom_output['also_merge'].setValue(inject_aov)
            self.bottom_output['label'].setValue('also [value also_merge]')            
            self.bottom_output.setInput(1,premult)
            
        if self.mult_aov:
            mult_merge = nuke.nodes.Merge2( xpos=tx+x_offset, ypos=shuffle_in.ypos()-self.y_offset_small+th/2)
            mult_merge['operation'].setValue('multiply')
            mult_merge['Achannels'].setValue('rgb')
            mult_merge['Bchannels'].setValue('rgb')
            mult_merge['output'].setValue('rgb')
            mult_merge.setInput(0,unp_exit_node)
            if self.div_aov: mult_merge.setInput(0,div_merge)
            shuffle_in.setInput(0,mult_merge)
            
            mult_dot = nuke.nodes.Dot( xpos=self.x-ds, ypos=mult_merge.ypos()+ds/2)
            mult_merge.setInput(1,mult_dot)
            mult_dot.setInput(0,divmult_unpremult)
            if self.div_aov: mult_dot.setInput(0,div_dot)
            if not self.div_aov: self.subtract_node=mult_merge
    
    def build_orphan_tree(self):
        pref = nuke.toNode('preferences')
        ds=int(pref['dot_node_scale'].value())*6
        tw=int(pref['TileWidth'].value())
        th=int(pref['TileHeight'].value())
        tx=int(self.x+(tw/2)*self.dir_mult)
       
        self.top_output = nuke.nodes.Dot(xpos=self.x-ds,ypos=self.y-ds)
        self.top_input=self.top_output
        
        shuffle_out = nuke.nodes.Shuffle(xpos=tx, ypos=self.top_input.ypos()+self.y_offset_small+ds)
        shuffle_out['label'].setValue('<b>[value in] -> [value out]')
        shuffle_out['in'].setValue('rgb')
        shuffle_out['out'].setValue('rgb')
        shuffle_out.setInput(0,self.top_output)
        shuffle_out.setYpos(int(shuffle_out.ypos()-th+shuffle_out.screenHeight()))
    
        unpremult = nuke.nodes.Unpremult( xpos=tx, ypos=int(shuffle_out.ypos()+self.y_offset_small+th/2))
        unpremult.setInput(0,shuffle_out)
        
        self.subtract_node = nuke.nodes.Merge2( xpos=tx, ypos=unpremult.ypos()+self.y_offset_small)
        self.subtract_node['operation'].setValue('from')
        self.subtract_node['Achannels'].setValue('rgb')
        self.subtract_node['Bchannels'].setValue('rgb')
        self.subtract_node['output'].setValue('rgb')
        self.subtract_node['hide_input'].setValue(True)
        self.subtract_node.setInput(0,unpremult)
                           
        self.bottom_output = nuke.nodes.Merge2( xpos=tx, ypos=self.subtract_node.ypos()+self.y_offset_large+self.y_offset_small*2-th*0.2)
        self.bottom_output['operation'].setValue('plus')
        self.bottom_output['Achannels'].setValue('rgb')
        self.bottom_output['Bchannels'].setValue('rgb')
        self.bottom_output['output'].setValue('rgb')
        self.bottom_output['label'].setValue('orphan aovs')            
        self.bottom_output.setInput(1,self.subtract_node)
            
class aov_krakout:
    def __init__(self, kn, dir_mult=None, x_offset=None, y_offset_small=None, y_offset_large=None, x_offset_mult=None, subtract_aovs=None):
        self.kn=kn
        pref = nuke.toNode('preferences')        
        if dir_mult is None:
            dir_mult=-1
        self.dir_mult=dir_mult
        if x_offset is None:
            x_offset=2*pref['GridWidth'].value()
        self.x_offset=x_offset*dir_mult
        if y_offset_small is None:
            y_offset_small=3*pref['GridHeight'].value()
        self.y_offset_small=y_offset_small
        if y_offset_large is None:
            y_offset_large=10*pref['GridHeight'].value()
        self.y_offset_large=y_offset_large
        if x_offset_mult is None:
            x_offset_mult=1
        self.x_offset_mult=x_offset_mult
        if subtract_aovs is None:
            subtract_aovs=False
        self.subtract_aovs=subtract_aovs
        self.aov_list=[]
        self.aov_trees=[]

    def resolve_envvars(self, pattern):
        loop_pattern=''
        for p in pattern.replace(' ','').split(','):
            if p[0] == '$':
                if p[1:] in os.environ:
                    loop_pattern = '{0},{1}'.format(loop_pattern,os.getenv(p[1:]))
            else:
                loop_pattern = '{0},{1}'.format(loop_pattern,p)
        return loop_pattern[1:]
            
    def set_aovs_from_pattern(self, pattern):
        print('\n')
        pattern = self.resolve_envvars(pattern)
        
        #---- fetch all layers (aovs) in the node
        all_channels = self.kn.channels()
        all_layers = list( set([c.split('.')[0] for c in all_channels]) )
        all_layers.sort()
        
        ret_match_layers = []
        ret_not_match_layers = []
        for p in pattern.replace(' ','').split(','):
            #---- find the layers we want to break out
            if len(p.split('/')[0].split('^')) == 1:
                match_layers = fnmatch.filter(all_layers, p)
                if len(match_layers) : print ("+ match >> {0} >> {1}".format(p,match_layers))
                if p[0] == '!':
                    not_match_layers = fnmatch.filter(all_layers, p[1:])
                    if len(not_match_layers) : print ("- match >> {0} >> {1}".format(p,not_match_layers))
                    ret_not_match_layers += not_match_layers
                match_layers.sort()               
                ret_match_layers += match_layers
                
            #---- find the layers we want to mult back together
            for math_op in ['/','^']:    
                if len(p.split(math_op))>1:
                    pq = p.split(math_op)[0]
                    pd = p.split(math_op)[1]
                    if pd[0]=='*':
                        match_layers=[]
                        match_layers_divisors = fnmatch.filter(all_layers, pd)
                        for pd2 in match_layers_divisors:
                            match_layers_quotients = fnmatch.filter(all_layers, pq)
                            for pq2 in match_layers_quotients:
                                if pq2.replace(pq[1:],'')==pd2.replace(pd[1:],''):
                                    match_layer = '{0}{1}{2}'.format(pd2,math_op,pq2)
                                    match_layers.append(match_layer)
                        list(set(match_layers))
                        match_layers.sort()
                        ret_match_layers += match_layers                    
                    else: 
                        if pd in all_layers:
                            match_layers = fnmatch.filter(all_layers, pq)
                            match_layers = list(map(lambda x: x+math_op+pd, match_layers))
                            if len(match_layers) : print ("+ match >> {0} >> {1}".format(p,match_layers))
                            if p[0] == '!':
                                not_match_layers = fnmatch.filter(allLayers, pQ[1:])
                                not_match_layers = list(map(lambda x: x+math_op+pD, not_match_layers))
                                if len(not_match_layers) : print ("- match >> {0} >> {1}".format(p,not_match_layers))
                                ret_not_match_layers += not_match_layers
                            match_layers.sort()
                            ret_match_layers += match_layers
                    
        self.aov_list = [x for x in ret_match_layers if x not in ret_not_match_layers]
        if len(self.aov_list) : print ('layers/aovs to recombine {0}'.format(ret_match_layers))
        if self.dir_mult == -1:
            self.aov_list.reverse()
            
    def build_aov_trees(self):
        nx=self.kn.xpos()+self.kn.screenWidth()/2
        ny=self.kn.ypos()+self.kn.screenHeight()/2
        pref=nuke.toNode('preferences')
        th=int(pref['TileHeight'].value())
        gw=int(pref['GridWidth'].value())
        ds=int(pref['dot_node_scale'].value())*6
        
        start_dot = nuke.nodes.Dot( xpos=nx-ds, ypos=ny+self.y_offset_small-ds)
        start_dot.setInput(0,self.kn)
        previous_top_output=start_dot
        
        orphan_buffer=False
        if self.subtract_aovs:
            orphan_buffer=True
            x=previous_top_output.xpos()+self.x_offset+ds
            y=previous_top_output.ypos()+ds
            tree = aov_tree(None, [x,y], self.dir_mult, self.x_offset, self.y_offset_small, self.y_offset_large, self.x_offset_mult)
            self.aov_trees.append(tree)
            previous_top_output = tree.top_output
        
        for aov in self.aov_list:
            is_last_tree = False
            if aov == self.aov_list[-1]: is_last_tree = True
            x=previous_top_output.xpos()+self.x_offset+ds
            y=previous_top_output.ypos()+ds
            tree = aov_tree(aov, [x,y], self.dir_mult, self.x_offset, self.y_offset_small, self.y_offset_large, self.x_offset_mult, is_last_tree, orphan_buffer)
            self.aov_trees.append(tree)
            previous_top_output = tree.top_output
            
        if self.subtract_aovs:
            m=self.aov_trees[0].subtract_node
            j=1
            for tree in self.aov_trees:
                if m!=tree.subtract_node:
                    m.setInput(j,tree.subtract_node)
                    j+=1
                    if j==2:j=3
        
        self.aov_trees[0].top_input.setInput(0,start_dot)    
        for i in range(1,len(self.aov_trees)):
            self.aov_trees[i].top_input.setInput(0,self.aov_trees[i-1].top_output)  
        for i in range(0,len(self.aov_trees)-1):
            self.aov_trees[i].bottom_output.setInput(0,self.aov_trees[i+1].bottom_output)              
            
        copy = nuke.nodes.Merge2( xpos=self.kn.xpos(), ypos=self.aov_trees[0].bottom_output.ypos()+th/4)
        copy.setInput(1,self.aov_trees[0].bottom_output)
        copy['operation'].setValue('copy')
        copy['Achannels'].setValue('rgb')
        copy['Bchannels'].setValue('rgb')
        copy['output'].setValue('rgb')
        copy['also_merge'].setValue('all')
        copy['bbox'].setValue('B')
    
        pre_copy_dot1 = nuke.nodes.Dot(xpos=self.kn.xpos(), ypos=copy.ypos()-self.y_offset_small)
        pre_copy_dot1.setXpos(int(pre_copy_dot1.xpos()-ds+self.kn.screenWidth()/2))
        pre_copy_dot1.setYpos(int(pre_copy_dot1.ypos()-ds+self.kn.screenHeight()/2))
        pre_copy_dot1.setInput(0,start_dot)
        copy.setInput(0,pre_copy_dot1)
    
        pre_copy_dot2 = nuke.nodes.Dot(xpos=self.kn.xpos()-min(abs(self.x_offset),2*gw)*self.dir_mult, ypos=copy.ypos()-self.y_offset_small)
        pre_copy_dot2.setXpos(int(pre_copy_dot2.xpos()-ds+self.kn.screenWidth()/2))
        pre_copy_dot2.setYpos(int(pre_copy_dot2.ypos()-ds+self.kn.screenHeight()/2))
        pre_copy_dot2.setInput(0,pre_copy_dot1)
    
        pre_copy_dot3 = nuke.nodes.Dot(xpos=self.kn.xpos()-min(abs(self.x_offset),2*gw)*self.dir_mult, ypos=copy.ypos()+self.y_offset_small)
        pre_copy_dot3.setXpos(int(pre_copy_dot3.xpos()-ds+self.kn.screenWidth()/2))
        pre_copy_dot3.setYpos(int(pre_copy_dot3.ypos()-ds+self.kn.screenHeight()/2))
        pre_copy_dot3.setInput(0,pre_copy_dot2)
    
        copy_alpha = nuke.nodes.Copy( xpos=self.kn.xpos(), ypos=copy.ypos()+self.y_offset_small-th/4)
        copy_alpha['from0'].setValue('alpha')
        copy_alpha['to0'].setValue('alpha')
        copy_alpha.setInput(0,copy)
        copy_alpha.setInput(1,pre_copy_dot3)
        copy_alpha['bbox'].setValue('B')
    
        premult_end = nuke.nodes.Premult( xpos=self.kn.xpos(), ypos=copy_alpha.ypos()+self.y_offset_small)
        premult_end.setInput(0,copy_alpha)
        
        for e in self.kn.dependent():
            for i in range (e.inputs()):
                if e.input(i)==self.kn:
                    e.setInput(i,premult_end)
