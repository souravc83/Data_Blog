#clear workspace
rm( list =ls() )
cat('\014') #clear screen

#load libraries
library(ggplot2)
library(grid)

#define functions
read_input = function(filename)
{
  huffpost = read.csv(filename, sep=',', header=T)
  return(huffpost)
}

construct_cand_df = function(huffpost, cand_name,
                             announce_date, init_frame = NA )
{
  if (!any(cand_name %in% names(huffpost)))
  {
    print("Candidate name column not found")
    return()
  }
  
  num_polls = 10
  #find 5 polls prior to announcement in which
  #the candidate was polled
  pre_int = huffpost[huffpost$End.Date<=as.Date(announce_date) & 
                       !is.na(huffpost[,cand_name]),
                     c("End.Date",cand_name)]
  #top 5
  if(nrow(pre_int)>num_polls)
  {
    pre_int = head(pre_int[order(pre_int$End.Date,decreasing=T),],n=num_polls)
  }
  pre_int$diff_days = as.double(pre_int$End.Date-as.Date(announce_date))
  final_frame = pre_int[,c("diff_days",cand_name)]
  
  #10 polls after announcement
  post_int = huffpost[huffpost$End.Date > as.Date(announce_date) &
                        !is.na(huffpost[,cand_name]),
                     c("End.Date",cand_name)]
  #top 10
  if(nrow(post_int)>num_polls)
  {
    post_int = head(post_int[order(post_int$End.Date,decreasing=F),],n=num_polls)
  }
  post_int$diff_days = as.double(post_int$End.Date-as.Date(announce_date))
  final_frame = rbind(final_frame, post_int[,c("diff_days",cand_name)])
  
  names(final_frame) = c("diff_days","poll_rating")
  final_frame$Candidate = cand_name
  final_frame$poll_rating = final_frame$poll_rating - final_frame$poll_rating[1]
  
  if ( !is.na(init_frame) )
  {
    final_frame = rbind(init_frame, final_frame)  
  }
  return(final_frame) 
}
#main script
filename = '2016-national-gop-primary.csv'
huffpost = read_input(filename)
huffpost$End.Date = as.Date(huffpost$End.Date)

my_plot = ggplot()

f_frame = NA
f_frame = construct_cand_df(huffpost, "Cruz", "2015-03-23",f_frame)
#f_frame = construct_cand_df(huffpost, "Bush", "2015-06-15",f_frame)
#f_frame = construct_cand_df(huffpost, "Trump", "2015-06-16",f_frame)
#f_frame = construct_cand_df(huffpost, "Fiorina","2015-05-04",f_frame)
f_frame = construct_cand_df(huffpost, "Huckabee","2015-05-05",f_frame)
f_frame = construct_cand_df(huffpost, "Rand.Paul","2015-04-07",f_frame)
f_frame  = construct_cand_df(huffpost, "Carson","2015-05-04",f_frame)

f_frame$Candidate = as.factor(f_frame$Candidate) 
my_plot = ggplot( f_frame, aes(diff_days, poll_rating, colour = Candidate) )
my_plot2 = my_plot + 
           stat_smooth(size = 1.75, alpha =0.1) + 
           geom_point(size = 3) 

#add labels
my_plot2 = my_plot2 +
           xlab("Days from Announcement") +
           ylab("Poll Rating Change") +
           ggtitle("Change in Polling after Announcing") +
           ylim(-15,15)



#add vlines
my_plot2 =my_plot2 +
           geom_vline(xintercept = 15, colour = "black") +
           geom_vline(xintercept = 0, colour = "blue") +
           annotate("text",x=-15, y=-10, label= "Announcement\nDate") +
           geom_segment(aes(x = -5, y = -10, xend = 0, yend = -10),color="black", 
                         arrow = arrow(length = unit(0.25, "cm"))) +
           annotate("text", x=27, y=-10, label="Two\nWeeks\nfrom\nAnnouncing") +
           geom_segment(aes(x = 20, y = -10, xend = 15, yend = -10),color="black", 
                        arrow = arrow(length = unit(0.25, "cm")))
#change font
my_plot2 = my_plot2+
           theme(text = element_text(size=20))
  
print(my_plot2)


