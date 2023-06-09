# -----------------------------------------------------------------------------
# Emily Mitchell
# 6/8/23
#
# Plot GitHub traffic data
#  - pull stored csv files
#  - consolidate to de-duplicate information
#  - make some nice graphs!
# -----------------------------------------------------------------------------

library(dplyr)
library(stringr)
library(lubridate)
library(ggplot2)


# pick repository to view
repo_name = "MEPS"
repo_name = "MEPS-workshop"

#setwd(dirname(rstudioapi::getActiveDocumentContext()$path))


# pull and combine reports ----------------------------------------------------

traffic_dir   = str_glue("traffic_reports/{repo_name}")
traffic_files = list.files(traffic_dir, pattern = "*.csv", full.names = TRUE)

traffic_list <- list()
for(file in traffic_files) {
  # pull file save date from name
  get_file_date = str_extract(file, "\\d{4}-\\d{2}-\\d{2}")
  
  traffic_list[[file]] = read.csv(file) %>% 
    mutate(file_date = get_file_date)
}


# Combine and edit traffic data -----------------------------------------------

all_traffic = bind_rows(traffic_list) %>% 
  as_tibble %>% 
  mutate(traffic_date = str_extract(timestamp, "\\d{4}-\\d{2}-\\d{2}")) %>% 
  
  # convert dates from character to datetime and calculate days between
  mutate(
    traffic_date = ymd(traffic_date),
    file_date   = ymd(file_date),
    days_between = as.numeric(file_date - traffic_date)) %>% 

  # Remove first and last day of 2-week tracking period, 
  # since counts may not represent full days
  filter(days_between > 0 & days_between < 14)


all_traffic_unique = all_traffic %>% 
  distinct(count, uniques, traffic_date)


# Now make a beautiful graph! -------------------------------------------------


ggplot(all_traffic_unique) +
  geom_line(aes(x = traffic_date, y = count), color = "#0366d6", size = 1) +
  geom_point(aes(x = traffic_date, y = count), fill = "#0366d6", shape = 21, size = 3, color = "white", stroke = 0.5) +
  
  geom_line(aes(x = traffic_date, y = uniques), color = "#28a745", size = 1) +
  geom_point(aes(x = traffic_date, y = uniques), fill = "#28a745", shape = 21, size = 3, color = "white", stroke = 0.5) +
  labs(x = "", y = "") +
  theme_minimal()

  
  

