# Pigz wrapper

This repository is a wrapper for python to utilize gzip or pigz to compress or decompress data in parallel.

For installation:

    python setup.py install

For reading:

    from pigz import PigzFile
    with PigzFile("input.gz") as f:
        for line in f:
            print(line)

For writing:

    from pigz import PigzFile
    threads = 4 # default
    with PigzFile("output.gz", "wt", threads) as fw:
        for line in lines:
            fw.write(line)

For testing:

    python setup.py test

the output is as follows:

    ============================================================
    Read by gzip subprocess:
    Number: 1, Time: 585.19 ms
    Number: 2, Time: 726.82 ms
    Number: 3, Time: 698.48 ms
    Number: 4, Time: 728.64 ms
    Number: 5, Time: 698.70 ms
    Average time: 687.57 ms
    ============================================================
    Write by gzip subprocess:
    Number: 1, Time: 13652.26 ms
    Number: 2, Time: 13413.61 ms
    Number: 3, Time: 13303.46 ms
    Number: 4, Time: 13369.65 ms
    Number: 5, Time: 13340.88 ms
    Average time: 13415.97 ms
    ============================================================
    Read by pigz subprocess (4 threads):
    Number: 1, Time: 339.37 ms
    Number: 2, Time: 403.47 ms
    Number: 3, Time: 401.11 ms
    Number: 4, Time: 408.30 ms
    Number: 5, Time: 425.89 ms
    Average time: 395.63 ms
    ============================================================
    Write by pigz subprocess (4 threads):
    Number: 1, Time: 3562.05 ms
    Number: 2, Time: 3511.68 ms
    Number: 3, Time: 3519.51 ms
    Number: 4, Time: 3518.98 ms
    Number: 5, Time: 3513.09 ms
    Average time: 3525.06 ms
    ============================================================
    Read by gzip package:
    Number: 1, Time: 867.79 ms
    Number: 2, Time: 915.57 ms
    Number: 3, Time: 893.22 ms
    Number: 4, Time: 885.66 ms
    Number: 5, Time: 889.74 ms
    Average time: 890.40 ms
    ============================================================
    Write by gzip package:
    Number: 1, Time: 66520.40 ms
    Number: 2, Time: 66305.25 ms
    Number: 3, Time: 65591.92 ms
    Number: 4, Time: 65327.56 ms
    Number: 5, Time: 65716.15 ms
    Average time: 65892.26 ms

The pigz subprocess show significantly high effectiveness in compressing and decompressing data.