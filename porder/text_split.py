__copyright__ = """

    Copyright 2019 Samapriya Roy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""
__license__ = "Apache 2.0"

import os
def idsplit(infile,linenum,output):
    lines_per_file = int(linenum)
    smallfile = None
    with open(infile) as bigfile:
        basename=os.path.basename(infile).split('.')[0]
        for lineno, line in enumerate(bigfile):
            if lineno % lines_per_file == 0:
                if smallfile:
                    smallfile.close()
                small_filename = basename+'_{}.csv'.format(str(lineno+int(linenum)))
                smallfile = open(os.path.join(output,small_filename), "w")
            smallfile.write(line)
        if smallfile:
            smallfile.close()
    print('IDlist split at '+str(output))
