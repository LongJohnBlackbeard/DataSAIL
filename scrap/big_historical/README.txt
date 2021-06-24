The big_historical_v2_cython.pyx script can be built with the following command:
  python3 setup_v2.py build_ext --inplace

The cython helper library must be built on the target machine/architecture
before running the big_historical_v2.py script.

The big_historical_v2.py script can then be run with the command:
  python3 big_historical_v2.py

Although, the script can take longer to run than an ssh session lasts.
The following command was used to run the script during development:
  nohup python3 big_historical_v2.py

The big_historical_v2.py script relies on multiprocessing and was tuned
for Siren. big_historical_v2_cython.pyx should probably only be built
on Siren and the big_historical_v2.py script should probably only
be run on Siren, as it is currently tuned.
