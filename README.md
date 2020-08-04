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

The *replication* folder contains the material to demonstrate what reported in the published and submitted scientific papers related to the tool. At this date, the folder is fully devoted to the paper submitted to RSDA 2020 workshop. It contains:
* a *config.ini* of the ERTMS/ETCS case study
* a *maintenance.ini* of the ERTMS/ETCS case study
* a *indices.log* the file containing the quantitative metrics of the case study
* four *output.log.** that reports the four executions requested in the config.ini.


## Usage

The *dse.py* python programme takes as input 4 arguments:
* the *configuration file*
* the *maintenance file*
* the *log output file* i.e. the simulation log
* the *indices output file* i.e. the whole experiment output metrics

In alternative, one can just specify a folder (the *batch* folder is an example) that has to contain, for each experiment, the four files described previously, named respectively as [filename].ini, [filename].mnt, [filename].log and [filename].ind. If more filenames are specified (i.e. multiple experiments want to be executed), they will be run in series.

Both maintenance and configuration files are handled by the python package [*configparser*](https://docs.python.org/3/library/configparser.html), so they follow the default schema accepted by the parser.
A generic configuration file needs to have the following structure:  
[SECTION]  
attribute_1 = value_1  
attribute_2 = value_2  
.  
.  
attribute_n = value_n  

where each value is imported as a string


### Configuration file structure

The configuration file needs to contain the following sections:
* main/comm, that contain the hyperparameters of the experiment and the execution policy
* the system-specific sections that describe the actual structure. In particular, there is a system-level section containing the description (i.e. the subsystems) of the system and a section for each part, containing the description of each component. Each component is modeled as a 4-ple following the representation *(name, N, K, MTBF)*, where N and K mean that the requirements for that subsystem to run properly is to have K components over N working. Check the file *config.ini* to see an example of a configuration file.

### Maintenance file structure

The maintenance file structure contains the following sections:
* main, that contains the general informations related to the mainteners
* the system-specific sections in which the MTTRs are specified
Check the file *maintenance.ini* to see an example of a maintenance file.

## Output
The output of each experiment is made up of two files: the simulation logs file and the quantitative metrics file

### Simulation logs
The name is self-explicative, the level of detail of the log can be specified in the configuration file. The DSE engine can output failures, warnings or simply each event that takes place during the simulation.
### Quantitative metrics
This is actually the most interesting part of the output: it contains all the quantitative metrics specified by the user in order to summarise the behaviour of the system (in this version the chosen metrics is the uptime of the system and of its components).


## License
The software is licensed according to the GNU General Public License v3.0 (see License file).

## Feedback
Anyone can report bugs on GitHub! Here's how it works:
* Click “New issue” and choose the appropriate format.
* Fill out the template with all the relevant info.
