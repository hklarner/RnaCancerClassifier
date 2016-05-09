library(lattice)

#read and print data
data <- read.csv(file="benchmark1_results.csv", sep=" ")
no_na_data <- na.omit(data)
print(no_na_data)

rows <- data[1]
cols <- data[2]
healthy <- data[3]
time_first <- data[4]
time_all <- data[5]
solutions <- data[6]

print(max(cols))

#start plot axes in (0,0)
par(xaxs="i", yaxs="i") 
par(mgp=c(3,1,0))

#rows - columns - time_first
wireframe(time_first ~ cols * rows, data=no_na_data, main = "Generating first model", drape = TRUE, perspective=TRUE, colorkey=FALSE, xlab=list("number of columns", rot=35), ylab=list("number of rows", rot=-40), zlab="time (s)", xlim=c(min(cols),max(cols)), ylim=c(min(rows),max(rows)), zlim=c(min(time_first),max(time_first)), scales = list(arrows=FALSE,font = 0.3,tck = c(0.5, 0.5, 0.5),distance =c(2, 2, 2)),zoom = 0.6, cex.lab=0.05)


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
plot(time_all ~ solutions, data = no_na_data, main = "Generating all models", type="l", col="blue", xlab="number of solutions", ylab="time (s)", xlim=c(min(solutions),max(solutions)), ylim=c(min(time_all),max(time_all)), xaxp  = c(0,round(max(solutions), digits=-2), 20), yaxp  = c(0,round(max(time_all), digits=-2), 20), lwd=1.5)


