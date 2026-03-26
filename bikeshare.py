import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]
months = ["all", "january", "february", "march", "april", "may", "june"]



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington)
    city = input('Would you like to analyze "chicago", "new york city" or "washington"\nYour input:').lower()

    #checks if the input is valid
    while city not in CITY_DATA:
        city = input('This is not a valid city.\nPlease enter "chicago", "new york city" or "washington"\nYour input:').lower()

    # get user input for month (all, january, february, ... , june)
    month = input('Please select the month.\nPossible months are "january", "february", "march", "april", "may", "june" or "all"\nYour input:').lower()

    # checks if the input is valid
    while month not in months:
        month = input('This is not a valid month.\n Possible months are "january", "february", "march", "april", "may", "june" or "all"\nYour input:').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please select the day.(e.g., monday, tuesday...).\nType "all" to see all days.\nYour input:').lower()

    #checks if the input is valid
    while day not in days:
        day = input('This is not a valid day.\nPossible days are "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday" or "all"\nYour input:').lower()

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]



    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df["month"].mode()[0]
    print('Most Frequent Month:', months[popular_month].title())

    # display the most common day of week
    popular_day = df["day_of_week"].mode()[0]
    print('Most Frequent Day Of Week:', popular_day)

    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df["Start Station"].mode()[0]
    print("Most Common Start Station: ", popular_start_station)

    # display most commonly used end station
    popular_end_station = df["End Station"].mode()[0]
    print("Most common End Station: ", popular_end_station)

    # display most frequent combination of start station and end station trip
    end_start_combination = df.groupby(['Start Station','End Station']).size().idxmax()
    print("Most common combination of Start and End Station: ", end_start_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print("Total Travel Time in hours:", total_travel_time / 3600.0)

    # display mean travel time
    mean_travel_time = int(df["Trip Duration"].mean())
    print("Mean Travel Time in hours:", mean_travel_time / 3600.0)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    #fills NaN values of User Type with string "No User Type"
    df["User Type"].fillna("No User Type", inplace=True)
    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    try:
        # Display counts of gender
        df["Gender"].fillna("Missing Gender", inplace=True)
        gender_counts = df['Gender'].value_counts()
        print(gender_counts)
    except:
        # if no gender information given, prints text
        print("No gender values given.")

    try:
        # fills empty Birth Year rows with the mean value
        df["Birth Year"].fillna(df["Birth Year"].mean(), inplace=True)

        # Display earliest, most recent, and most common year of birth
        earliest_year = int(df["Birth Year"].min())
        most_recent_year = int(df["Birth Year"].max())
        most_common_year = int(df["Birth Year"].mode()[0])

        print("Earliest Year of Birth: {}\nMost recent Year of Birth: {}\nMost common Year of Birth: {}".format(earliest_year, most_recent_year, most_common_year))
    except:
        # if no birth year given, prints this text
        print("No birth year given.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """displays individual data
    5 rows will be added with each enter"""
    print("press enter to see row data, press no to skip")
    x = 5
    while (input() != "no"):
        print(df.head(x))
        x += 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
