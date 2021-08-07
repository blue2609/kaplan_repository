library(forecast)

data=read.csv("BigCat2.csv")

values=data$Value[1:82]
Actual=data$Actual

# convert data to time series so seasonality (12) can be specified
ts_values<-ts(values,frequency=12)
fit <- auto.arima(ts_values)

values_forecast <- forecast(fit, level=c(95), h=14)

#uplot in R studio
ts_Actual<-ts(Actual, frequency=12)
autoplot(values_forecast)+autolayer(ts_Actual)


values_future <- values_forecast$mean
values_original_fitted <- values_forecast$fitted
values_x <- values_forecast$x
upper_95 <- values_forecast$upper[,1]
lower_95 <- values_forecast$lower[,1]

# return objects to Spotfire
list(values_future = values_future,
     values_original_fitted = values_original_fitted,
     values_x = values_x,
     upper_95 = upper_95,
     lower_95 = lower_95)

fitted <- values_original_fitted
future <- values_future
original <- values_x
future_upper_95 <- upper_95
future_lower_95 <- lower_95

predicted <- rep(NA,82)
upper_95 <- rep(NA, 82)
lower_95 <- rep(NA, 82)

#Create Data frame to return to Spotfire

for (i in future) predicted <- c(predicted, i)
for (i in future_upper_95) upper_95 <- c(upper_95, i)
for (i in future_lower_95) lower_95 <- c(lower_95, i)

for (i in 1:14) original <- c(original, NA)
for (i in 1:14) fitted <- c(fitted,NA)


predicted_values <- data.frame( original, fitted, Actual, predicted, upper_95, lower_95)

write.csv(predicted_values,"predicted_values.csv",row.names = FALSE)
