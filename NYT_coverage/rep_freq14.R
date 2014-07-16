rm(list=ls())


repub=read.table('rep_freq14.txt',header=FALSE,col.names=c("name","num_stories"))
png('reps14top10.png')
barplot(repub$num_stories[1:10],
legend=repub$name[1:10],
        names.arg=c(1:10),
        xlab="Candidate",
        ylab="Number of News Stories",
        col=rainbow(10))
dev.off()

png('reps14_1120.png')

barplot(repub$num_stories[11:20],
        legend=repub$name[11:20],
        names.arg=c(11:20),
        xlab="Candidate",
        ylab="Number of News Stories",
        col=rainbow(10))
dev.off()