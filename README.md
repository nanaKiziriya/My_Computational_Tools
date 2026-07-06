## One shoddy way to import in python:

```
def gitModule(owner:str, repo:str, mod_file:str) :

  import shutil
  import importlib
  import os.path
  import numpy as np

  try :
    link = f"https://github.com/{owner}/{repo}.git"
    temp_dir = f"TEMP_{int(np.random.rand()*10**16)}"
    while os.path.isfile(temp_dir) :
      temp_dir = f"TEMP_{int(np.random.rand()*10**16)}"
    !git clone $link $temp_dir -q
    temp = importlib.import_module(f'{temp_dir}.{mod_file}')
    shutil.rmtree(temp_dir, ignore_errors=True)
    return temp;
  except :
    print(f"Something went wrong during gitModule({owner},{repo},{mod_file})")


# Example of usage
rgb = gitModule('nanaKiziriya','My_Computational_Tools','RGBSequence')
# https://github.com/nanaKiziriya/My_Computational_Tools/blob/main/RGBSequence.py

print(rgb.color_sequence())

```



## NOTICE:

All programs in this repo are free to use under the **GNU General Public License v3.0**.

(https://www.gnu.org/licenses/gpl-3.0.en.html)
