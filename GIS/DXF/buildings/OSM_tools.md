---
layout: default
title:  OSM處理過程所用到的小工具
parent: buildings
grand_parent: DXF
last_modified_date: 2024-12-09 14:33:45
tags: GIS DXF
---

# OSM處理過程所用到的小工具

{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 背景

- 因為工作太過複雜，工具當然是越多越好，如果不夠用也只好自己做。
- 這種分享有時候也很殘忍，因為對某人很好用的工具，對其他人可能就沒那麼好用，見仁見智囉!


### 新創平行運作所需之次目錄

- 這個問題會發生，是因為檔名沒有規則性，使用`bash`來建目錄很快，但是檔案要區分下去就沒那麼方便了，這一題，LLM的建議是使用python來做。
- 將檔案略分為20個群組，這是因為搭配工作站有20個CPU可以同步來執行。
- 使用`np.array_split`，這招厲害，沒聽過也沒用過。
- 中文檔案名稱還可以忍受，半型的小括弧，這就有點挑戰了，需要加個反斜線來進行程式化。

```python
#kuang@DEVP /nas2/kuang/MyPrograms/CADNA-A/OSM
#$ cat make_sub.py
import numpy as np
import os
kml_folder='./'
fnames=[filename for filename in os.listdir(kml_folder) if filename.startswith('final')]
split_fnames = np.array_split(fnames, 20)
for i in range(20):
    os.system(f"mkdir -p sub{i}")
p1='/nas2/kuang/MyPrograms/CADNA-A/OSM'
for i in range(20):
    for fname in split_fnames[i]:
        if '(' in fname:
            ff=fname.replace('(','\\(').replace(')','\\)')
            os.system(f"ln -sf {p1}/{ff} {p1}/sub{i}/{ff}")
        else:
            os.system(f"ln -sf {p1}/{fname} {p1}/sub{i}/{fname}")
```

### 整併各個經緯度範圍的building2D結果

- 這不是個小工具，算個小作業，我把ipython上的作業過程留下來，免得重作時還要重新問AI讓AI再想一遍。
- building3D也是2D做出來的，所以需要將其剔除，免得重複處理。
- AI這題的答案也很優秀，很少人會這樣用條件。`~building2D['geometry'].isin(building3D['geometry'])`

```python
kuang@DEVP /nas2/kuang/MyPrograms/CADNA-A/OSM
$ cat bld2d.py
cd OSM
import os
import glob
directory = './'
dfs = []
col=['geometry']
for file in glob.glob(os.path.join(directory, 'output??bld.csv')):
    df = pd.read_csv(file)
    dfs.append(df[col])
df[col].head()
dfs[0].head()
dfs[-1].head()
len(df)
len(dfs)
combined_df = pd.concat(dfs, ignore_index=True)
len(combined_df)
dfs.to_csv('building2D.csv',index=False)
combined_df.to_csv('building2D.csv',index=False)
!lst
mv building2D.csv building2D_all.csv
building3D = pd.read_csv('building3D.csv')
building2D = pd.read_csv('building2D_all.csv')
building2D = building2D[~building2D['geometry'].isin(building3D['geometry'])]
building2D.to_csv('building2D_updated.csv', index=False)
len(building2D)
building2D.head()
history
```

## 執行腳本

$ ls *cs
  break_osm2.cs  do_join.cs
(pyn_env)
kuang@DEVP /nas2/kuang/MyPrograms/CADNA-A/OSM
$ cat *cs


### 全區0.5度解析度之切割腳本

- `break_osm.cs`這支腳本會連續做5個東西向範圍，再由外部控制南北向(0~7)
- ``
```bash
for i in {0..5};do
j=$1
left=$(echo "119.2 + $i * 0.5" |bc)
right=$(echo "119.7 + $i * 0.5" |bc)
bottom=$(echo "21.5 + $j * 0.5" |bc)
top=$(echo "22.0 + $j * 0.5" |bc)
osmconvert input.osm -b=${left},${bottom},${right},${top} --complete-ways -o=output${i}${j}.osm
done
cd sub$1
for i in $(ls final*);do python ../../join_Alt_osmBld.py $i;done
cd ..
```

### 北高都會區0.1度解析度之切割腳本

```bash
i=$1
j=$2
start_l=$(echo "119.2 + $i * 0.5" |bc)
start_b=$(echo "21.5 + $j * 0.5" |bc)
for k in {0..5};do
for l in {0..5};do
left=$(echo "$start_l + $k * 0.1" |bc)
right=$(echo "$left + 0.1" |bc)
bottom=$(echo "${start_b} + $l * 0.1" |bc)
top=$(echo "$bottom + 0.1" |bc)
sub  osmconvert input.osm -b=${left},${bottom},${right},${top} --complete-ways -o=output${i}${j}${k}${l}.osm
done
done
```

### 將高度併入build2D檔案內

`for i in $(ls output??pnt.csv);do j=${i/pnt/bld};sub python join.py $i $j;done`

```bash
$ cat do_join.cs
cd sub$1
for i in $(ls final*);do python ../../join_Alt_osmBld.py $i;done
cd ..
```