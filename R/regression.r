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
		break
	}
}

theta.normal = solve(t(ox) %*% ox) %*% (t(ox) %*% oy)

polyfit <- lm(oy~cbind(X2, (X2)^2), data)
coef2 <- coef(polyfit)
y3 <- cbind(1,data$X2,data$X2^2) %*% coef2

line = data.frame(ox, oy, y3)

dataplot = ggplot(line, aes(X2, oy)) + geom_point() + ylab('Quantity') + xlab('Days')

dataplot + geom_abline(intercept=theta.normal[1], slope=theta.normal[2]) + geom_line(line, aes(X2, y3))

