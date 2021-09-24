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
    
### Backward heuristics

This module contains the backward heuristics.

    DDLP_ReverseHeuristic.py
    
### Random

This module deals with the random instance generator from the probabilistic model.

    DDLP_Random.py
    
### Density plot (Backtrack)

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

### Density plot for FDDLP (Forward Data Delivery on a Line Problem)

This code is to generate density plots of the empirical probability of solvability for random FDDLP instances using a polynomial algorithm developed for this purpose.

    DensityPlot_EDLA.py
    
It takes as arguments:

    width
    min_radius
    max_radius
    min_number_robots
    max_number_robots
    trials 
    epsilon

Example of running DensityPlot_EDLA.py:

    ./python DensityPlot_EDLA.py 1 0 1 0 50 5 0.05

Running the code would generate a graphic like this:

![Figure_2](https://user-images.githubusercontent.com/13812290/134738330-4172290b-751b-4d2e-90bd-683e87355050.png)

A Google Colab notebook to run the code on your browser (Ctrl+F9) is found here:
https://colab.research.google.com/drive/17c6QgocmOW0AJb_g3IYm-B-pW0bW4VIi?usp=sharing

### Scheinerman's model

This code is to experimentally test Scheinerman's Theorem about the connectivity threshold for random interval graphs.

    Scheinermann.py
    
It takes as arguments:

    width
    min_radius
    max_radius
    min_number_robots
    max_number_robots
    trials

Example of running Scheinermann.py:

    ./python Scheinermann.py 1 0 1 0 50 5

Running the code would generate a graphic like this:

![width=1 0 max_radius=1 0 max_n=50 trials=5 rows=50 cols=50_Scheinerman-1](https://user-images.githubusercontent.com/13812290/134737689-5a01d469-f3c7-45fa-a913-fbd63097906b.png)

A Google Colab notebook to run the code on your browser (Ctrl+F9) is found here:
https://colab.research.google.com/drive/10oNKfeXd6yWUkTbuOl3hLMdOTgZDqBKb#scrollTo=GyoaL01Ksl5G

### Exploring Nodes in the Backtrack tree 

This code is a graphic visualization of the empirical probability of a randomly generated instance, with parameters (n,r), to have a large number of nodes to be explored by the Backtrack algorithm.

    Nodes_EDL.py
    
It takes as arguments:

    width
    min_radius
    max_radius
    min_number_robots
    max_number_robots
    trials 
    epsilon

Example of running Nodes_EDL.py:

    ./python Nodes_EDL.py 1 0 1 0 50 5 0.05

Running the code would generate a graphic like this:

![Figure_4](https://user-images.githubusercontent.com/13812290/134740806-3f405e36-0142-44be-8307-f4426755285f.png)

A Google Colab notebook to run the code on your browser (Ctrl+F9) is found here:
https://colab.research.google.com/drive/12tnJO0D1G8R_zrNYV0Kg1dqX1Ta080IY?usp=sharing

### Testing difficult instances with approximation algorithms.

This code is a graphic visualization of the empirical probability of a randomly generated instance, with parameters (n,r), to be solved by ten different approximation algorithms (heuristics) and backtrack on instances presumably difficult.

    Difficult_EDL.py
    
It takes as arguments:

    width
    min_radius
    max_radius
    min_number_robots
    max_number_robots
    trials 
    epsilon

Example of running Difficult_EDL.py:

    ./python Difficult_EDL.py 1 0 1 0 50 5 0.05

Running the code would generate a graphic like this:

![Figure_5](https://user-images.githubusercontent.com/13812290/134742489-ac800d78-13e8-482e-8091-04985dfb6b0e.png)

A Google Colab notebook to run the code on your browser (Ctrl+F9) is found here:
https://colab.research.google.com/drive/10A1vursHf-1DGyT0R41zAT_EckKG0KgC?usp=sharing

