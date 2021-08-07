
# loading packages
#library(forecast)
library('forecast',lib.loc = 'C:/Program Files/R/R-3.6.1/library')
library(Metrics)

# reading data 
data <- read.csv("C:/Users/Public/Documents/Datasets/DATA 4400/AirPassengers.csv")

#You can use this in model to just get the parameters 
data_ts= ts(data[-1],start=2010,frequency=12) 

# splitting data into train and valid sets (we could also use subset)
train <- data[1:100,]
valid <- data[101:nrow(data),]

nrow(train);nrow(valid)

train_ts<-ts(train[-1], start=2010, frequency=12)


# training model
model <- auto.arima(train_ts,D=1)

# model summary
summary(model)

forecastR<-forecast(model,level=c(95), h=nrow(valid))
autoplot(forecastR) +autolayer(data_ts)