# ================================================ 
#	This Script Requires these packages:
#	- renv
# 	- rtools
# 	- usethis
# ================================================ 
library(usethis)
library(renv)
# library(installr)

usethis::create_project(path="C:/Users/Public/Documents/R Scripts",rstudio=TRUE,open=TRUE)

# initialise a new renv for the project 
renv::init(bare=TRUE)

# for some reason, when doing renv::init() to install all dependencies, it often gets stuck. 
# renv::init()

# # get the list of required packages
required_packages <- unique(renv::dependencies()$Package)

# install all the required packages and generate the renv.lock file 
# to record all the packages installed
install.packages(required_packages,type="binary")
renv::snapshot()

