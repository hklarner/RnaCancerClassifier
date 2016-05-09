library(lattice)

#read and print data
data <- read.csv(file="benchmark1_results.csv", sep=" ")
no_na_data <- na.omit(data)
print(no_na_data)

rows <- no_na_data[1]
cols <- no_na_data[2]
healthy <- no_na_data[3]
time_first <- no_na_data[4]
time_all <- no_na_data[5]
solutions <- no_na_data[6]


#start plot axes in (0,0)
par(xaxs="i", yaxs="i") 
par(mgp=c(3,1,0))


#rows - columns - time_first
#3D plot for healthy=0.3
wireframe(time_first[healthy==0.3] ~ cols[healthy==0.3] * rows[healthy==0.3], data=no_na_data, main = "Generating first model (healthy==0.3)", drape = TRUE, perspective=TRUE, colorkey=FALSE, xlab=list("number of columns", rot=35), ylab=list("number of rows", rot=-40), zlab="time (s)", xlim=c(min(cols[healthy==0.3]),max(cols[healthy==0.3])), ylim=c(min(rows[healthy==0.3]),max(rows[healthy==0.3])), zlim=c(min(time_first[healthy==0.3]),max(time_first[healthy==0.3])), scales = list(arrows=FALSE,font = 0.3,tck = c(0.8, 0.8, 0.8),distance =c(1, 1, 1)),zoom = 0.8, cex.lab=0.05)


#3D plot for healthy=0.6
wireframe(time_first[healthy==0.6] ~ cols[healthy==0.6] * rows[healthy==0.6], data=no_na_data, main = "Generating first model (healthy==0.6)", drape = TRUE, perspective=TRUE, colorkey=FALSE, xlab=list("number of columns", rot=35), ylab=list("number of rows", rot=-40), zlab="time (s)", xlim=c(min(cols[healthy==0.6]),max(cols[healthy==0.6])), ylim=c(min(rows[healthy==0.6]),max(rows[healthy==0.6])), zlim=c(min(time_first[healthy==0.6]),max(time_first[healthy==0.6])), scales = list(arrows=FALSE,font = 0.3,tck = c(0.8, 0.8, 0.8),distance =c(1, 1, 1)),zoom = 0.8, cex.lab=0.05)


#3D plot for healthy=0.9
wireframe(time_first[healthy==0.9] ~ cols[healthy==0.9] * rows[healthy==0.9], data=no_na_data, main = "Generating first model (healthy==0.9)", drape = TRUE, perspective=TRUE, colorkey=FALSE, xlab=list("number of columns", rot=35), ylab=list("number of rows", rot=-40), zlab="time (s)", xlim=c(min(cols[healthy==0.9]),max(cols[healthy==0.9])), ylim=c(min(rows[healthy==0.9]),max(rows[healthy==0.9])), zlim=c(min(time_first[healthy==0.9]),max(time_first[healthy==0.9])), scales = list(arrows=FALSE,font = 0.3,tck = c(0.8, 0.8, 0.8),distance =c(1, 1, 1)),zoom = 0.8, cex.lab=0.05)


#rows - columns - time_first (different angles)
p <- wireframe(time_first ~ cols * rows, data=no_na_data, drape = TRUE, colorkey=FALSE, xlab="c", ylab="r", zlab="t",cex.lab=0.05, lab=3)
npanel <- c(4, 2)
rotx <- c(-50, -80)
rotz <- seq(30, 300, length = npanel[1]+1)
update(p[rep(1, prod(npanel))], layout = npanel,
    panel = function(..., screen) {
        panel.wireframe(..., screen = list(z = rotz[current.column()],
                                           x = rotx[current.row()]))})


#time for calculating all solutions - number of solutions
plot(time_all ~ solutions, data = no_na_data, main = "Generating all models", type="p", col="blue", xlab="number of solutions", ylab="time (s)", xlim=c(min(solutions),100000), ylim=c(min(time_all),20000), xaxp  = c(0,100000, 20), yaxp  = c(0,20000, 20), lwd=1.5)


#time for calculating first model - number of cols (number of rows fixed to 10)
plot(time_first[rows==10] ~ cols[rows==10], data = no_na_data, main = "Generating first model (number of rows = 10)", type="p", col="blue", xlab="number of columns", ylab="time (s)", xlim=c(min(cols[rows==10]),max(cols[rows==10])), ylim=c(min(time_first[rows==10]),max(time_first[rows==10])), xaxp  = c(0,max(cols), 20), yaxp  = c(0,round(max(time_all), digits=-2), 20), lwd=1.5)

#scatterplot - overview all variables
plot(no_na_data)


