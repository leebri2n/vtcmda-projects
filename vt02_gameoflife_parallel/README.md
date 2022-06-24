This is a school project for CMDA3634, Computer Science Foundations for Computational Modeling and Data Analytics, submitted most recently on 8 December, 2021. Therefore, all code is omitted so as to uphold academic integrity. Only final results are shown.

In this project, I implement multiple working versions of John Conway's Game of Life simulation. The first iteration, in Python is a rapid prototype for the logic and functionality of the simulation. The second iteration, now implemented in C, is the first-pass performant solution. The third iteration, which is also in implemented in C, modifies the program to run parallel in a shared-memory environment through OpenMP on one nodes on Virginia Tech's Advanced Research Computing (ARC) cluster. Lastly, the fourth iteration, which is also implemented in C, modifies the simulation to run parallel in a distributed memory environment through the Message Passing Interface (MPI) across multiple nodes on Virginia Tech's Advanced Research Computing (ARC) cluster. The C implementations hold the grid data in a 1D array such that each "cell" on the grid has four channels for RGBA values, which hold floats.

Through this project, not only was I able to learn the C programming language, but I was also able to write parallel computing programs for the first time. Upon examining at the scalability studies in the runtimes, the benefits of adding more processors and nodes can be seen plots of runtime and speedup as well as sheer computing power. For the fourth implementation in particular, my teammate Cara Dunnavant and I were able to harness the capabilities of MPI to submit and run batch jobs of up to 100,000 by 100,000 grids across two nodes, a great amount of data.

More information on John Conway's Game of Life:
https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
https://en.wikipedia.org/wiki/Cellular_automaton
http://pi.math.cornell.edu/~lipa/mec/lesson6.html

Supporting materials and implementations written by Dr. Russell J. Hewett:
https://code.vt.edu/rhewett/cmda3634_materials.git
