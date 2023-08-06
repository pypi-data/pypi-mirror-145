# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mpipartition']

package_data = \
{'': ['*']}

install_requires = \
['mpi4py>=3.1.0,<4.0.0', 'numpy>=1.10,<2.0']

setup_kwargs = {
    'name': 'mpipartition',
    'version': '0.2.3',
    'description': 'MPI volume decomposition and particle distribution tools',
    'long_description': 'MPIPartition\n============\n\n\n.. image:: https://img.shields.io/pypi/v/mpipartition.svg\n   :target: https://pypi.python.org/pypi/mpipartition\n\n.. image:: https://github.com/ArgonneCPAC/MPIPartition/actions/workflows/pypi.yml/badge.svg\n   :target: https://github.com/ArgonneCPAC/MPIPartition/actions/workflows/pypi.yml\n\n.. image:: https://github.com/ArgonneCPAC/MPIPartition/actions/workflows/sphinx.yml/badge.svg\n   :target: https://github.com/ArgonneCPAC/MPIPartition/actions/workflows/sphinx.yml\n\nA python module for MPI volume decomposition and particle distribution\n\n\n* Free software: MIT license\n* Documentation: https://argonnecpac.github.io/MPIPartition\n* Repository: https://github.com/ArgonneCPAC/MPIPartition\n\n\nFeatures\n--------\n\n* Cartesian partitioning of a cubic volume among available MPI ranks\n* distributing particle-data among ranks to the corresponding subvolume\n* overloading particle-data at rank boundaries\n* exchaning particle-data according to a "owner"-list of keys per rank\n\n\nInstallation\n------------\n\nInstalling from the PyPI repository:\n\n.. code-block:: bash\n\n   pip install mpipartition\n\nInstalling the development version from the GIT repository\n\n.. code-block:: bash\n\n   git clone https://github.com/ArgonneCPAC/mpipartition.git\n   cd mpipartition\n   python setup.py develop\n\n\nRequirements\n------------\n\n* `mpi4py <https://mpi4py.readthedocs.io/en/stable/>`_: MPI for Python\n* `numpy <https://numpy.org/>`_: Python array library\n\n\nBasic Usage\n-----------\nCheck the `documentation <https://argonnecpac.github.io/MPIPartition>`_ for\nan in-depth explanation / documentation.\n\n.. code-block:: python\n\n   # this code goes into mpipartition_example.py\n\n   from mpipartition import Partition, distribute, overload\n   import numpy as np\n\n   # create a partition of the unit cube with available MPI ranks\n   partition = Partition(1.)\n\n   if partition.rank == 0:\n       print(f"Number of ranks: {partition.nranks}")\n       print(f"Volume decomposition: {partition.decomposition}")\n\n   # create random data\n   nparticles_local = 1000\n   data = {\n       "x": np.random.uniform(0, 1, nparticles_local),\n       "y": np.random.uniform(0, 1, nparticles_local),\n       "z": np.random.uniform(0, 1, nparticles_local)\n   }\n\n   # distribute data to ranks assigned to corresponding subvolume\n   data = distribute(partition, data, (\'x\', \'y\', \'z\'))\n\n   # overload "edge" of each subvolume by 0.05\n   data = overload(partition, data, 0.05, (\'x\', \'y\', \'z\'))\n\nThis code can then be executed with ``mpi``:\n\n.. code-block:: bash\n\n   mpirun -n 10 python mpipartition_example.py\n\n--------\n\nA more applied example, using halo catalogs from a\n`HACC <https://cpac.hep.anl.gov/projects/hacc/>`_ cosmological simulation (in\nthe `GenericIO <https://git.cels.anl.gov/hacc/genericio>`_ data format):\n\n.. code-block:: python\n\n   from mpipartition import Partition, distribute, overload\n   import numpy as np\n   import pygio\n\n   # create a partition with available MPI ranks\n   box_size = 64.  # box size in Mpc/h\n   partition = Partition()\n\n   # read GenericIO data in parallel\n   data = pygio.read_genericio("m000p-499.haloproperties")\n\n   # distribute\n   data = distribute(partition, box_size, data, [f"fof_halo_center{x}" for x in "xyz"])\n\n   # mark "owned" data with rank (allows differentiating owned and overloaded data)\n   data["status"] = partition.rank * np.ones(len(data["fof_halo_center_x"]), dtype=np.uint16)\n\n   # overload by 4Mpc/h\n   data = overload(partition, box_size, data, 4., [f"fof_halo_center{x}" for x in "xyz"])\n\n   # now we can do analysis such as 2pt correlation functions (up to 4Mpc/h)\n   # or neighbor finding, etc.\n',
    'author': 'Michael Buehlmann',
    'author_email': 'buehlmann.michi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ArgonneCPAC/MPIPartition',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
