cat("\014") 
options(max.print=1000000)
t1 <- Sys.time()
library(ggplot2)


THE_FILE   <- "/Users/akond.rahman/Documents/Personal/misc/solidity_output/FINAL_MONTH_WISE_COUNT.csv"
THE_LIMIT  <- 12

LINE_DATA  <- read.csv(THE_FILE)
overall_plot <- ggplot(data=LINE_DATA, aes(x=MONTH, y=COUNT, group=1)) + 
  geom_point(size=0.5)  + scale_x_discrete(breaks = LINE_DATA$MONTH[seq(1, length(LINE_DATA$MONTH), by = THE_LIMIT)]) +
  geom_smooth(size=1.0, method='loess') + ggtitle("Count of Solidity Files in GitHub Over Time") +   
  labs(x='Month', y='Count') + 
  theme(text = element_text(size=20), axis.text.x = element_text(angle=45, hjust=1), plot.title = element_text(hjust = 0.5)) +
  ylim(c(0, 105)) 

overall_plot
t2 <- Sys.time()
print(t2 - t1)  
rm(list = setdiff(ls(), lsf.str()))