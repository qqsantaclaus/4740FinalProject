# Load data
trips <- read.csv('./data/50_61_aggregated_by_date.csv', header = T, na.strings='')
dim(trips)
trips[1:10, ]
colnames(trips)
sum(trips$is_weekday == 1) / sum(trips$is_weekday == 0)

# Only look at weekdays
trips = trips[trips$is_weekday == 1, ]
dim(trips)

# remove irrelevant columes
trips = trips[, !colnames(trips) %in% c("station_id_1", "station_id_2", "date", "is_weekday", "zip_code")]

# identify empty entries
# Let <NA> in “events” also be a level
sum(is.na(trips))
levels(trips$events)
trips$events <- addNA(trips$events)
levels(trips$events)
sum(is.na(trips))

# Convert "T" in precipitation record to 0 
# ("T" stands for detected but immeasurable precipitation)
Tindex = trips$precipitation_inches == "T"
sum(Tindex)
trips$precipitation_inches[Tindex] = 0
sum(trips$precipitation_inches == "T")

# remove lines with empty entries (which should be numeric)
trips <- trips[complete.cases(trips), ]
sum(is.na(trips))
dim(trips)

# check data types
is.numeric(trips$max_gust_speed_mph)
is.numeric(trips$precipitation_inches)
trips$precipitation_inches = as.numeric(trips$precipitation_inches)
is.numeric(trips$precipitation_inches)

# Train-test split
set.seed(2)
train_indices = sample(1:nrow(trips), nrow(trips)/2)
train_trips = trips[train_indices, ]
test_trips = trips[-train_indices, ]
train_truth = trips$num_trips[train_indices]
test_truth = trips$num_trips[-train_indices]

# Try basic linear regression
trips_lm = lm(num_trips~.,data=trips, subset=train_indices)
summary(trips_lm)
pred = predict(trips_lm, newdata = test_trips)
plot(pred, test_truth)
