# DSE
Dependability Simulation Engine

A discrete event simulator (DES) framework for modelling complex systems

## Context

The growth of computing power of modern computers and cloud systems focuses the attention on a new maintenance paradigm: the predictive maintenance. In this scenario, the component/subsystem is constantly monitored: related data are constantly captured and analyzed by remote computers mainly by means of machine learning techniques. Defining and testing new predictive maintenance algorithms is of paramount importance: since developing and assuring the quality of a new method can be costly, a simulation-based approach can be
a feasible way to accomplish this task.

## Objective

This repository contains a first version of a software framework whose purpose is to support the user in simulating complex systems. This is done by providing the basic abstract structure of a discrete event simulator, trying to minimize the case-specific coding activity. The idea is to take as input a high level description of the **System Under Study (SUS)**, a **Configuration/Maintenance File** and a **Specific Code** in order to produce **Simulation Logs** and **Quantitative Metrics**.

## Repository structure

The repository is structured as follows:
* core package: it is the fixed part of the simulator, it is project-independent and contains the definition of the classes and the functions needed for every simulation

* ertms package: it is an example of specific package used for the dependability analysis of the European Rail Traffic Management System/European Train Control System (ERTMS/ETCS) level 2 signalling railway system

* root directory: it contains the configuration file *config.ini*, the maintenance file *maintenance.ini* and the main python programme *dse.py*

## Dependencies

The whole framework is written in Python language (version 3.7). The packages that need to be installed for a correct behaviour are *simpy*, *numpy* and *scipy*

## Replication package

The *batch* folder is the replication folder. It contains:
* 




## Usage

The *dse.py* python programme takes as input 4 arguments:
* the *configuration file*
* the *maintenance file*
* the *log output file* i.e. the simulation log
* the *indices output file* i.e. the whole experiment output metrics

In alternative, one can just specify a folder (the *batch* folder is an example) that has to contain, for each experiment, the four files described previously, named respectively as [filename].ini, [filename].mnt, [filename].log and [filename] .ind. If more filenames are specified (i.e. multiple experiments want to be executed), they will be run in series.

### Configuration file structure


### Maintenance file structure


## Output



## License
The software is licensed according to the GNU General Public License v3.0 (see License file).

## Feedback
Anyone can report bugs on GitHub! Here's how it works:
* Click “New issue” and choose the appropriate format.
* Fill out the template with all the relevant info.