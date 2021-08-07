
# ------------------------------------------------------------------------------------------------------------------------
# This script assumes that the machine it's run on already has 'tools' and 'sets' libraries installed on it'
# ------------------------------------------------------------------------------------------------------------------------

library('tools')
library('sets')

PACKAGE_NAME = ''
installDirs <- .libPaths()
requiredPackages <- commandArgs(trailingOnly = TRUE)
# print(args)


# ------------------------------------------------------------------------------------------------------------------------
# << HELPER FUNCTIONS >> 
# ------------------------------------------------------------------------------------------------------------------------

getUserDependencies <- function(packagename,user_packages){
    suggested_packages <- unlist(package_dependencies(packagename,recursive=TRUE))
    # return (suggested_packages)
    
    # # check if any of the suggested packages are already installed in user level directory
    user_installed_dependencies <- intersect(suggested_packages,user_packages)

    return (user_installed_dependencies)
}

getSystemDependencies <- function(packagename,system_packages){
    suggested_packages <- unlist(package_dependencies(packagename,recursive=TRUE))
    # return (suggested_packages)
    
    # # check if any of the suggested packages are already installed in user level directory
    system_installed_dependencies <- intersect(suggested_packages,system_packages)

    return (system_installed_dependencies)
}

# ------------------------------------------------------------------------------------------------------------------------
# << Main Program starts here >> 
# ------------------------------------------------------------------------------------------------------------------------

# try to get the user and system installation directories
for (installDir in installDirs){
    if (grepl('C:/Users',installDir,fixed=TRUE)){
        userInstallDir <- installDir
    }else if(grepl('C:/Program Files',installDir)){
        systemInstallDir <- installDir
    }
}

ip_df <- as.data.frame(installed.packages())
ip_df <- ip_df[c('Package','LibPath')]

# get user and system installed packages and save them into 2 separate dataframes
user_ip_df <- ip_df[ip_df$LibPath == userInstallDir,]
user_packages <- rownames(user_ip_df)
user_packages<-sub("\\.\\d","",user_packages)

system_ip_df <- ip_df[ip_df$LibPath == systemInstallDir,]
system_packages <- rownames(system_ip_df)
system_packages<-sub("\\.\\d","",system_packages)

missingSysPkgs <- setdiff(requiredPackages,system_packages)
print(missingSysPkgs)


# # only execute the code below if PACKAGE_NAME is not an empty string
# if (PACKAGE_NAME != ''){
#     package_dir <- ip_df[PACKAGE_NAME,c('Package','LibPath')]

#     # make sure that the package hasn't been installed on system-level directory
#     if(nrow(package_dir) > 0){
#         for (installDir in package_dir$LibPath){
#             if (installDir == userInstallDir){
#                 is_package_installed <- paste("'",PACKAGE_NAME,"' already installed in User Directory")
#             }else if (installDir == systemInstallDir){
#                 is_package_installed <- paste("'",PACKAGE_NAME,"' already installed in system Directory")
#             }
#         }
#     }else{
#         is_package_installed <- paste("'",PACKAGE_NAME,"' hasn't been installed anywhere")
#     }

#     # user_installed_dependencies <- getUserDependencies(PACKAGE_NAME,user_packages)
#     user_installed_dependencies <- getUserDependencies(PACKAGE_NAME,user_packages)
#     system_installed_dependencies <- getSystemDependencies(PACKAGE_NAME,system_packages)

#     # ------------------------------------------------------------ 
#     # Print out useful messages
#     # ------------------------------------------------------------ 
#     print(paste('USER_INSTALL_DIR:',userInstallDir))
#     print(paste('SYSTEM_INSTALL_DIR:',systemInstallDir))
#     print(paste('IS_PACKAGE_INSTALLED:',is_package_installed))
#     print(paste('USER_INSTALLED_DEPENDENCIES:',user_installed_dependencies))
#     print(paste('SYSTEM_INSTALLED_DEPENDENCIES:',system_installed_dependencies))
# }