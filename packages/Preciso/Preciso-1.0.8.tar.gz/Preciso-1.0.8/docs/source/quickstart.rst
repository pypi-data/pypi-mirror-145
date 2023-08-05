.. Getting started with Preciso

Getting started
=================================

Contents of this guide
----------------------

- What does PreciSo do, how it works ?
- How to use it without installing it on your computer (online user)
- How to use it in your projects (local user)
- How to modify or extend its capabilities (i.e. for developers)


Overview
--------

Preciso is a Python wrapper to the initial C++ project, which allows modelling the precipitation of complex alloys. It is designed to be **lightweight** and **convenient**, for both new and more experienced users.

Below is an example use case for PreciSo :

.. code-block:: python

    import preciso
    import matplotlib.pyplot as plt

    # a configuration file specific to your material
    config_filename = "path/to/configuration_file.txt"
    
    # communication with PreciSo's C++ engine is transparent :
    results = preciso.runSimulation(config_filename) 

    # results are available in the form of pandas DataFrames
    df = results.precipitation[0] 
    
    plt.loglog(df["t[s]"],
               df["rmean_beta'[m]"],
               label="$R_{mean} (m)$")
    # *A beautiful figure appears*

Under the hood, the Python module calls the C++ code, and retrieves its outputs. 

.. note::
    PreciSo is available as a *Python package*. To use it, you will need **Python 3**, and a few other packages PreciSo is built on. 
    If you have never heard of Python before, and don't need to add new features PreciSo, the online version will be the best option.

.. note::
    If you have any issue installing PreciSo, or if this documentation is somehow inaccurate, feel free to submit a ticket to the project's `Gitlab issue tracker <https://gitlab.com/arnall/preciso/issues>`_.


How to use PreciSo online (no installation) 
-------------------------------------------

To use PreciSo online, we recommended using Google Colab, Repl.it, CodeOcean, MyBinder, or any equivalent. 

To start using it on **Google Colab** : 

- Go to `<https://colab.research.google.com>`_ (needs a Google account).
- Create a new notebook. You can rename it in the top bar (default is Untitled.ipynb)
- In the first cell of the notebook, type ``pip install preciso`` and press the run button on the left. 
- This will output a lot of text that you can delete later ("Clear output", below the run button). Just make sure the last line says ``Successfully installed preciso-xx``. If not, you can try to google your error message (last lines of the output), or send us an email or open an `issue <https://gitlab.com/arnall/preciso/issues>`_.
- You can now ``import preciso`` and use it in the rest of the notebook !

For other platforms, all you need is to find how to `install custom python packages <https://docs.repl.it/repls/packages>`_ from the PyPi repo. From a `Repl <https://repl.it/>`_, it's as simple as clicking the "Packages" button, typing "Preciso" and clicking "add". 
The difference between Repl and Colab is that Repls are basically code snippets, whilst Colab is an interactive platform, and is much better at results visualization.



Installation (local user)
--------------------------

.. note::
    PreciSo supports Python 3 only. The current recommended version is 3.7. 

In order to run PreciSo on your computer, you will need to :

- Get Python
- Install the PreciSo package. 

For experienced users who have Python installed, installing PreciSo is as simple as ``pip install preciso``. **If you are not sure if you already have Python or how to install PreciSo, continue reading.**

.. warning::
    **Installing Python** the first time can be **tedious**, especially on Windows, and take a lot of disk space. If you only need very occasional use of PreciSo, you may want to use PreciSo online (see above).

The main barrier in installing Python is the possible existance of multiple instances of Python on your machine. 
If you already have one Python executable (possibly installed by another software) and install another one, it is likely that PreciSo will not be installed in the correct location, and it won't work. 


To avoid that, the recommended way is to use **virtual environments**. If you never used Python before, you can do it easily by installing Anaconda as described below. 

Advanced users may prefer using miniconda (lightweight version of Anaconda), virtualenv or pipenv to create an environment in which they will install PreciSo and its dependencies. The step-by-step procedure is described in the **Installing PreciSo for developers** section below.

Install with Anaconda (all OS)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Install a full Anaconda distribution, following the `official documentation <https://docs.anaconda.com/anaconda/install/>`_.
2. Open Anaconda, and launch Jupyter.
3. Go to the directory of your choice, and create a new Python3 notebook.
4. In the top cell, type ``! pip install preciso``. Run the cell (Shift+Enter), and wait for the installation to finish.
5. In a new cell, type ``import preciso``. This command should not fail.
6. Then, type ``preciso.runSimulation(" ", debug=True)``. The output should report an error, and contain "Welcome to PreciSo v3.0". This means the C++ engine of PreciSo was correctly started, and the installation was fully successful. If you don't get this output, feel free to contact us for help.



Installing PreciSo for developers
---------------------------------

On Linux/MacOS, using Miniconda
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Miniconda is a distribution that includes ``conda``, the package manager that will help you make a clean install of Python and PreciSo on any platform, with no root permissions. The famous Anaconda distribution is similar to Miniconda, but it includes a huge number of additional packages you don't need for using PreciSo.


1. To get Python and Miniconda, follow the **instructions** from the official documentation of `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_ **and** `conda <https://conda.io/projects/conda/en/latest/user-guide/install/index.html>`_. 

On MacOS and Linux, it should be :

.. code-block:: bash

    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -O ~/miniconda.sh
    bash ~/miniconda.sh -b -p $HOME/miniconda


2. Once conda is installed, create an environment that lists all Preciso's dependencies. For that, we'll use a file to specify the packages we want to install, that contains :

.. code-block:: python

    name: python-preciso
    channels:
      - anaconda
    dependencies:
      - python=3.7
      - numpy
      - pandas
      - matplotlib
      - scipy
      - jinja2
      - git
      - jupyter
      - seaborn

This file can be **downloaded** `here <https://framagit.org/arnall/preciso/raw/master/environment.yml?inline=false>`_. 

3. Then, run one line at a time :

.. code-block:: python

    # the first time you use conda
    
    # On macOS / Linux :
    $HOME/miniconda/bin/conda init

    # If conda is not found, you'll have to Google for a solution for your specific case/platform, or ask for help

    # create an environment from the file you downloaded
    conda env create -f environment.yml

    # activate the environment everytime you want to use it. 
    # On Linux/MacOS can set an alias in your ~.bashrc or ~.bash_profile file for this one.
    conda activate python-preciso

    # Download the last version of Preciso
    git clone https://framagit.org/arnall/preciso.git

    # Install preciso in developer mode (-e)
    cd preciso
    pip install -e .


4. Check that the installation was successful. The following command should issue no error when ran in a **new** terminal.

.. code-block:: python
    
    python3 -c 'import preciso; print("Preciso was successfully installed !")'



Manual installation on Linux/Mac OS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you already have a full Python installed and ready-to-go, and have git, you can follow these instructions.

Downlaod PreciSo package::

    git clone https://framagit.org/arnall/preciso.git preciso

Upgrade pip::

    python3 -m pip install --user --upgrade pip

In Jupyter, open a new terminal and enter the preciso folder::

    cd preciso

Install preciso package::

    pip install -e .

Check all requirements::

    pip install -r requirements.txt


On Windows (using Anaconda)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

To install Python requirements :

1. Install a full Anaconda distribution, following its official documentation. 

.. note::
    
    Alternatively, you can install miniconda by downloading the installer `here <https://conda.io/miniconda.html>`_. Then from a terminal, do :

    .. code-block:: bash

        start /wait "" Miniconda3-latest-Windows-x86_64.exe /InstallationType=JustMe /RegisterPython=0 /S /D=%UserProfile%\miniconda


2. Download the `environment file <https://framagit.org/arnall/preciso/raw/master/environment.yml?inline=false>`_.

3. From Anaconda, `import an environment <https://docs.anaconda.com/anaconda/navigator/tutorials/manage-environments/#importing-an-environment>`_ and **activate it**.

**For the installation of Preciso :**

4. Open an Anaconda prompt, Jupyter terminal or jupyter notebook. Make sure you access your python-preciso environment by typing ``conda env list``. It should display something like :

.. code-block:: bash
    
    # conda environments:
    #
    base                      /home/aallera/miniconda
    python-preciso         *  /home/aallera/miniconda/envs/python-preciso

Check the position of the ``*`` character, which means that ``python-preciso`` is the activated environment.


5. Create a folder and extract the archive found `here <https://framagit.org/arnall/preciso/-/archive/master/preciso-master.zip>`_ (you'll have to manually fetch new versions to get updates and bug fixes !)

or

5. Get preciso source code with ::

    git clone https://framagit.org/arnall/preciso.git
    
It will create a "preciso" folder in the current directory, that will contain the last version of the code. 
Updates can be done from this "preciso" directory with ``git pull``.

6. Go to the folder that contains preciso's ``setup.py``::

    cd preciso

Then install preciso with pip (if error, try ``pip3`` instead)::

    pip install -e .

If executed from a Jupyter notebook, do instead ::

    !pip install -e .

Relaunch Jupiter Notebook and check that preciso is importable from anywhere::

    import preciso; preciso.runSimulation("", temp=False)
