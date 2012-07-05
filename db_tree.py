from myutil import conn
import re

def test():
    print "hello db tree"

tree_display_list = {}
tree_list = {}
tree_list_example = {'a':{1:{}, 2:{}, '3':{4:{'99':{4:{}}}, '5':{'d':{}}}, '4':{7:{}, 8:{}}}, 'b':{6:{}, 4:{}, 2:{}}, 'c':{90:{}, 6:{}}, 'd':{100:{}}}

def leaf_loop(leaf, thing_from, thing_to):
    flag = True
    if leaf.has_key(thing_from):
        leaf[thing_from][thing_to] = {}
        flag = False
    return flag

def subtree_loop(subtree, thing_from, thing_to):
    #flag = True
    if subtree.has_key(thing_from):
        if subtree[thing_from].has_key(thing_to):
            print "repeat: %s -> %s *** %s"%(str(thing_from), str(thing_to), str(subtree[thing_from]))
            #sys.error()
        else:
            subtree[thing_from][thing_to] = {}
        #print "found:%s, *****%s"%(str(thing_from), str(subtree))
        return False
    else:
        flag = True
        for key in subtree:
            flag = subtree_loop(subtree[key], thing_from, thing_to)
            if flag == False:
                break
        return flag
        


def tree_loop(tree, thing_from, thing_to):
    if tree.has_key(thing_from): # if a->b has found in tree[a]
        tree[thing_from][thing_to] = {}
    else:
        flag = True
        #for key in tree:
        flag = subtree_loop(tree, thing_from, thing_to)
        #if flag == False:
        #print "tree stop at:", key, thing_from
        #break
        if flag == True: ## if a->b is never found in the tree
            tree[thing_from] = {thing_to:{}}
    #print tree

#tree_loop(tree_list_example, '10', '10') # new leaf in the top level
#tree_loop(tree_list_example, 'd', '5') # new leaf int he buttom level
#tree_loop(tree_list_example, '3', '10') # new leaf int he middle
#tree_loop(tree_list_example, '3', '5') # same leaf appears again

#tree_list_example = {'a':{1:{}, 2:{}, '3':{4:{}, '5':{'d':{}}}, '4':{7:{}, 8:{}}}, 'b':{6:{}}}

#def subsubtree_display(subsubtree, s):
#    for key in subsubtree:
#        if subsubtree[key] == {}:
#            thing_to = "hello"


def subtree_display(subtree, s):
    for key in subtree:
        if subtree[key] == {}:
            thing_to = key
            s2 = '%s -> %s '%(s, str(thing_to)) # a single tree has been set down
            print s2
            #continue
        else:
            thing_to = key
            s1 = '%s -> %s '%(s, str(thing_to))
            subtree_display(subtree[key], s1)

def tree_display(tree_list):
    for root in tree_list:
        thing_from = root
        s = '%s '%(str(thing_from))
        subtree = tree_list[root]
        s = subtree_display(subtree, s)
        #print s

#tree_display(tree_list_example)


sql_tree = '''
SELECT * FROM derived_raw
'''
def get_tree():
    #print "hello"
    c = conn.cursor()
    param = ()
    sql = sql_tree
    c.execute(sql, param)
    for row in c.fetchall():
        #print row
        thing_from = row[1]
        thing_to = row[2]
        #print thing_from
        #print thing_to
        tree_loop(tree_list, thing_from, thing_to)
    #print tree_list
    #print len(tree_list)
    #tree_display(tree_list)
    print "tree_list: %s"%(str(len(tree_list)))
    return tree_list
    

def list_no_duplicate(lists):
    ln = []
    for l in lists:
        if l not in ln:
            ln.append(l)
    #ln.append('asbc')
    #lists = ln
    #print len(ln)
    return ln

sql_child_with_multiple_parents = '''
SELECT COUNT(x_url) AS p_n, y_url FROM derived_raw
GROUP BY y_url
ORDER BY p_n DESC
'''
def get_things_with_multiple_parents():
    child_list = []
    f = open('./tree/things_with_multiple_parents.txt', 'w')
    txt = 'parents_count\tthing_to\n'
    f.write(txt)
    c = conn.cursor()
    param = ()
    sql = sql_child_with_multiple_parents
    c.execute(sql, param)
    for row in c.fetchall():
        parents_count = row[0]
        thing_to = row[1]
        txt = '%s\t%s\n'%(str(parents_count), str(thing_to))
        f.write(txt)
        if parents_count > 1:
            #print parents_count, thing_to
            child_list.append(thing_to)
    c.close()
    f.close()
    #print len(child_list)
    t = list_no_duplicate(child_list)
    print "child_list: %s"%(str(len(t)))
    return t


def subtree_check(subtree, s, childs, child_list):
    for key in subtree:
        if subtree[key] == {}:
            thing_to = key
            s2 = '%s -> %s '%(s, str(thing_to)) # a single tree has been set down
            childs.append(s2)
            child_list.append(thing_to)
            #print s2
            #continue
        else:
            thing_to = key
            s1 = '%s -> %s '%(s, str(thing_to))
            child_list.append(thing_to)
            childs, child_list = subtree_check(subtree[key], s1, childs, child_list)
    return childs, child_list

def tree_check(tree_list, children_list):
    f = open('./tree/tree_root_has_nodes_with_multiple_parents.txt', 'w')
    parent_list = {}
    for root in tree_list:
        thing_from = root
        s = '%s '%(str(thing_from))
        subtree = tree_list[root]
        childs = []
        child_list = []
        childs, child_list = subtree_check(subtree, s, childs, child_list)
        #print "hello", childs
        #print "worldd", child_list
        for c in children_list:
            if c in child_list:
                #print thing_from, c, parent_list
                if parent_list.has_key(c):
                    parent_list[c].append(thing_from)
                else:
                    parent_list[c] = [thing_from]
    #print parent_list
    #print "================="
    parent_list = parent_list.values()
    #print parent_list
    parents = []
    for ps in parent_list:
        for p in ps:
            if p not in parents:
                parents.append(p)
    #print parents
    #print "********"
    for p in parents:
        p1 = []
        p2 = []
        for pl in parent_list:
            #print "****", p, pl
            if p in pl:
                p1 = p1 + pl
                #print p1
            else:
                p2.append(pl)
        #print p, p1, "***", p2
        #print p2 + [p1]
        parent_list = p2 + [p1]
        #print parent_list, "---"
    #print parent_list
    pt = []
    print "------------"
    for p in parent_list:
        p = list_no_duplicate(p)
        txt = str(p)+"\n"
        f.write(txt)
        #print p
        pt.append(p)
    f.close()
    return pt
   
                            
#print tree_list_example
#tree_check(tree_list_example, [2, 6, 100, 90])
#print "tree_check"

def get_thing_with_multi_parents_root_list(tree_list, child_list):
    parent_list = tree_check(tree_list, child_list)
    return parent_list
    

def get_tree_individual(tree_list, parent_list):
    print len(tree_list)
    trees = []
    i = 0
    for pl in parent_list:
        tl = {}
        #print pl, "pppp"
        pl = list_no_duplicate(pl)
        #print pl
        for p in pl:
            tl[p] = tree_list[p]
            del tree_list[p]
            i = i+1
        trees.append(tl)
        #print tl, "+++"
    #for t in trees:
        #print t, "\n"
    print "overlaped tree:%d"%(len(trees))
    print "unoverlaped tree:%d"%(len(tree_list))
    #print i
    #print '\n\n\n\n\n\nn\nn\\n\n\n'
    #print parent_list
    for pl in tree_list:
        #print pl
        trees.append({pl:tree_list[pl]})
    print "total individual trees:%d"%(len(trees))
    thing_counts = {}
    i = 0
    thing_number = 2
    for t in trees:
        #print t
        ts = str(t)
        #print ts
        results = re.findall('thing', ts)
        thing_count = len(results) 
        if thing_counts.has_key(thing_count):
            thing_counts[thing_count] = thing_counts[thing_count] + 1
        else:
            thing_counts[thing_count] = 1
        if thing_count > thing_number:
            #print ts
            i += 1
        #print len(t)
    print "trees has thing numbers larger than %d: %d"%(thing_number, i)
    print "trees with things counts: %s"%(str(thing_counts))
    #for tree in trees:
    #    print tree, '**'
    return trees

#parent_tree = tree_check(tree_list_example, [2, 6, 90])
#get_tree_individual(tree_list_example, parent_tree)


def subtree_dot(subtree, s, tree_dot_list, tree_bound_list):
    for key in subtree:
        if subtree[key] == {}:
            thing_to = key
            thing_to = thing_to.strip('\n\t/thing:')
            s2 = '%s -> {%s} ;'%(s, str(thing_to)) # a single tree has been set down
            tree_dot_list.append(s2)
            tree_bound_list.append(s2)
            #print s2
            #continue
        else:
            thing_to = key
            thing_to = thing_to.strip('\n\t/thing:')
            s1 = '%s -> {%s} '%(s, str(thing_to))
            tree_dot_list, tree_bound_list = subtree_dot(subtree[key], s1, tree_dot_list, tree_bound_list)
    return tree_dot_list, tree_bound_list

def tree_dot(tree_list):
    tree_dot_list = []
    tree_bounds_list = {}
    for root in tree_list:
        thing_from = root
        thing_from = thing_from.strip('\n\t/thing:')
        s = '{%s} '%(str(thing_from))
        subtree = tree_list[root]
        tree_bound_list = []
        tree_dot_list, tree_bound_list = subtree_dot(subtree, s, tree_dot_list, tree_bound_list)
        tree_bounds_list[thing_from] = tree_bound_list
    #print tree_dot_list, '\n\n\n'
    return tree_dot_list, tree_bounds_list


net_counts = {} # to varified for the net count of nodes in each tree
nets = {}
tree_counts = {}
tree_duplicate = {}

def tree_write(tree_list):
    txt_list = {}
    txt_bound_list = {}
    for tree in tree_list:
        #print tree,"**"
        tree_txt, tree_bound = tree_dot(tree) # test tree_bound
        #print len(tree_bound), tree_bound, "**"
        #print len(tree_txt), tree_txt
        #print len(tree_bound)
        ts = str(tree)
        #print ts, "****"
        results = re.findall('thing', ts)
        #print len(results), results, '\n'
        thing_count = len(results) 
        if txt_list.has_key(thing_count):
            txt_list[thing_count] = txt_list[thing_count] + tree_txt
            txt_bound_list[thing_count] = txt_bound_list[thing_count] + [tree_bound]
            net_counts[thing_count] = net_counts[thing_count] + [tree_txt]
            #tree_counts[thing_count] = tree_counts[thing_count] + 1
        else:
            txt_list[thing_count] = tree_txt
            txt_bound_list[thing_count] = [tree_bound]
            net_counts[thing_count] = [tree_txt]
            nets[thing_count] = {}
            #tree_counts[thing_count] = 1
    ######## varification ##############
    for net_count in net_counts:
        for count in net_counts[net_count]:
            #tree_counts[net_count] = tree_counts[net_count] + 1
            #print tree_counts
            for c in count:
                net_results = re.findall('[0-9]+', c)
                for nr in net_results:
                    #print nr
                    if tree_duplicate.has_key(nr):
                        if tree_duplicate[nr].has_key(net_count):
                            tree_duplicate[nr][net_count] = tree_duplicate[nr][net_count] + 1
                        else:
                            tree_duplicate[nr][net_count] = 1
                    else:
                        tree_duplicate[nr] = {}
                        tree_duplicate[nr][net_count] = 1
                    #print tree_duplicate
                    if nets[net_count].has_key(nr):
                        nets[net_count][nr] = nets[net_count][nr]+1
                    else:
                        nets[net_count][nr] = 1
                    #print nr, nets[net_count][nr]
                #print net_count, "==",  c, "**"
    total_0 = 0
    f = open('./validation/how often a node appear in paths.txt', 'w')
    f.write('bound_count \tthing_id \tpath_count\n')
    for ns in nets:
        #print ns, nets[ns]
        #print tree_counts[ns]
        total_1 = 0
        total_2 = 0
        for n in nets[ns]:
            total_1 = total_1 + nets[ns][n]
            total_2 = total_2 + 1
            #print ns, n, nets[ns][n]
            f.write('%s\t%s\t%s\t\n'%(ns, n, nets[ns][n]))
        total_0 = total_0 + total_2
        print '\t', ns, '\t', total_2, '\t', total_1
    f.close()
    print total_0
    f = open('./validation/which gv files a node would appear.txt', 'w')
    f.write('thing_id \t{gv files:appear times}')
    for td in tree_duplicate:
        f.write('%s\t%s\n'%(td, tree_duplicate[td]))
        if len(tree_duplicate[td]) > 1:
            print '\t', td,'\t',  tree_duplicate[td]
            #pass
    f.close()
    ########## varification #################
    #print txt_list
    for thing_count in txt_list:
        f = open('./tree/results/no_board/thing_count_%s.gv'%(str(thing_count)), 'w')
        f.write('strict digraph graphname {\n')
        for path in txt_list[thing_count]:
            f.write('\t%s\n'%path)
        f.write('}')
        f.close()
    #print txt_bound_list
    for thing_count in txt_bound_list:
        #print txt_bound_list[thing_count]
        f = open('./tree/results/with_board/bound_thing_count_%s.gv'%(str(thing_count)), 'w')
        f.write('strict digraph graphname {\n')
        trees = txt_bound_list[thing_count]
        for tree in trees:
            #print thing_count, '******', tree, '\n'
            for t in tree:
                #print t, tree[t]
                f.write('\tsubgraph cluster_%s {\n'%t)
                f.write('\t\tnode [style=filled];\n')
                for path in tree[t]:
                    f.write('\t\t%s\n'%path)
                f.write('\t\tlabel = "root_%s";\n'%t)
                f.write('\t\tcolor = blue;\n')
                f.write('\t }\n')
            #for t in tree
        #    f.write('\t%s\n'%path)
        f.write('}')
        f.close()
        
#parent_tree = tree_check(tree_list_example, [2, 6, 90])
#tree_clean = get_tree_individual(tree_list_example, parent_tree)
#tree_write(tree_clean)


sql_derived_thing_all_x = '''
SELECT x_url FROM derived_raw;
'''
sql_derived_thing_all_y = '''
SELECT y_url FROM derived_raw;
'''

def thing_check():
    thing_unique = {}
    c = conn.cursor()
    c.execute(sql_derived_thing_all_x, ())
    for raw in c.fetchall():
        x = raw[0].strip().replace('/thing:', '')
        if thing_unique.has_key(x):
            thing_unique[x] = thing_unique[x]+1
        else:
            thing_unique[x] = 1
    c.execute(sql_derived_thing_all_y, ())
    for raw in c.fetchall():
        y = raw[0].strip().replace('/thing:', '')
        if thing_unique.has_key(y):
            thing_unique[y] = thing_unique[y]+1
        else:
            thing_unique[y] = 1
    print len(thing_unique)
