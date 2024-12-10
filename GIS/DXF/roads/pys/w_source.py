#kuang@DEVP /nas2/kuang/MyPrograms/CADNA-A/inputDWS
#$ cat w_source.py
import ezdxf
from ezdxf.addons.dxf2code import entities_to_code, block_to_code
import sys

root=sys.argv[1].replace('.dxf','').replace('.DXF','')
doc = ezdxf.readfile(sys.argv[1])
msp = doc.modelspace()
source = entities_to_code(msp)

# create source code for a block definition
MyBlock=doc.blocks.block_names()
block_source = block_to_code(doc.blocks[MyBlock[0]])

# merge source code objects
source.merge(block_source)

with open(f"{root}.py", mode='wt') as f:
    f.write(source.import_str())
    f.write('\n\n')
    f.write(source.code_str())
    f.write('\n')
