library(RinR)

ActualPathToOpenSourceR <- "C:\\Program Files\\R\\R-3.6.1\\bin\\R.exe"

options( RinR_R_FULL_PATH = ActualPathToOpenSourceR )

passengers <- passengers_by_month$passengers

forecast <- RinR::REvaluate(
	data = list(passengers = passengers),
	expr = 
	{
		library(forecast)
			
		# convert data to time series so seasonality (12) can be specified
		ts_passengers = ts(passengers, frequency = 12)
			
		fit <- auto.arima(ts_passengers)

		passenger_forecast <- forecast(fit, 36)
		
		passenger_fitted <- passenger_forecast$mean
		passenger_original_fitted <- passenger_forecast$fitted
		passenger_x <- passenger_forecast$x
		upper_95 <- passenger_forecast$upper[,1]
		lower_95 <- passenger_forecast$lower[,1]

		# return objects
		list(passenger_fitted = passenger_fitted,
				passenger_original_fitted = passenger_original_fitted,
				passenger_x = passenger_x,
				upper_95 = upper_95,
				lower_95 = lower_95)
	}
)

fitted <- forecast[["passenger_original_fitted"]]
future <- forecast[["passenger_fitted"]]
original <- forecast[["passenger_x"]]
future_upper_95 <- forecast[["upper_95"]]
future_lower_95 <- forecast[["lower_95"]]

predicted <- rep(NA, 144)
upper_95 <- rep(NA, 144)
lower_95 <- rep(NA, 144)
new_dates <- passengers_by_month$Month

if (run_forecast) 
{

new_dates <- c(new_dates, 
"2020-01", "2020-02", "2020-03", "2020-04", "2020-05", "2020-06",
"2020-07", "2020-08", "2020-09", "2020-10", "2020-11", "2020-12",
"2021-01", "2021-02", "2021-03", "2021-04", "2021-05", "2021-06",
"2021-07", "2021-08", "2021-09", "2021-10", "2021-11", "2021-12",
"2022-01", "2022-02", "2022-03", "2022-04", "2022-05", "2022-06",
"2022-07", "2022-08", "2022-09", "2022-10", "2022-11", "2022-12")

for (i in future) predicted <- c(predicted, i)
for (i in future_upper_95) upper_95 <- c(upper_95, i)
for (i in future_lower_95) lower_95 <- c(lower_95, i)

for (i in 1:36) original <- c(original, NA)
for (i in 1:36) fitted <- c(fitted, NA)
} else {
	fitted <- rep(NA, 144)
}

# convert dates to the R data type that Spotfire will see as datetime
dates_typed <- as.POSIXct(new_dates, format="%Y-%m")

predicted_values <- data.frame(dates_typed, predicted, original, upper_95, lower_95, fitted)