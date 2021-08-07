                ##Program: DATA4400_SimpleVar
                ##Author: SN
                ##Date: May 2021

# Demonstration of VAR model on artificially created bivariate timeseries.
#Includes stationarity tests, Granger causality test and final forecast.
                

set.seed(123) # Reset random number generator for reasons of reproducability

library(aTSA)
library(dplyr)

# Generate sample
t <- 200 # Number of time series observations
k <- 2 # Number of endogenous variables
p <- 2 # Number of lags

# Generate coefficient matrices
A.1 <- matrix(c(-.3, .6, -.4, .5), k) # Coefficient matrix of lag 1
A.2 <- matrix(c(-.1, -.2, .1, .05), k) # Coefficient matrix of lag 2
A <- cbind(A.1, A.2) # Companion form of the coefficient matrices

# Generate series
series <- matrix(0, k, t + 2*p) # Raw series with zeros
for (i in (p + 1):(t + 2*p)){ # Generate series with e ~ N(0,0.5)
  series[, i] <- A.1%*%series[, i-1] + A.2%*%series[, i-2] + rnorm(k, 0, .5)
}

series <- ts(t(series[, -(1:p)])) # Convert to time series format
names <- c("V1", "V2") # Rename variables



#Stationarity Test - Augmented Dickey Fuller

adf.test(series[,1])
adf.test(series[,2])

# Stationarity Test - Phillips-Perron

pp.test(series[,1])
adf.test(series[,2])

plot.ts(series) # Plot the series

library(vars) # Load package

var.1 <- VAR(series, 2, type = "none") # Estimate the model

var.aic <- VAR(series, type = "none", lag.max = 5, ic = "AIC")
summary(var.aic)

# True values in console
A

# Extract coefficients, standard errors etc. from the object
# produced by the VAR function
est_coefs <- coef(var.aic)

# Extract only the coefficients for both dependent variables

# and combine them to a single matrix
est_coefs <- rbind(est_coefs[[1]][, 1], est_coefs[[2]][, 1]) 

# Print the rounded estimates in the console
round(est_coefs, 2)


#Granger Causality

var.cause.Series1 <- causality(var.aic, cause = "Series.1")
var.cause.Series1

var.cause.Series2 <- causality(var.aic, cause = "Series.2")
var.cause.Series2

# Calculate the IRF
ir.1 <- irf(var.1, impulse = "Series.1", response = "Series.2", n.ahead = 20, ortho = FALSE)

# Plot the IRF
plot(ir.1)


# Calculate impulse response
ir.2 <- irf(var.1,impulse="Series.1",response="Series.2",n.ahead = 20,ortho = FALSE,
            cumulative = TRUE)
# Plot
plot(ir.2)


#To generate the forecast error variance decompositions we make use of 
#the fevd command, where we set the number of steps ahead to ten.

bv.vardec <-fevd(var.aic,n.ahead=10)
plot(bv.vardec)

#Series 1 is determined by Series 1 shocks but Series 2 is determined by both.

predictions <- predict(var.aic, n.ahead = 8, ci = 0.95)
plot(predictions, names = "Series.1")
plot(predictions, names = "Series.2")

fanchart(predictions, names = "Series.1")
fanchart(predictions, names = "Series.2")