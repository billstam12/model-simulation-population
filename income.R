	library(ipumsr)
	library(fitdistrplus)
	library(ggplot2)
	library(STAR)
	library(dplyr, warn.conflicts = FALSE)

	setwd("/Users/macmini/Desktop/cryptopals/model-simulation-population/data")

	df <- read.csv(file="cps_00005.csv", header=TRUE, sep=",")
	#Remove nan, d$INCTOT == 99999999, d$INCTOT == 99999998,

	df <- na.omit(df)
	df <- df[!(df$FTOTVAL ==  99999999 | df$FTOTVAL ==  99999998),]
	df <- df[!(df$INCTOT ==  99999999 | df$INCTOT == 99999998),]

	df <- df[order(df$FTOTVAL),]

	#We get the 5 classes. According to William Thompson & Joseph Hickey, 2005	we have
	lc = (floor(.2*nrow(df)))
	wc = (floor(.52*nrow(df)))
	lmc = (floor(.84*nrow(df)))
	umc = (floor(.99*nrow(df)))
	uc = (floor(.01*nrow(df)))

	lower_class = df[1:lc,]
	working_class = df[(lc+1):wc,]
	lower_middle_class = df[(wc+1):lmc,]
	upper_middle_class = df[(lmc+1):umc,]
	upper_class = df[(umc+1):nrow(df),]

	#print(nrow(lower_class)/nrow(df)*100)  -> 20%
	#print(nrow(working_class)/nrow(df)*100) -> 32%
	#print(nrow(lower_middle_class)/nrow(df)*100) -> 32%
	#print(nrow(upper_middle_class)/nrow(df)*100) -> 15%
	#print(nrow(upper_class)/nrow(df)*100) -> 1%

	print(fitdist(lower_class$INCTOT, distr = "unif", method = "mme"))
	print(fitdist(working_class$INCTOT, distr = "norm", method = "mme"))
	print(fitdist(lower_middle_class$INCTOT, distr = "norm", method = "mme"))
	print(fitdist(upper_middle_class$INCTOT, distr = "norm", method = "mme"))
	plot(fitdist(upper_class$INCTOT, distr = "gamma", method = "mme"))

	#df_m = filter(df, SEX==1)
	#df_f = filter(df, SEX == 2)

	#transform(df, AGE = as.numeric(AGE))
	#m <- ggplot(df_m, aes(x=(df_m$AGE), y=(df_m$INCTOT))) + geom_col(colour ="blue")  + xlab("Age")+ ylab("Income")+ ggtitle("Age to Income Ratio (Both Sexes)")
	#m <- m  + geom_col(data = df_f, aes(x=(df_f$AGE), y=(df_f$INCTOT)), colour = "red")
	