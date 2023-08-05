Saving Results
===============

HDF5.py is a python module allowing to save a PreciSo Result object as an hdf5 file that can be read later. It adds to the preciso python module the function HDF5_make, taht can be run stand-alone or can be called when using runSimulation as usual.


How to create an hdf5 PreciSo result file
------------------------------------------



All folowing commands are to be run in an Anaconda prompt with preciso imported.

To create an hdf5 save file from an input file, run

.. code-block:: python

	preciso.HDF5_make([YourSavedFileTitle], [YourInputFilePath], [All preciso's simulation optionnal arguments (temp, write_limit, nodes, n_samples, debug)])

..

	- I exhort to name your HDF5 file with the '.hdf5' extension, although it is not mandatory.

	- By default, the HDF5 file will be saved in the current directory. You can specify another directory by adding to the arguments target_path = [YourDirectoryPath].

	- By default, you cannot overwrite an existing saved HDF5 file with the same name. I you want to do so, please add the argument mode='w'

	- You can save a python result object instead of running the simulation on the input file by adding res = [YourResultObject]. Note that you still need to specify the input file it comes from or the function will not run. You can omit the simulation optionnal arguments; the default ones will still be saved into the HDF5 file though.

I recommend to read HDF_make's documentation for any detailed information about the function arguments.



The function HDF5_make will NOT return the results object. If you want the result object on top of saving it, run instead of HDF5_make:

.. code-block:: python

	preciso.runSimulation([All preciso's usual arguments], save_title = [YourSavedFileTitle])

You can here use the optionnal arguments 'save_target_path' and 'save_mode' in the same way we use 'target_path' and 'mode' respectively with HDF5_make, and default saving comportments are strictly identical.

Again, all concerned arguments are reported in detail in runSimulation's documentation.


Result file structure
---------------------


The root group's attributes gathers all simulation parameters with their respective names as keys, and a string form of the input file at the key 'input'.

The root has three subgroups 'precipitation', 'distribution' and 'mechanics', referring to the associated attributes of the Results object. The arborecence then follows the same logic recursively
	
	- All value-like attribute are saved as attributes of the current group with their names as keys
	
	- All DataFrame attributes are saved in a subgroup of a related name with pandas.to_hdf; eventual metadata is saved as attributes of the group containing the DataFrame
	
	- All dictionnary-like attributes define a new sub group, which elements follow these 3 rules.

To read a dataframe in the hdf5 format, use pandas.read_hdf([theHDF5File], [yourSubgroupPath]). Read its documentation for further details.


Keys for nodes (concerns all three main groups), precipitates and steps (only in ditribution) follow the patterns 'node\_[node's number]', 'precipitate\_[precipitate's name]' and 'step\_[step's number]' respectively. Please consider avoiding naming precipitates with special characters, as it might raise some warnings during saving or reading process.

Remember that you can access to all group keys with 

.. code-block:: python

	[YourOpenedHdf5File][PathToAGroup].keys()

and to all attribute keys with

.. code-block:: python

	[YourOpenedHdf5File][PathToAGroup].attrs.keys()


If an attribute is optionnal (for example distributions), the related group has an boolean attribute 'Enabled'.

Note that all booleans values were saved as ints (1 for True and 0 for False), which usually does not require any type conversion for further use (like in conditionnal statements or assertions).

