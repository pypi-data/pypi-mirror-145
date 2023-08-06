.. _installation:

=======================
Installation
=======================

WindKit is distributed through the `conda <https://docs.conda.io/en/latest/>`_ package, dependency, and environment manager via DTU Wind Energy's Open Conda Channel.

.. note:: If you are installing PyWAsP, which requires a license, you will obtain WindKit through DTU Wind Energy's WAsP Conda Channel instead.

1. To install WindKit you need to first install conda, this can be done through either the `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_ minimal conda installer, or the `Anaconda <https://www.anaconda.com/>`_ Data Science Platform. Generally we recommend Miniconda on Linux,and Anaconda on Windows and macOS.

2. After you have installed conda you will need to add the DTU Wind Energy Open Conda Channel and the conda-forge channel.

  The easiest way to do so is via the command prompt.

  On Linux and macOS, open a terminal that has conda configured. On Windows, you will find an entry called the Anaconda Prompt, which will setup the necessary environment for configuring conda.

  Run the commands below to add the channels::

    conda config --add channels conda-forge
    conda config --add channels https://conda.windenergy.dtu.dk/channel/open

3. Now you can setup a new conda environment that has WindKit installed::

    conda create -n <env_name> windkit jupyterlab


  This command will find all of the dependencies of windkit and install them along with windkit in an environment named *env_name*. In the example above, we have included `JupyterLab <https://jupyterlab.readthedocs.io/en/stable/>`_ as an optional dependency, as it can be a good place to get started with learning WindKit.

4. Change to the new environment and start JupyterLab::

    conda activate <env_name>
    jupyter-lab


  In the first cell of your jupyter notebook, you can type the command ``import windkit as pw``, and run the cell. From there, you will be able to access all of the :ref:`windkit_api` from the *pw* namespace.
