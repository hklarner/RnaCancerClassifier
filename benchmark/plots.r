library(lattice)

#read and print data
data <- read.csv(file="benchmark1_results.csv", sep=" ")
print(data)

rows <- data[1]
cols <- data[2]
healthy <- data[3]
time_first <- data[4]
time_all <- data[5]
solutions <- data[6]

#start plot axes in (0,0)
par(xaxs="i", yaxs="i") 
par(mgp=c(3,1,0))

#rows - columns - time_first
wireframe(time_first ~ cols * rows, data=data, main = "Generating first model", drape = TRUE, perspective=TRUE, colorkey=FALSE, xlab=list("number of columns", rot=35), ylab=list("number of rows", rot=-40), zlab="time (s)", xlim=c(0,max(cols)), ylim=c(0,max(rows)), zlim=c(0,max(time_first)), xaxp  = c(0, max(cols), 100), scales = list(arrows=FALSE,font = 0.3,tck = c(0.8, 0.6, 0.4),distance =c(2, 2, 2)),zoom = 0.6, cex.lab=0.05)

#rows - columns - time_first (different angles)
p <- wireframe(time_first ~ cols * rows, data=data, drape = TRUE, colorkey=FALSE, xlab="c", ylab="r", zlab="t",cex.lab=0.05, lab=3)
npanel <- c(4, 2)
rotx <- c(-50, -80)
rotz <- seq(30, 300, length = npanel[1]+1)
update(p[rep(1, prod(npanel))], layout = npanel,
    panel = function(..., screen) {
        panel.wireframe(..., screen = list(z = rotz[current.column()],
                                           x = rotx[current.row()]))})

#time for calculating all soltions - number of solutions
plot(time_all ~ solutions, data = data, main = "Generating all models", type="l", col="blue", xlab="number of solutions", ylab="time (s)", xlim=c(0,max(solutions)), ylim=c(0,max(time_all)), xaxp  = c(0, 100000, 20), yaxp  = c(0, 30000, 20), lwd=1.5)


