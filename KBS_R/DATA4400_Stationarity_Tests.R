install.packages("readxl")
install.packages("aTSA")
install.packages("dplyr")

library(readxl)
library(aTSA)
library(dplyr)

# You will need to change the location of the source file
data <- read_xlsx("C:\\Users\\Public\\Documents\\Datasets\\DATA 4400\\Telstra.xlsx")

# Clean the data to only include dates and closing price
cleandata = subset(data, select = -c(ASX.Code,Open, High, Low, Volume) )

# Create the lprice variable
lprice = log(cleandata$Close, 10)

# Stationarity Test - Augmented Dickey Fuller
adf.test(lprice)

# Stationarity Test - Phillips-Perron
pp.test(lprice)

# Plot time series graph of lprice
ts.plot(lprice)

# Conduct first-order difference of lprice
lprice_d1 <- diff(lprice, differences = 1)

# Plot the time series graph of lprice_d1
ts.plot(lprice_d1)

# Conduct the ADF test on the first differenced variable
adf.test(lprice_d1)

# Conduct PP test on the first differenced variable
PP.test(lprice_d1)