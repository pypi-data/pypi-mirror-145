Selecting Instance Types
========================


When creating clusters, Coiled will match the instance type with the
requirements that you specify for CPU, Memory and GPU. Coiled chooses five
instance types to serve as a fallback when creating a Cluster since sometimes
a specific instance type might not be available in your cloud provider of choice.

You might not wish to get allocated random instance types, and you might want to
provide a list of instance types when creating a Cluster. This will allow you to
have more fine-grain control of the type of Cluster that you create.

With the keyword argument ``scheduler_vm_types`` and ``worker_vm_types``, you can
specify instance types for both the Scheduler and Workers. For example:

.. code:: python

  import coiled

  cluster = coiled.Cluster(
      scheduler_vm_types=["t3.large", "t3.xlarge"],
      worker_vm_types=["m5n.large", "m5zn.large"],
  )

It's recommended that you specify more than one instance type in your list to
avoid instance availability issues in the cloud provider and region that
you are using Coiled.

.. note::

  The order of the instance type will not be preserved when creating the cluster.


Specifying Instance Types
-------------------------


You can use the command :meth:`coiled.list_instance_types()` to see a list of all
allowed instance types for your configured cloud provider.

.. code:: python

  import coiled

  coiled.list_instance_types()

You can also specify  one or a combination of keyword arguments (``cores``, ``memory`` and
``gpus``) to filter these results.

.. code:: python

  import coiled

  # Filter instances that have 4 cores only
  coiled.list_instance_types(cores=4)

  # Filter instances by cores and memory
  coiled.list_instance_types(cores=2, memory="8 Gib")

The ``list_instance_types`` command also allows you to specify a range in what to filter instances by.
For example:

.. code:: python

  import coiled

  coiled.list_instance_types(cores=[2, 8])

You might be interested in reading :doc:`select_gpu_type`.
