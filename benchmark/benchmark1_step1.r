

# generates random binary matrices in files matrix_<rows>_<columns>_<prob>.csv

rows_max  = 12
cols_max  = 12
prob_max  = 30
prob_step = 10

if (1) {
for (rows in seq(10,rows_max)) {
   for (cols in seq(10,cols_max)) {
      for (prob_healthy in seq(10,prob_max,prob_step)) {
         
         
         a = formatC(rows, width=3, flag="0")
         b = formatC(cols, width=3, flag="0")
         c = formatC(prob_healthy, width=3, flag="0")
         
         
         fname = paste("csvs/matrix",a,b,c,sep="_")
         fname = paste(fname,".csv",sep="")
         
         prob = prob_healthy*0.01

         vector_index    = matrix(seq(1:rows),rows,1)
         vector_annots   = matrix(rbinom(rows,1,prob),rows,1)
         matrix_profiles = matrix(sample(0:1,rows*cols, replace=TRUE),rows,cols)
         matrix_complete = cbind(vector_index, vector_annots, matrix_profiles)

         miRNAs = sprintf("g%d",seq(1:cols))
         colnames = c("ID", "Annots", miRNAs)
         colnames(matrix_complete) = colnames

         write.table(matrix_complete, fname, sep=", ", row.names=FALSE, quote=FALSE)
         
      
      }
   }
}

n = length(seq(10,rows_max))*length(seq(10,cols_max))*length(seq(10,prob_max,prob_step))
sprintf("created %d files in ./csvs",n )
}













