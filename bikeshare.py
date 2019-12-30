import time
from datetime import datetime
import pandas as pd
import numpy as np

CITY_DATA = {"chicago": "chicago.csv",
              "new york city": "new_york_city.csv",
              "washington": "washington.csv" }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ""
    while city not in ['chicago', 'new york city', 'washington']:
        city = str(input("Would you like to see bikeshare data for Chicago, New York City or Washington: ")).lower()

    # get user input for month (all, january, february, ... , june)
    month = ""
    while month not in ["january", "february", "march", "april", "may", "june", "all"]:
        month = str(input("Which month between January and February would you like to know bikeshare data for: ")).lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ""
    while day not in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]:
        day = str(input("Which day of the week would you like to seee bikeshare data for: ")).lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #load file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    #convert start time to datetime object
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    #extract month and day of week from Start Time to create new columns
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.weekday_name

    #filter by month if applicable
    if month != "all":
        months = ["january", "february", "march", "april", "june"]
        month = months.index(month) + 1

        #filter by month to create new dataframe
        df = df[df["month"] == month]

    #filter by day of week if applicable
    if day != "all":
        #filter by day to create new dataframe
        df = df[df["day_of_week"] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df["month"].mode()[0]
    print("\nThe most common month is {}".format(popular_month))

    # display the most common day of week
    popular_day = df["day_of_week"].mode().iloc[0]
    print("\nThe most common day is {}".format(popular_day))

    # display the most common start hour
    df["hour"] = df["Start Time"].dt.hour
    popular_hour = df["hour"].mode().iloc[0]
    print("\nThe most common start hour is {}".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df["Start Station"].value_counts().idxmax()
    print("The most commonly used start station is {}".format(popular_start_station))

    # display most commonly used end station
    popular_end_station = df["End Station"].value_counts().idxmax()
    print("The most commonly used End station is {}".format(popular_end_station))

    # display most frequent combination of start station and end station trip
    df["combination_station"] = df["Start Station"] + " to " + df["End Station"]
    popular_combination_station = df["combination_station"].mode().values[0]
    print("The most frequent combination of start and end station trip is {}".format(popular_combination_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print("The total travel time: {}".format(total_travel_time))

    # display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    print("The mean travel time: {}".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df.groupby('User Type')['User Type'].count()
    print("Total number of users by type: {}".format(user_type_count))

    if city != "washington":

    # Display counts of gender
        gender_count = df.groupby("Gender")["Gender"].count()
        print("Count of genders: {}". format(gender_count))

    # Display earliest, most recent, and most common year of birth
        earliest_birth_year = df["Birth Year"].min() #earliest
        print("The earliest year of birth is: {}".format(earliest_birth_year))

        recent_birth_year = df["Birth Year"].max() #most recent
        print("The most recent year of birth is: {}".format(recent_birth_year))

        common_birth_year = df["Birth Year"].mode() #most common
        print("The most common year of birth is: {}".format(common_birth_year))

    else:
        print("\nThis city's database does not contain columns for gender and birth year.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """ Display raw data to user"""

    start_row = 0
    stop_row = 5

    raw_data = input("\nDo you want to see the raw data? Enter yes or no.\n").lower()

    #Display 5 rows of df per user request
    if raw_data == "yes":
        while True:
            print(df.iloc[start_row:stop_row])
            start_row += 5
            stop_row += 5
            raw_data = input("\nDo you want to see the raw data? Enter yes or no.\n").lower()
            if raw_data == "no":
                break



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
