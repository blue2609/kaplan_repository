[TOC]

# Introduction

This repository stores all projects, datasets and scripts related to KBS MBATS Environment. 

Sub-directories which contain datasets and scripts uploaded/written to MBATS by teachers are:

- `KBS_Datasets`: Contains all Excel, CSV, txt and compressed folders datasets used by lecturers in the MBATS environment
- `KBS_Python`: Contains all Python scripts constructed downloaded/written by lecturers and instructors at KBS
- `KBS_R`: Contains all R related scripts & output as well as Spotfire workbook/output constructed downloaded/written by lecturers and at KBS

All other sub-directories in this repository are mini-projects which aim to make the task of administering MBATS environment easier:


|Sub-Directory Name|Purpose of Project|Project Status|
|-------|--------|--------|
|`ApplicationUpdateScraper`|This project aims to check updates to certain MBATS applications automatically|Discontinued. Not really sure how useful this is as most applications can be managed with package managers like Chocolatey, conda/mamba/pip, Renv, etc.|
|`AutomateAppUpdate`|This project aims to use a package manager like **chocolatey** to automatically install application updates. In the future, someone might consider to continue working on this project should Kaplan decides to create a workflow that can automate application updates with package managers|Not done
|`AutomateSQLImport`| A tool which enables its user to create many SQL Server tables quickly from a directory that contains many Excel and CSV files|**[WORKING]** Can actually be used to automatically create SQL Server tables from CSV and Excel files on any server (not just MBATS)
|`ControlExploratoryProcess`|A simple Powershell script project which will prevent more than 1 lecturer to use **Exploratory Desktop** application on MBATS Prod server at the same time|This one is already deployed on MBATS Prod to prevent more than one lecturer from using Exploratory Desktop application on the r
|`GoogleColab`|Contains all Python and bash scripts that can be used to **Connect Google Colab to a SQL Server Database**, **Connect Google Colab to a private remote repository**,**Run a small flask webapp from Google Colab (this is just an experiment)**|These scripts actually work on Google Colab but the thing is, if KBS insists on using Google Colab, how can it be integrated with our current MBATS Environment?
|`internalizing_packages`|A project (currently only a concept with README and no code) that attempts to internalise data analytics packages as well as Kaplan's internal scripts and projects | Not started yet, currently only consists of README so someone in the future can continue the project
|`publishAppsScripts`|This directory contains a few PowerShell scripts that you can use to deploy a Remote app to RDWeb|The scripts in this directory are actually working, they're some very simple scripts whith utilises the **`New-RDRemoteApp`** PowerShell cmdlet
|`R_Package_Management`|This project aims to make it easier for MBATS environment administrators and lecturers at KBS to manage R packages| Not done, it turns out the proper way of managing R packages is with something called **'Renv'** package manager and for anyone who wants to continue working on this project in the future please look into that Renv and keep working on this sub-directory
|`RebuildApplication`|This project aims to create a PowerShell script that can automate the installation of data analytics applications on a fresh/clean Windows Server|**[WORKING, partially done]** Unfortunately, due to time constraint, the only component of the project completed was the Conda environment rebuilding portion. There are still a couple other components to the project which need to be done in order to automate the whole data analytics applications installation process on a fresh Windows Server

     

# Cloning a Sub-Directory/Project

# Using `sparse-checkout`

---
**WARNING**

This is actually not perfect. It seems like the method below will still clone the whole project to the user's local machine but it just doesn't bring all files into the working directory of the project. 

The issue here is if the user is working with a Linux/UNiX terminal environment with Powerlevel10k theme, the terminal will indicate that there are hundreds of untracked/modified files in the repository when there's actually no new, untracked/modified file in the project directory

Hence, please proceed with caution. Please ask someone from the Devops team on how to do this properly in the future!

In the meantime, maybe it would be safer to just clone the whole repository for now (including all the datasets)

---
It is possible for a user to clone only a single sub-directory/project from this repository. In order to do so, the `sparse-checkout` feature of git can be utilised:

- First, create a new empty directory and go inside that directory
- initialise git repository in this new empty directory with `git init`
- Enable sparse checkouts with this command: `git config core.sparsecheckout true`
- Tell git which sub-directory you want to clone by either doing:
    - `echo <sub_directory_name> >> .git/info/sparse-checkout` OR
    - edit `.git/info/sparse-checkout` directly and write the sub-directory name that you want in this file

- Then, add the remote repository by running this command: `git remote add -f origin git@bitbucket.org:KaplanAustralia/kbs-mbats-environment.git`
- Finally, pull fetch the content of the repository using `git pull master origin`
