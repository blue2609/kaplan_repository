#Program: NN_Iris.r
#Author: Sanjeev adpated from
#Date: July 2020


#install.packages("neuralnet")
#install.packages("NeuralNetTools")
#install.packages("ggplot2")
#install.packages("GGally")
#install.packages("caret")

library("neuralnet")
library("NeuralNetTools")
library("ggplot2")
library("GGally")
library("caret")

data(iris)

ggplot <- function(...) 
  ggplot2::ggplot(...) + 
  scale_color_brewer(palette="Purples") + 
  scale_fill_brewer(palette="Purples")

unlockBinding("ggplot",parent.env(asNamespace("GGally")))
assign("ggplot",ggplot,parent.env(asNamespace("GGally")))

graph_corr <- ggpairs(iris, mapping = aes(color = Species), 
                      columns = c('Sepal.Length', 
                                  'Sepal.Width', 
                                  'Petal.Length', 
                                  'Petal.Width', 
                                  'Species'), 
                      columnLabels = c('Sepal.Length', 
                                       'Sepal.Width', 
                                       'Petal.Length', 
                                       'Petal.Width', 
                                       'Species')) 
graph_corr <- graph_corr + theme_minimal()
graph_corr

#One of the most important procedures when forming a neural network is data normalization. 
#This involves adjusting the data to a common scale so as to accurately compare predicted and actual values. 
#Failure to normalize the data will typically result in the prediction value remaining the same across all observations, regardless of the input values.

#We can do this in two ways in R:
  
#  Scale the data frame automatically using the scale function in R
#Transform the data using a max-min normalization technique. 
#In this example, will be to use Max-Min Normalization function.
norm.fun = function(x){(x - min(x))/(max(x) - min(x))}

#Apply function to normalise data()

df_iris = iris[,c("Sepal.Length","Sepal.Width",
                  "Petal.Length","Petal.Width" )]

df_iris = as.data.frame(apply(df_iris, 2, norm.fun))

df_iris$Species = iris$Species

df_iris$setosa <- df_iris$Species=="setosa"
df_iris$virginica <- df_iris$Species == "virginica"
df_iris$versicolor <- df_iris$Species == "versicolor"

## 75% of the sample size
smp_size <- floor(0.75 * nrow(df_iris))

## set the seed to make your partition reproducible
set.seed(123)
train_ind <- sample(seq_len(nrow(df_iris)), size = smp_size)

training.set <- df_iris[train_ind, ]
test.set <- df_iris[-train_ind, ]


model = as.formula("Species ~ 
                           Sepal.Length + 
                           Sepal.Width + 
                           Petal.Length + 
                           Petal.Width")

iris.net <- neuralnet(model,
                      data=training.set, 
                      hidden=c(10,10), 
                      rep = 5, 
                      act.fct = "logistic",
                      err.fct = "ce",
                      linear.output = F, 
                      lifesign = "minimal", 
                      stepmax = 1000000,
                      threshold = 0.001)

plotnet(iris.net, 
        alpha.val = 0.8, 
        circle_col = list('purple', 'white', 'white'), 
        bord_col = 'black')

iris.prediction <- compute(iris.net, test.set)

idx <- apply(iris.prediction$net.result, 1, which.max)

predicted <- as.factor(c('setosa', 'versicolor', 'virginica')[idx])

confusionMatrix(predicted, test.set$Species)

