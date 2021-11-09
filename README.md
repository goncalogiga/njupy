# njupy

njupy is a simple script used as a sort of front end for [jupyter
ascending](https://github.com/untitled-ai/jupyter_ascending.vim), a plugin used
to edit Jupyter notebooks in vim.

## Installation

After cloning the repository,

```
git clone https://github.com/goncalogiga/njupy
```

install it with 

```
pip install .
```

Once the plugin is also intalled in vim, everything should work.

## Usage

If you have a jupyter notebook called ```test.ipynb``` file, you can simply run the following command:

```
njupy test.ipynb
```

This will generate a python file called ```test.sync.py``` and will rename the ```test.ipynb``` file into ```test.sync.ipynb``` and launch it with jupyter notebook (the process is detatched so you can still use the terminal which called njupy to launch vim)

Once the jupyter notebook is open, jupyter_ascending will work with the test.sync.py file

After you are done, you can call the following command from the directory where the notebook is, in order to remove the ```.sync.py``` file and restore the original name of the jupyter notebook. This will also kill the process used to run the notebook.

```
njupy --end
```
