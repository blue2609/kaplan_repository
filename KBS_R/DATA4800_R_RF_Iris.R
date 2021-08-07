#Program R_RF_Iris.R
# Simple Random Forest model in R to be used in week 3 of DATA 4800
#Author: Sanjeev Naguleswaran
#Date: June 2020


#install.packages("randomForest")
#install.packages("Mass")
#install.packages("caret")

library(randomForest)
library(ROCR)
library(datasets)
data(iris)
head(iris)

library(MASS)
library(caret)

# USe the set.seed function so that we get same results each time
set.seed(123)
data(iris)
View(iris)


# Splitting data into training and testing. As the species are in order
# splitting the data based on species
iris_setosa <- iris[iris$Species == "setosa", ] # 50
iris_versicolor <- iris[iris$Species == "versicolor", ] # 50
iris_virginica <- iris[iris$Species == "virginica", ] # 50
iris_train <-
  rbind(iris_setosa[1:25, ], iris_versicolor[1:25, ], iris_virginica[1:25, ])
iris_test <-
  rbind(iris_setosa[26:50, ], iris_versicolor[26:50, ], iris_virginica[26:50, ])

rf <- randomForest(Species ~ ., data = iris_train)
rf  # Description of the random forest with no of trees, mtry = no of variables for splitting

# each tree node.
# Out of bag estimate of error rate is 4 % in Random Forest Model.
attributes(rf)
pred1 <- predict(rf, iris_train)
head(pred1)
head(iris_train$Species)

# looks like the first six predicted value and original value matches.

confusionMatrix(pred1, iris_train$Species)  # 100 % accuracy on training data

# Around 95% Confidence Interval.
# Sensitivity for all three species/categories is 100 %

# Prediction with test data - Test Data
pred2 <- predict(rf, iris_test)
confusionMatrix(pred2, iris_test$Species) # 94,67 % accuracy on test data
# Error Rate in Random Forest Model :
plot(rf)



# Calculate the probability of new observations belonging to each class
# prediction_for_roc_curve will be a matrix with dimensions data_set_size x number_of_classes
prediction_for_roc_curve <- predict(rf, iris_test[, -5], type = "prob")

# Use pretty colours:
pretty_colours <- c("#F8766D", "#00BA38", "#619CFF")

# Specify the different classes
classes <- levels(iris_test$Species)

# For each class
for (i in 1:3)
{
  # Define which observations belong to class[i]
  true_values <- ifelse(iris_test[, 5] == classes[i], 1, 0)
  # Assess the performance of classifier for class[i]
  pred <- prediction(prediction_for_roc_curve[, i], true_values)
  perf <- performance(pred, "tpr", "fpr")
  if (i == 1)
  {
    plot(perf, main = "ROC Curve", col = pretty_colours[i])
  }
  else
  {
    plot(perf,
         main = "ROC Curve",
         col = pretty_colours[i],
         add = TRUE)
  }
  # Calculate the AUC and print it to screen
  auc.perf <- performance(pred, measure = "auc")
  print(auc.perf@y.values)
}
