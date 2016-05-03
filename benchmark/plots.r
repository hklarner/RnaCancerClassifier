library(lattice)

data <- read.csv(file="benchmark1_results.csv", sep=" ")
print(data)

rows <- data[1]
cols <- data[2]
time_first <- data[4]

print(rows)
print(cols)
print(time_first)

wireframe(time_first ~ cols * rows, data=data)

p <- wireframe(time_first ~ cols * rows, data=data)
npanel <- c(4, 2)
rotx <- c(-50, -80)
rotz <- seq(30, 300, length = npanel[1]+1)
update(p[rep(1, prod(npanel))], layout = npanel,
    panel = function(..., screen) {
        panel.wireframe(..., screen = list(z = rotz[current.column()],
                                           x = rotx[current.row()]))
    })
