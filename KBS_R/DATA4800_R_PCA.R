#Program R_PCA_Iris.R
# Simple Random Forest model in R to be used in week 4 of DATA 4800
#Author: Sanjeev Naguleswaran
#Date: June 2020

library(ggplot2)
library(cowplot) # required to arrange multiple plots in a grid
theme_set(theme_bw(base_size=12)) # set default ggplot2 theme
library(dplyr)
library(grid) # required to draw arrows
library(datasets)
data(iris)
head(iris)


#If we want to find out which characteristics are most distinguishing between iris plants, 
#we have to make many individual plots and hope we can see distinguishing patterns:
  
p1 <- ggplot(iris, aes(x=Sepal.Length, y=Sepal.Width, color=Species)) + geom_point()
p2 <- ggplot(iris, aes(x=Petal.Length, y=Petal.Width, color=Species)) + geom_point()
p3 <- ggplot(iris, aes(x=Sepal.Length, y=Petal.Length, color=Species)) + geom_point()
p4 <- ggplot(iris, aes(x=Sepal.Width, y=Petal.Width, color=Species)) + geom_point()
plot_grid(p1, p2, p3, p4, labels = "AUTO")

#In this particular case, it seems that petal length and petal width 
#are most distinct for the three species. Principal Components Analysis (PCA) allows us to systematically discover such patterns, and it works also when there are many more variables than just four.

#The basic steps in PCA are to (i) prepare a data frame that holds only the numerical columns of interest, (ii) scale the data to 0 mean and unit variance, and (iii) do the PCA with the function prcomp():

iris %>% select(-Species) %>% # remove Species column
  scale() %>%                 # scale to 0 mean and unit variance
  prcomp() ->                 # do PCA
  pca                         # store result as `pca`

# now display the results from the PCA analysis
pca

#The main results from PCA are the standard deviations and the rotation matrix. We will talk about them below. First, however, let?s plot the data in the principal components. Specifically, we will plot PC2 vs. PC1. 
#The rotated data are available as pca$x:

head(pca$x)

#As we can see, these data don?t tell us to which species which observation belongs. 
#We have to add the species information back in:

# add species information back into PCA data
pca_data <- data.frame(pca$x, Species=iris$Species)
head(pca_data)

ggplot(pca_data, aes(x=PC1, y=PC2, color=Species)) + geom_point()

#In the PC2 vs PC1 plot, versicolor and virginica are much better separated.

#Next, let?s look at the rotation matrx:

pca$rotation

#It tells us how much each variable contributes to each principal component. For example, Sepal.Width contributes little to PC1 but makes up much of PC2. Often it is helpful to plot the rotation matrix as arrows. This can be done as follows:

# capture the rotation matrix in a data frame
rotation_data <- data.frame(pca$rotation, variable=row.names(pca$rotation))
# define a pleasing arrow style
arrow_style <- arrow(length = unit(0.05, "inches"),
                     type = "closed")
# now plot, using geom_segment() for arrows and geom_text for labels
ggplot(rotation_data) + 
  geom_segment(aes(xend=PC1, yend=PC2), x=0, y=0, arrow=arrow_style) + 
  geom_text(aes(x=PC1, y=PC2, label=variable), hjust=0, size=3, color='red') + 
  xlim(-1.,1.25) + 
  ylim(-1.,1.) +
  coord_fixed() # fix aspect ratio to 1:1

#We can now see clearly that Petal.Length, Petal.Width, and Sepal.Length all contribute to PC1, and Sepal.Width dominates PC2.

#Finally, we want to look at the percent variance explained. 
#The prcomp() function gives us standard deviations (stored in pca$sdev). 
#To convert them into percent variance explained, we square them and then divide by the sum over all squared standard deviations:
percent <- 100*pca$sdev^2/sum(pca$sdev^2)
percent

#The first component explains 73% of the variance, the second 23%, the third 4% and the last 0.5%. We can visualize these results nicely 
#in a bar chart:

perc_data <- data.frame(percent=percent, PC=1:length(percent))
ggplot(perc_data, aes(x=PC, y=percent)) + 
  geom_bar(stat="identity") + 
  geom_text(aes(label=round(percent, 2)), size=4, vjust=-.5) + 
  ylim(0, 80)