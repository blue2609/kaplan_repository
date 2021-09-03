[TOC]

# Introduction

This repository stores all projects, datasets and scripts related to KBS MBATS Environment. 

Sub-directories which contain datasets and scripts uploaded/written to MBATS by teachers are:

- `KBS_Datasets`: Contains all Excel, CSV, txt and compressed folders datasets used by lecturers in the MBATS environment
- `KBS_Python`: Contains all Python scripts constructed downloaded/written by lecturers and instructors at KBS
- `KBS_R`: Contains all R related scripts & output as well as Spotfire workbook/output constructed downloaded/written by lecturers and at KBS

All other sub-directories in this repository are mini-projects which aim to make the task of administering MBATS environment easier:

- `ApplicationUpdateScraper`: This project aims to check updates to certain MBATS applications automatically 
- `AutomateAppUpdate`: This project aims to use a package manager like **chocolatey** to automatically install application updates 
- `AutomateSQLImport`: A tool which enables its user to create many SQL Server tables quickly from a directory that contains many Excel and CSV files
- `ControlExploratoryProcess`: A simple Powershell script project which will prevent more than 1 lecturer to use **Exploratory Desktop** application on MBATS Prod server at the same time
- `GoogleColab`: Contains all Python and bash scripts that can be used to:
    - Connect Google Colab to a SQL Server Database
    - Connect Google Colab to a private remote repository
    - Run a small flask webapp from Google Colab (this is just an experiment)

- `R_Package_Management`: This project aims to make it easier for MBATS environment administrators and lecturers at KBS to manage R packages

# Cloning a Sub-Directory/Project

It is possible for a user to clone only a single sub-directory/project from this repository. In order to do so, the `sparse-checkout` feature of git can be utilised:

- First, create a new empty directory and go inside that directory
- initialise git repository in this new empty directory with `git init`
- Enable sparse checkouts with this command: `git config core.sparsecheckout true`
- Tell git which sub-directory you want to clone by either doing:
    - `echo <sub_directory_name> >> .git/info/sparse-checkout` OR
    - edit `.git/info/sparse-checkout` directly and write the sub-directory name that you want in this file

- Then, add the remote repository by running this command: `git remote add -f origin git@bitbucket.org:KaplanAustralia/kbs-mbats-environment.git`
- Finally, pull fetch the content of the repository using `git pull master origin`
