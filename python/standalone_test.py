import maya.standalone
import maya.OpenMaya as OpenMaya

import sys

def main(argv=None):
    try:
        maya.standalone.initialize(name='python')
    except:
        sys.stderr.write('Failed to initialize standalone application')
        raise
    
    sys.stderr.write('Hello,world!\n')
    OpenMaya.MGlobal().executeCommand('print \"Hello world!"')
    maya.standalone.uninitialize()

if __name__ == '__main__':
    main()