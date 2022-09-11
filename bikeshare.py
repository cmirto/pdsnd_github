import time
import pandas as pd
import numpy as np
import calendar
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    print()
    while True:
        cities = ['chicago', 'new york city','washington']
        city = input('\nWhat city would you like to see analyze (Chicago, New York City, or Washington)? \n').lower()
        if city in cities:
            break
        else:
            print('\nSorry, wrong input. Please input a valid city \n')

      # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        months = ['all','january', 'february', 'march', 'april', 'may', 'june']
        month = input('\nWhat month would you like to see data for? Enter month: January, February, March, April, May, June. Or type All for all months.\n').lower()
        if month in months:
            break
        else:
            print('\nPlease enter a valid month')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = input('\nWhat day do you want see data for? Enter Day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday. Or type All for all days.\n').lower()
        if day in days:
            break
        else:
            print('\nPlease enter a valid day')

    print('-'*40)
    return city, month, day

## load data based on the filters that were inputted

def load_data(city, month, day):
    """
    This will load data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.day_name()

     # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int

        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1


        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    df.fillna(0)

    # filter by day of week if applicable
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel based on the city you selected."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    pop_month_name = calendar.month_name[popular_month]
    print('The most popular month is: {}'.format(pop_month_name))
    df.groupby(['month'])['month'].count()

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('The most popular day is:', popular_day)

    # TO DO: display the most common start hour
    df['hour']= pd.DatetimeIndex(df['Start Time']).hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular hour is:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations."""

    print('\nCalculating The Most Popular Stations\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most popular Start Station is:', popular_start_station)

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most popular End Station is:', popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    start_end_stations = df['Start Station'] +' >>> ' + df['End Station']
    popular_combo = start_end_stations.mode()[0]
    print('The most popular combination of stations is (Start >>> End):', popular_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = round(df['Trip Duration'].sum())
    days, remainder = divmod(total_travel_time, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    print('The total time traveled: {} days, {} hours, {} minutes, {} seconds'.format(days, hours, minutes, seconds ))

    # TO DO: display mean travel time
    avg_travel_time = round(df['Trip Duration'].mean())
    days, remainder = divmod(avg_travel_time, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    print('The average travel time is: {} days, {} hours, {} minutes, {} seconds'.format(days, hours, minutes, seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    try:
        user_types = df['User Type'].value_counts()
        print('Here are the different user types, and the amount of each type:\n')
        print(user_types)

    # TO DO: Display counts of gender
        gender_count = df['Gender'].value_counts()
        print("\nHere is the amount of users based on gender:\n")
        print(gender_count)

    # TO DO: Display earliest, most recent, and most common year of birth
        oldest_year = round(df['Birth Year'].min())
        youngest_year = round(df['Birth Year'].max())
        common_year = round(df['Birth Year'].mode()[0])

        print('\nHere are stats on the users based on their birth year:\n')
        print('The oldest birth year is:', oldest_year)
        print('The youngest birth year is:', youngest_year)
        print('The most common birth year is:', common_year)

    except KeyError:
        print('\nThere is no Gender or Birth Year data for your selected city.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


    ## Give user the option to see a sample of the raw data
    starting_row = 0
    while True:
        display_data = input('\nWould you like to see a sample of the raw data? Enter yes or no\n').lower()
        if display_data.lower() == 'yes':
            print(df.iloc[starting_row : starting_row + 5])
            starting_row += 5
            display_data = input('Would you like to see more data? Enter yes or no\n').lower()
            print(df.iloc[starting_row : starting_row + 5])

        elif display_data.lower() == 'no':
            break
        else:
            print('\nPlease enter yes or no.' )


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
