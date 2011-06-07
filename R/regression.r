library(ggplot2)
mydata = read.csv("/home/joshua/Downloads/test_data.csv", header = TRUE)

m = length(mydata$x)
theta = matrix(c(0,0), nrow=1)
ux = matrix(c(rep(1,m), mydata$x), ncol=2)
uy= matrix(mydata$y, ncol=1)
delta = function(x,y,th) {
	delta = (t(x) %*% ((x %*% t(th)) - y))
	return(t(delta))
}

for (i in 0:m) {
	j = (m - i)
	if (uy[(j)] > uy[(j-1)]) {
		oy=matrix(uy[j:m], ncol=1)
		ox=matrix(c(rep(1,(i+1)), ux[j:m,2]), ncol=2)
		oy_x=matrix(c(rep(1,(i+1)), uy[j:m]), ncol=2)
		ox_y=matrix(ux[j:m,2], ncol=1)
		break
	}
}

data = data.frame(ox, oy)
data_backwards = data.frame(oy_x, ox_y)

theta_normal = solve(t(ox) %*% ox) %*% (t(ox) %*% oy)
theta_backwards = solve(t(oy_x) %*% oy_x) %*% (t(oy_x) %*% ox_y)

polyfit <- lm(oy~cbind(X2, (X2)^2), data)
polyfit_backwards <- lm(ox_y~cbind(X2, (X2)^2), data_backwards)

coef2 <- coef(polyfit)
coef2_backwards <- coef(polyfit_backwards)

y3 <- cbind(1,data$X2,data$X2^2) %*% coef2
y3_backwards <- cbind(1,data_backwards$X2,data_backwards$X2^2) %*% coef2_backwards

line = data.frame(ox, oy, y3)

dataplot = ggplot(line, aes(X2, oy)) + geom_point() + ylab('Quantity') + xlab('Days')

dataplot + geom_abline(intercept=theta_normal[1], slope=theta_normal[2]) + geom_line(aes(X2, y3))

