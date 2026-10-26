# Ensures the simulator package root is on sys.path so `pytest` (as invoked by
# run.sh) can import the `sim` package regardless of the test rootdir. Pytest
# adds the directory containing this file to sys.path at collection time.
