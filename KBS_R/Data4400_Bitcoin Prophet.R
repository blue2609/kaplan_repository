#installing the packages
#install.packages("prophet")
library(prophet)
library(tidyverse)

#loading the dataset
bitcoin <- read.csv("C:/Users/Public/Documents/Datasets/DATA 4400/BitcoinPrices.csv")
head(bitcoin)

# Filtering down to only include dates and prices
data <- bitcoin %>% select(Date, Closing.Price..USD.)

# Changing dates to date format
data$Date <- as.Date(data$Date, format = '%d/%m/%Y')

#Renaming columns Date to ds and Closing.Price..USD. to y
names(data)[names(data) == "Date"] <- "ds"
names(data)[names(data) == "Closing.Price..USD."] <- "y"

#calling the prophet function to fit the model
Model1 <- prophet(data)
Future1 <- make_future_dataframe(Model1, periods =365)
tail(Future1)

Forecast1 <- predict(Model1, Future1)
tail(Forecast1[c('ds','yhat','yhat_lower','yhat_upper')])

#Plotting the Model Estimates
dyplot.prophet(Model1, Forecast1)
prophet_plot_components(Model1, Forecast1)
