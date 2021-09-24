# DDLP-PhD-Thesis
Study of algorithmic efficiency for a combinatorial optimization problem.

## Description

This project is the subject of my Ph.D. thesis. I worked on an NP-Complete problem to demonstrate its inherent
difficulty by studying a phase transition phenomenon that emerged from a probabilistic model of the Data Delivery
problem. A significant amount of work consisted in running simulations. I wrote the code in Python.

## Using/Browsing the Code

The source/ directory contains all of the code.

### Data Delivery Class

This is a class to represent instances of the Data Delivery on a Line Problem (DDLP).

    DataDelivery.py
    
### Connectivity

This module deals with the connectivity properties of the DDLP problem.

    DDLP_Connectivity.py
    
### Forward heuristics

This module contains the forward heuristics.

    DDLP_Heuristic.py
    
### Random

This module deals with the random instance generator from the probabilistic model.

    DDLP_Random.py
    
### Density plot

This code is to generate density plots of the empirical probability of solvability for random DDLP instances using the Backtrack algorithm developed for this purpose.

    DensityPlot_EDL.py
    
It takes as arguments:

    width
    min_radius
    max_radius
    min_number_robots
    max_number_robots
    trials 
    epsilon

Example of running DensityPlot_EDL.py:

    ./python DensityPlot_EDL.py 1 0 1 0 50 5 0.05

Running the code would generate a graphic like this:

![Figure_1](https://user-images.githubusercontent.com/13812290/134736938-c13cd963-f001-4b54-a7fe-5e1f629c99b1.png)

A Google Colab notebook to run the code on your browser (Ctrl+F9) is found here:
https://colab.research.google.com/drive/12IsW5GONcCRSNTt3E2dJAThD5cLTrVe_?usp=sharing

   
### Data Delivery Class

This is a class to represent instances of the Data Delivery on a Line Problem (DDLP).

    DataDelivery.py
    
### Connectivity

This module deals with the connectivity properties of the DDLP problem.

    DDLP_Connectivity.py
    
### Forward heuristics

This module contains the forward heuristics.

    DDLP_Heuristic.py
    
### Random

This module deals with the random instance generator from the probabilistic model.

    DDLP_Random.py
    
### Backward heuristics

This module contains the backward heuristics.

   DDLP_ReverseHeuristic.py

### Scheinerman's model 

This code is to experimentally test Scheinerman's Theorem about the connectivity threshold for random interval graphs. Scheinermann.py takes as arguments:

    width = 1.0
    min_radius = 0.0
    max_radius = 1.0
    min_number_robots = 0
    max_number_robots = 50
    trials = 5

Example of running Scheinermann.py:

    ./python Scheinermann.py 1 0 1 0 50 5

Running the code would generate a graphic like this:

![width=1 0 max_radius=1 0 max_n=50 trials=5 rows=50 cols=50_Scheinerman-1](https://user-images.githubusercontent.com/13812290/134735538-80bf170e-ae42-45f3-86f8-c1df3ea956d4.png)

A Google Colab notebook to run the code on your browser (Ctrl+F9) is found here:
https://colab.research.google.com/drive/10oNKfeXd6yWUkTbuOl3hLMdOTgZDqBKb#scrollTo=GyoaL01Ksl5G

