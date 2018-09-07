	library(ipumsr)
	library(fitdistrplus)
	library(ggplot2)
	library(STAR)
	library(dplyr, warn.conflicts = FALSE)

	setwd("C:/Users/bills/Desktop/ML_Projects/population-simulator/data")

	df <- read.csv(file="cps_00005.csv", header=TRUE, sep=",")
	#Remove nan, d$INCTOT == 99999999, d$INCTOT == 99999998,

	df <- na.omit(df)
	df <- df[!(df$FTOTVAL ==  99999999 | df$FTOTVAL ==  99999998),]
	df <- df[!(df$INCTOT ==  99999999 | df$INCTOT == 99999998),]

	df <- df[order(df$FTOTVAL),]

	#We get the 5 classes. According to William Thompson & Joseph Hickey, 2005	we have

	lower_class = df[df$FTOTVAL <= 16000,]
	working_class = df[(df$FTOTVAL > 16000 & df$FTOTVAL <= 30000),]
	lower_middle_class = df[(df$FTOTVAL > 30000 & df$FTOTVAL <= 75000),]
	upper_middle_class = df[(df$FTOTVAL > 75000 & df$FTOTVAL <= 300000),]
	upper_class = df[(df$FTOTVAL > 300000),]

	print(fitdist(lower_class$INCTOT, distr = "unif", method = "mme"))
	print(fitdist(working_class$INCTOT, distr = "norm", method = "mme"))
	print(fitdist(lower_middle_class$INCTOT, distr = "norm", method = "mme"))
	plot(fitdist(upper_middle_class$INCTOT, distr = "norm", method = "mme"))
	print(fitdist(upper_class$INCTOT, distr = "gamma", method = "mme"))

	df_m = filter(df, SEX==1)
	df_f = filter(df, SEX == 2)

	transform(df, AGE = as.numeric(AGE))
	m <- ggplot(df_m, aes(x=(df_m$AGE), y=(df_m$INCTOT))) + geom_col(colour ="blue")  + xlab("Age")+ ylab("Income")+ ggtitle("Age to Income Ratio (Both Sexes)")
	m <- m  + geom_col(data = df_f, aes(x=(df_f$AGE), y=(df_f$INCTOT)), colour = "red")
