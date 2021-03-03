# ----------------------------
# Hacer graficos para el reporte del GCBM (Crecimeinto)
# Contacto: juliancabezas@gmail.com
# ----------------------------
gc()

#------------------------------------------------------
# Manejo de la libreria

# Usamos "checkpoint" para asegurar reproducibilidad
# install.packages("checkpoint")
# library("checkpoint")
# checkpoint("2020-02-28") #Aqui indicamos la fecha de entrega del codigo

# Instalar paquetes necesarios si no estan instalados
if (!require(writexl)) install.packages("writexl")
if (!require(readr)) install.packages("readr")
if (!require(dplyr)) install.packages("dplyr")
if (!require(tidyr)) install.packages("tidyr")




results_db_path <- "./Results"
results_file <- "Results_index_filter30_v2.csv"

pushs <- read_csv(file.path(results_db_path,results_file))

pushs

# Table with the results


pushs$slope_group <- ifelse(is.na(pushs$slope),"No Change",
                            ifelse(pushs$p_value <= 0.05, 
                                   ifelse(pushs$slope > 0, "Significant Positive","Significant Negative"),"Not Significant"))



push_file <- "./Processed/push_total_filter30.csv"

pushs_full <- read_csv(push_file)

pushs_full

push_year_user <- pushs_full %>% group_by(user,year) %>% summarize(mean_index = mean(r_py_index))

push_year_user


push_year_user <- left_join(push_year_user,pushs[c('user','slope_group')],by = c('user'))


push_year_user <- ungroup(push_year_user)


# using 5 cathgories
push_year_user$mean_group_5cat <- cut(push_year_user$mean_index, 
                                      breaks=c(-Inf,0, 0.333333333333333, 0.666666666666666,0.99999999999, Inf), 
                                      labels=c("Exclusive Python","Mostly Python","Mixed","Mostly R","Exclusive R"))



push_year_user

push_year_user <- left_join(push_year_user,pushs[c('user','slope_group')],by = c('user'))

push_year_user




write_xlsx(push_year_user, "./Results/Pushs_class_slope.xlsx")













push_year_user$mean_group_3cat <- cut(push_year_user$mean_index, 
                                      breaks=c(-Inf,0,0.99999999999, Inf), 
                                      labels=c("Exclusive Python","Mixed","Exclusive R"))

push_year_user


push_spread <- select(push_year_user,user,year, mean_group_3cat) %>% spread(year, mean_group_3cat)

push_spread_comb <- push_spread %>%  group_by(`2015`,`2016`,`2017`,`2018`,`2019`) %>% 
  summarize(freq = n())

push_spread_comb$subject <- 1:nrow(push_spread_comb)
push_spread_comb

push_subjects <- gather(push_spread_comb, "year","class", 1:5)


push_subjects$class <- factor(push_subjects$class,levels= c("Exclusive Python","Mixed","Exclusive R",NA))

ggplot(push_subjects[complete.cases(push_subjects), ],
       aes(x = as.factor(year), stratum = class, alluvium = subject,
           y = freq,
           fill = class, label = class)) +
  scale_x_discrete(expand = c(.1, .1)) +
  geom_flow() +
  geom_stratum(alpha = .5) +
  geom_text(stat = "stratum", size = 3,min.y = 1000000000) +
  scale_fill_viridis_d(name = "User R-Python Ratio class",
                       labels = c("Exclusive Python User","Mixed R and Python User","Exclusive R User"),begin = 1,end = 0) +
  theme(legend.position = "none") +
  ylab("Number of users") +
  xlab("Year") +
  ggtitle("Transitions of users between classes (2015-2019)")+
  theme_bw(10)


ggsave("./Graphs/Transitions_full_3class_v1.tiff",dpi = 250,height = 10,width = 15,units= "cm")





# Now the same with 5 cathegories

push_spread <- select(push_year_user,user,year, mean_group_5cat) %>% spread(year, mean_group_5cat)

push_spread_comb <- push_spread %>%  group_by(`2015`,`2016`,`2017`,`2018`,`2019`) %>% 
  summarize(freq = n())

push_spread_comb <- filter(push_spread_comb,!(`2015`== "Exclusive Python" & `2016`== "Exclusive Python" & `2017`== "Exclusive Python" & `2018`== "Exclusive Python" & `2019`== "Exclusive Python"))
push_spread_comb <- filter(push_spread_comb,!(`2015`== "Exclusive R" & `2016`== "Exclusive R" & `2017`== "Exclusive R" & `2018`== "Exclusive R" & `2019`== "Exclusive R"))
push_spread_comb


push_spread_comb$subject <- 1:nrow(push_spread_comb)
push_spread_comb

push_subjects <- gather(push_spread_comb, "year","class", 1:5)

push_subjects$class

push_subjects$class <- factor(push_subjects$class,levels= c("Exclusive Python","Mostly Python","Mixed","Mostly R","Exclusive R",NA))

push_subjects

ggplot(push_subjects[complete.cases(push_subjects), ],
       aes(x = as.factor(year), stratum = class, alluvium = subject,
           y = freq,
           fill = class, label = class)) +
  scale_x_discrete(expand = c(.1, .1)) +
  geom_flow() +
  geom_stratum(alpha = .5) +
  geom_text(stat = "stratum", size = 2,min.y = 1000000000) +
  #geom_text(stat = "stratum", size = 3) +
  scale_fill_viridis_d(name = "User R-Python Ratio class",
                       labels = c("Exclusive Python User","Mostly Python User","Mixed R and Python User","Mostly R User","Exclusive R User"),begin = 1,end = 0) +
  theme(legend.position = "none") +
  ylab("Number of users") +
  xlab("Year") +
  ggtitle("Transitions of users between classes (2015-2019)")+
  theme_bw(10)

ggsave("./Graphs/Transitions_filtered_5class_v1.tiff",dpi = 250,height = 10,width = 15,units= "cm")





# Scatterplot

pushs_full

pushs_full <- left_join(pushs_full,pushs[c('user','slope_group','slope')],by = c('user'))

pushs_full$slope

scatter <- ggplot(pushs_full, aes(x=time, y=r_py_index, color=slope_group)) +
  geom_point() +
  xlab("Number of months since January 2015") +
  ylab("R-Python Ratio Index") +
  scale_color_manual(name = "Slope (Trend)",labels = c("No change","Not significant trend","Trend towards Python","Trend towards R"),values = c("forestgreen", "gray", "gold","dodgerblue3")) +
  theme_bw(10)


ggsave("./Graphs/Scatter_R_Python_Index_v1.tiff",scatter,dpi = 200,height = 8,width = 15,units= "cm")
pushs_full

scatter <- ggplot(pushs_full[!(pushs_full$slope_group %in% c("No Change", "Not Significant")),], aes(x=time, y=r_py_index, color=slope_group,size = slope)) +
  geom_point() +
  xlab("Number of months since January 2015") +
  ylab("R-Python Ratio Index") +
  scale_color_manual(name = "Slope (Trend)",labels = c("Trend towards Python","Trend towards R"),values = c("gold","dodgerblue3")) +
  theme_bw(10)

ggsave("./Graphs/Scatter_R_Python_Index_filterChange_v1.tiff",scatter,dpi = 200,height = 8,width = 15,units= "cm")

max(pushs_full$slope,na.rm = TRUE)
min(pushs_full$slope,na.rm = TRUE)
pushs_full

#model <- lm(push_full$r

# trend to Python

scatter <- ggplot(pushs_full[!(pushs_full$slope_group %in% c("No Change", "Not Significant", "Significant Positive")),], aes(x=time, y=r_py_index, color=slope_group)) +
  geom_point(alpha = 0.3,colour="black",size =1) + 
  geom_line(aes(group= user,colour =slope), stat="smooth",method = "lm",alpha = 0.8) +
  #stat_smooth(aes(color= user),geom='line', alpha=0.5, se=FALSE,show.legend = FALSE)
  #geom_smooth(aes(fill= user),method=lm, se=FALSE,show.legend = FALSE,color = "dodgerblue3",alpha = 0.2, lwd = 1) +
  xlab("Number of months since January 2015") +
  ylab("R-Python Ratio Index") +
  ylim(c(0,1)) +
  scale_colour_viridis_c(name = "Slope (Trend)", direction = 1, limits = c(-0.045, 0)) +
  #scale_color_manual(values = c("black","dodgerblue3")) +
  theme_bw(10) 


scatter

ggsave("./Graphs/Scatter_SlopesToPythone_v1.tiff",scatter,dpi = 250,height = 8,width = 15,units= "cm")



# trend to R

scatter <- ggplot(pushs_full[!(pushs_full$slope_group %in% c("No Change", "Not Significant", "Significant Negative")),], aes(x=time, y=r_py_index, color=slope_group)) +
  geom_point(alpha = 0.3,colour="black",size =1) + 
  geom_line(aes(group= user,colour =slope), stat="smooth",method = "lm",alpha = 0.8) +
  #stat_smooth(aes(color= user),geom='line', alpha=0.5, se=FALSE,show.legend = FALSE)
  #geom_smooth(aes(fill= user),method=lm, se=FALSE,show.legend = FALSE,color = "dodgerblue3",alpha = 0.2, lwd = 1) +
  xlab("Number of months since January 2015") +
  ylab("R-Python Ratio Index") +
  ylim(c(0,1)) +
  scale_colour_viridis_c(name = "Slope (Trend)", direction = -1, limits = c(0,0.045)) +
  #scale_color_manual(values = c("black","dodgerblue3")) +
  theme_bw(10) 

scatter


ggsave("./Graphs/Scatter_SlopesToR_v1.tiff",scatter,dpi = 250,height = 8,width = 15,units= "cm")


# Histogram


pushs_full_gather <- gather(pushs_full[c("r_actions","py_actions")], "actions","number")

pushs_full_gather

pushs_full


p<-ggplot(pushs_full_gather, aes(x=number, fill=actions)) +
  geom_histogram(position="identity", alpha=0.55,color = "black",bins = 50) +
  xlim(0,500) +
  ylim(0,150000) +
  ylab("Frequency") +
  xlab("Monthly push actions") +
  scale_fill_manual(name="Language of  \nthe repository",values = c("gold","dodgerblue3"),labels = c("Python","R")) +
  theme_bw(10)

p

ggsave("./Graphs/Histogram_Push_Language.tiff",p,dpi = 250,height = 8,width = 15,units= "cm")

options(scipen=999)

p<-ggplot(pushs_full, aes(x=r_py_index)) +
  geom_histogram(position="identity", alpha=0.75,color = "black",bins = 20,fill = "dodgerblue3") +
  geom_rug(alpha = 0.05, sides = "t") +
  ylim(0,550000) +
  ylab("Frequency") +
  xlab("R-Python Ratio Index") +
  #scale_fill_manual(name="Language of  \nthe repository",values = c("gold","dodgerblue3"),labels = c("Python","R")) +
  theme_bw(10)

ggsave("./Graphs/Histogram_R_Py_Index.tiff",p,dpi = 250,height = 10,width = 15,units= "cm")




























scatter <- ggplot(pushs_full[!(pushs_full$slope_group %in% c("No Change", "Not Significant", "Significant Positive")),], aes(x=time, y=r_py_index, color=slope_group)) +
  geom_point(alpha = 0.3) +
  xlab("Number of months since January 2015") +
  ylab("R-Python Ratio Index") +
  scale_color_manual(name = "Slope (Trend)",labels = c("Trend towards Python","Trend towards R"),values = c("black","dodgerblue3")) +
  theme_bw()


scatter

pushs_full[!(pushs_full$slope_group %in% c("No Change", "Not Significant", "Significant Positive")),]


))))))))))))))))))))))))))


ggsave("./Graphs/Scatter_R_Python_Index_filterChange_v1.tiff",scatter,dpi = 200,height = 8,width = 15,units= "cm")

for (i in 1:n)

























ggplot(filter(push_subjects),
       aes(x = as.factor(year), stratum = class, alluvium = subject,
           y = freq,
           fill = class, label = class)) +
  scale_x_discrete(expand = c(.1, .1)) +
  geom_flow() +
  geom_stratum(alpha = .5) +
  geom_text(stat = "stratum", size = 3) +
  scale_fill_manual(name = "User R-Python Ratio class",labels = c("Exclusive Python User","Mixed R and Python User","Exclusive R User"),values = c("#edf8b1", "#7fcdbb", "#2c7fb8")) +
  theme(legend.position = "none") +
  ggtitle("Transitions of users between classes (2015-2019)")+
  theme_bw()















push_year_user$class_slope <- paste0(push_year_user$mean_group_3cat,"-",push_year_user$slope_group)


push_spread <- select(push_year_user,user, year, class_slope) %>% spread(year, class_slope)

push_spread_comb <- push_spread %>%  group_by(`2015`,`2016`,`2017`,`2018`,`2019`) %>% 
  summarize(freq = n())

push_spread_comb$subject <- 1:193
push_spread_comb

push_subjects <- gather(push_spread_comb, "year","class", 1:5)

push_subjects <- separate(push_subjects,col = class,into = c("class","slope"),sep = "-")

push_subjects

ggplot(filter(push_subjects,!is.na(freq)),
       aes(x = as.factor(year), stratum = class, alluvium = subject,
           y = freq,
           fill = slope, label = class)) +
  scale_x_discrete(expand = c(.1, .1)) +
  geom_flow() +
  geom_stratum(alpha = .5) +
  geom_text(stat = "stratum", size = 3) +
  theme(legend.position = "none") +
  ggtitle("Transitions of users between classes (2015-2019)")+
  theme_bw()




ggplot(as.data.frame(push_subjects),
        aes(y = freq, x = year,stratum = class,alluvium = subject)) +
        #geom_alluvium(aes(fill = as.factor(slope_group)), width = 1/12) +
        geom_alluvium(width = 1/12) +
        geom_stratum(width = 0.25, color = "black",fill = "gray") +
        geom_label(stat = "stratum", infer.label = TRUE) +
        scale_x_discrete(limits = c("2015-2017", "2018-2019"), expand = c(.05, .05)) +
        scale_fill_manual(name = "Slope (Trend)",labels = c("No change","Not significant trend","Trend towards Python","Trend towards R"),values = c("forestgreen", "gold", "firebrick2","dodgerblue3")) +
        ylab("Number of users") +
        #ggtitle("Transition of users between R and Python between 2015-2017 and 2018-2019 ")+
        theme_bw(13)









pushs_summary_3cat <- push_year_user %>% group_by(mean_group_3cat,slope_group,year) %>% 
                  summarise(freq = n())


pushs_summary_3cat$subject <- 1:54




ggplot(as.data.frame(pushs_summary_3cat),
       aes(y = freq, x = year,stratum = mean_group_3cat,alluvium = subject)) +
         geom_alluvium(aes(fill = as.factor(slope_group)), width = 1/12) +
         geom_stratum(width = 0.25, color = "black",fill = "gray") +
         geom_label(stat = "stratum", infer.label = TRUE) +
         scale_x_discrete(limits = c("2015-2017", "2018-2019"), expand = c(.05, .05)) +
         scale_fill_manual(name = "Slope (Trend)",labels = c("No change","Not significant trend","Trend towards Python","Trend towards R"),values = c("forestgreen", "gold", "firebrick2","dodgerblue3")) +
         ylab("Number of users") +
         #ggtitle("Transition of users between R and Python between 2015-2017 and 2018-2019 ")+
         theme_bw(13)

data(vaccinations)

vaccinations




plot <- ggplot(as.data.frame(filter(push_year_user,slope_group %in% c("Significant Positive","Significant Negative","Not Significant"))),
               aes(x = year, stratum = mean_group_3cat, alluvium = user,
                   fill = mean_group_3cat, label = mean_group_3cat)) +
  scale_fill_brewer(type = "qual", palette = "Set2") +
  geom_flow(stat = "alluvium", lode.guidance = "frontback",
            color = "darkgray") +
  geom_stratum() +
  theme(legend.position = "bottom") +
  ggtitle("student curricula across several semesters")


plot










pushs$mean_group_2015_2017 <- cut(push_year_user$mean_2015_2017, 
                                  breaks=c(-Inf,0, 0.333333333333333, 0.666666666666666,0.99999999999, Inf), 
                                  labels=c("Exclusive Python","Mostly Python","Mixed","Mostly R","Exclusive R"))

pushs$mean_group_2018_2019 <- cut(pushs$mean_2018_2019, 
                                  breaks=c(-Inf,0, 0.333333333333333, 0.666666666666666,0.99999999999, Inf), 
                                  labels=c("Exclusive Python","Mostly Python","Mixed","Mostly R","Exclusive R"))














# using 5 cathgories
pushs$mean_group_total <- cut(pushs$mean, 
                              breaks=c(-Inf,0, 0.333333333333333, 0.666666666666666,0.99999999999, Inf), 
                              labels=c("Exclusive Python","Mostly Python","Mixed","Mostly R","Exclusive R"))

pushs$mean_group_2015_2017 <- cut(pushs$mean_2015_2017, 
                                  breaks=c(-Inf,0, 0.333333333333333, 0.666666666666666,0.99999999999, Inf), 
                                  labels=c("Exclusive Python","Mostly Python","Mixed","Mostly R","Exclusive R"))

pushs$mean_group_2018_2019 <- cut(pushs$mean_2018_2019, 
                                  breaks=c(-Inf,0, 0.333333333333333, 0.666666666666666,0.99999999999, Inf), 
                                  labels=c("Exclusive Python","Mostly Python","Mixed","Mostly R","Exclusive R"))


# Suing 3 cathegories
pushs$mean_group_total_3cat <- cut(pushs$mean, 
                                   breaks=c(-Inf,0,0.99999999999, Inf), 
                                   labels=c("Exclusive Python","Mixed","Exclusive R"))

pushs$mean_group_2015_2017_3cat <- cut(pushs$mean_2015_2017, 
                                       breaks=c(-Inf,0,0.99999999999, Inf), 
                                       labels=c("Exclusive Python","Mixed","Exclusive R"))

pushs$mean_group_2018_2019_3cat <- cut(pushs$mean_2018_2019, 
                                       breaks=c(-Inf,0,0.99999999999, Inf), 
                                       labels=c("Exclusive Python","Mixed","Exclusive R"))



pushs_summary_3cat <- pushs %>% group_by(mean_group_2015_2017_3cat,mean_group_2018_2019_3cat,slope_group) %>% 
  summarise(freq = n())


pushs_summary_5cat <- pushs %>% group_by(mean_group_2015_2017,mean_group_2018_2019,slope_group) %>% 
  summarise(freq = n())

as.data.frame(UCBAdmissions)

pushs_summary_3cat
get_alluvial_type(as.data.frame(pushs_summary_3cat))

pushs_summary_3cat
attr(pushs_summary_3cat, "spec") <- NULL
attr(pushs_summary_3cat, "groups") <- NULL
attr(pushs_summary_3cat, ".drop") <- NULL

is_alluvia_form(as.data.frame(pushs_summary_3cat)[,1:4], axes = 1:4, silent = FALSE)
pushs_summary_3cat

data(majors)
majors

ggplot(as.data.frame(pushs_summary_3cat),
       aes(y = freq, axis1 = mean_group_2015_2017_3cat, axis2 = mean_group_2018_2019_3cat)) +
  geom_alluvium(aes(fill = as.factor(slope_group)), width = 1/12) +
  geom_stratum(width = 0.25, color = "black",fill = "gray") +
  geom_label(stat = "stratum", infer.label = TRUE) +
  scale_x_discrete(limits = c("2015-2017", "2018-2019"), expand = c(.05, .05)) +
  scale_fill_manual(name = "Slope (Trend)",labels = c("No change","Not significant trend","Trend towards Python","Trend towards R"),values = c("forestgreen", "gold", "firebrick2","dodgerblue3")) +
  ylab("Number of users") +
  #ggtitle("Transition of users between R and Python between 2015-2017 and 2018-2019 ")+
  theme_bw(13)

ggplot(as.data.frame(filter(pushs_summary_3cat,slope_group %in% c("Significant Positive","Significant Negative","Not Significant"))),
       aes(y = freq, axis1 = mean_group_2015_2017_3cat, axis2 = mean_group_2018_2019_3cat)) +
  geom_alluvium(aes(fill = as.factor(slope_group)), width = 1/12) +
  geom_stratum(width = 0.25, color = "black",fill = "gray") +
  geom_label(stat = "stratum", infer.label = TRUE) +
  scale_x_discrete(limits = c("2015-2017", "2018-2019"), expand = c(.05, .05)) +
  scale_fill_manual(name = "Slope (Trend)",labels = c("Not significant trend","Trend towards Python","Trend towards R"),values = c("gold", "firebrick2","dodgerblue3")) +
  ylab("Number of users") +
  #ggtitle("Transition of users between R and Python between 2015-2017 and 2018-2019 ")+
  theme_bw(13)


ggplot(as.data.frame(filter(pushs_summary_5cat,slope_group %in% c("Significant Positive","Significant Negative","Not Significant"))),
       aes(y = freq, axis1 = mean_group_2015_2017, axis2 = mean_group_2018_2019)) +
  geom_alluvium(aes(fill = as.factor(slope_group)), width = 1/12) +
  geom_stratum(width = 0.25, color = "black",fill = "gray") +
  geom_label(stat = "stratum", infer.label = TRUE) +
  scale_x_discrete(limits = c("2015-2017", "2018-2019"), expand = c(.05, .05)) +
  scale_fill_manual(name = "Slope (Trend)",labels = c("Not significant trend","Trend towards Python","Trend towards R"),values = c("gold", "firebrick2","dodgerblue3")) +
  ylab("Number of users") +
  #ggtitle("Transition of users between R and Python between 2015-2017 and 2018-2019 ")+
  theme_bw(13)

filter(pushs_summary_3cat),slope_group %in% c("Significant Positive","Significant Negative","Not Significant")


filter(pushs_summary_3cat),slope_group %in% c("Significant Positive","Significant Negative","Not Significant")

trn_mtrx <-with(pushs,table(mean_group_2015_2017, mean_group_2018_2019))

transitionPlot(trn_mtrx, box_width = 0.35,min_lwd = 0)

transitionPlot(pushs[c("mean_group_2015_2017","mean_group_2018_2019")])

data(Refugees, package = "alluvial")



ggplot(as.data.frame(UCBAdmissions),
       aes(y = Freq, axis1 = Gender, axis2 = Dept)) +
  geom_alluvium(aes(fill = Admit), width = 1/12)


geom_stratum(width = 1/12, fill = "black", color = "grey") +
  geom_label(stat = "stratum", infer.label = TRUE) +
  scale_x_discrete(limits = c("Gender", "Dept"), expand = c(.05, .05)) +
  scale_fill_brewer(type = "qual", palette = "Set1") +
  ggtitle("UC Berkeley admissions and rejections, by sex and department")


as.data.frame(UCBAdmissions)

ggplot(as.data.frame(Titanic),
       aes(y = Freq,
           axis1 = Survived, axis2 = Sex, axis3 = Class)) +
  geom_alluvium(aes(fill = Class),
                width = 0, knot.pos = 0, reverse = FALSE) +
  guides(fill = FALSE) +
  geom_stratum(width = 1/8, reverse = FALSE) +
  geom_text(stat = "stratum", infer.label = TRUE, reverse = FALSE) +
  scale_x_continuous(breaks = 1:3, labels = c("Survived", "Sex", "Class")) +
  coord_flip() +
  ggtitle("Titanic survival by class and sex")

data(majors)
majors

?transitionPlot

?cut

pushs$mean_group_total <- ifelse(pushs$slope == "No Change",
                                 ifelse(mean == 1,"Exclusive R user","Exclusive Python user"), 
                                 ifelse(pushs$mean > 0.5, "Significant Positive","Significant Negative"),"Not significant"))
