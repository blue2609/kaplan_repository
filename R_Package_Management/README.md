# Introduction

This project aims to do several things:

- create a new environment for a specific folder Path that contains R scripts/R markdowns. 
- Make sure all required packages to run KBS R scripts can be restored when R is updated to a newer version
- Check that all R scripts can run without any error
  
# New (Better) Solution 

This solution will use **Renv** package to create a project private environment/library isolated for each directory containing R scripts and R markdowns. **Renv** will also be the one to detect dependencies and save the dependencies for a an R project/directory in a file calld **Renv.lock** (it's a JSON file)

# Old Solution

There is a directory in this branch called **R Package Install (Old)*. This directory contains the Python and R scripts which can detect:

- Which R packages are already installed to system-level
- Which R packages are already installed to user-level (will vary for each user)
