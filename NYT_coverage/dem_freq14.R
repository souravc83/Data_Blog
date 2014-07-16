rm(list=ls())


dems=read.table('dem_freq14.txt',header=FALSE,col.names=c("name","num_stories"))
png('dems14.png')
barplot(dems$num_stories,
        legend=dems$name,
        names.arg=c(1:10),
        xlab="Candidate",
        ylab="Number of News Stories",
        col=rainbow(10))
dev.off() 
