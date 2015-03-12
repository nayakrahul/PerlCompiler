idCount = 0

def treeBegin(outfile):
    outfile.write('digraph parse_tree{\n')

def treeNode(label, outfile, p):
    global idCount
    text = ""
    nodeId = "Node%d" % idCount
    text = ""
    idCount += 1
    baseIds = []
    children = []

    for term in p[1:]:
        if type(term) == type(''):
            termId = "Child%d" % idCount
            idCount += 1
            if len(text) == 0:
                text = term
            else:
                text += " " + term
            baseIds.append(termId)
            outfile.write('%s [label="%s"];\n' % (termId, term))
            children.append(termId)
        else:
            termId = term[1]
            if len(text) == 0:
                text = term[0]
            else:
                text += " " + term[0]
            baseIds.extend(term[2])
            children.append(termId)

    label = label 
    print label
    outfile.write('%s [label="%s"];\n' % (nodeId, label))
    for child in children:
        outfile.write('%s -> %s;\n' % (nodeId, child))

    return (text, nodeId, baseIds)

def treeEnd(outfile, node):
    baseIds = node[2]
    outfile.write('{ rank=same;\n')
    for i in range(len(baseIds)-1):
        outfile.write('%s ->' % baseIds[i])
    outfile.write('%s [style=invis];\n}\n' % baseIds[-1])

    outfile.write('}\n')
