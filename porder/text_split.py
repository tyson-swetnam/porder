import os
def idsplit(infile,linenum,output):
    if not os.path.exists(output):
        os.makedirs(output)
    lines_per_file = int(linenum)
    smallfile = None
    with open(infile) as bigfile:
        for lineno, line in enumerate(bigfile):
            if lineno % lines_per_file == 0:
                if smallfile:
                    smallfile.close()
                small_filename = 'link_file_{}.csv'.format(str(lineno+int(linenum)))
                smallfile = open(os.path.join(output,small_filename), "w")
            smallfile.write(line)
        if smallfile:
            smallfile.close()
    print('IDlist split at '+str(output))
