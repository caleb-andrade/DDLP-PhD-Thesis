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

![width=1 0 max_radius=1 0 max_n=50 trials=5 rows=50 cols=50_Scheinerman-1](https://user-images.githubusercontent.com/13812290/134732761-76770fe2-7a80-40f7-947b-739a0ade7b83.png)


A Google Colab notebook to run the code on your browser is found here:
https://colab.research.google.com/drive/10oNKfeXd6yWUkTbuOl3hLMdOTgZDqBKb#scrollTo=GyoaL01Ksl5G

