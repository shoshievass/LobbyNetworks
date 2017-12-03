library(tidyverse)
library(stringr)

# event <- read_csv("Data/events2.csv")
event <- read_csv("Data/event.csv")

blockToArray <- function(s){
  unbracketed_str <- substr(s,2,str_length(s) - 1)
  char_array <- (str_split(unbracketed_str, ","))
  return(char_array)
}

strArrays <- blockToArray(event$hosts_id)

event_data <- event %>%
  group_by(row_number()) %>%
  mutate(
    event_id = X1,
    host_id_array = blockToArray(hosts_id)
  ) %>%
  ungroup() %>%
  select(
    hosts_id,
    host_id_array,
    event_id
  ) %>%
  unnest(host_id_array)

event_data %>%
  mutate_all(funs(as.factor)) %>%
  xtabs(~ event_id + host_id_array, data = .) ->
  event_matrix

H_mat <- crossprod(event_matrix)
save.image(file = "host_cross_data.rdata")

## Plot frequencies
own_appearances <- diag(H_mat)
joint_showing <- (colSums(H_mat) - own_appearances)
sum(joint_showing)

hist(joint_showing)
plot(log(own_appearances), log(joint_showing))
table(joint_showing)
