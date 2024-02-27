from pandas import *
import os, glob
source_directory='./'
fnames = glob.glob(os.path.join(os.path.expanduser(source_directory), "*.csv"))
for fname in fnames:
    df=read_csv(fname)
    if fname==fnames[0]:
        df0=df
        continue
    else:
        combined_df = concat([df0, df], ignore_index=True)
        df0=combined_df
df0.to_csv('df0.csv',index=False)
