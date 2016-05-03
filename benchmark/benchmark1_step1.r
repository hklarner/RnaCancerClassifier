

# this script requires the library "gdata"
# require(gdata)


if (0) {
for (rows in seq(10,20)) {
   for (cols in seq(10,20)) {
      for (healthy in seq(10,90,10)) {
         
         
         a = formatC(rows, width=3, flag="0")
         b = formatC(cols, width=3, flag="0")
         a = paste(a,"x",b,sep="")
         
         b = formatC(healthy, width=3, flag="0")
         b = paste("h",b,sep="")
         
         fname = paste("matrix",a,b,sep="_")
         fname = paste(fname,".csv",sep="")
         
         
         
      
      }
   }
}
}

rows = 3
cols = 5
fname = "csvs/junk.csv"
prob = 0.80


vector_index    = matrix(seq(1:rows),rows,1)
vector_annots   = matrix(c(0,1,rbinom(rows-2,1,prob)),rows,1)
matrix_profiles = matrix(sample(0:1,rows*cols, replace=TRUE),rows,cols)
matrix_complete = cbind(vector_index, vector_annots, matrix_profiles)



miRNAs = sprintf("g%d",seq(1:cols))
colnames = c("ID", "Annots", miRNAs)
colnames(matrix_complete) = colnames

write.table(matrix_complete, fname, sep=", ", row.names=FALSE, quote=FALSE)











