import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def user_filter_input():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    cities = ['chicago', 'new york city', 'washington']

    while True:
        city= input('Please choose a city from chicago, new york city, or washington:\n').lower()
        if city not in cities:
            print('Please choose a valid city:')
        else:
            break
    # TO DO: get user input for month (all, january, february, ... , june)

    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

    while True:
        month = input('Enter a month between January and June or select all:\n').lower()
        if month not in months:
            print('You have made an invalid selection, please choose a correct month:')
        else:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    days = ['sunday','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

    while True:
        day = input('Enter a day of the week or all days:\n').lower()
        if day not in days:
            print('Please choose a correct day:')
        else:
            break

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

    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month

    df['day'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print('data frame has columns:\n', df.columns)

    print('data frame has NaN values:\n', df.isnull().sum().sum())

    # TO DO: display the most common month

    most_common_month = df['month'].mode()[0]

    print('Most common month:\n', most_common_month)

    # TO DO: display the most common day of week

    most_common_day = df['day'].mode()[0]

    print('Most common day of week:\n', most_common_day)


    # TO DO: display the most common start hour

    df['hour'] = df['Start Time'].dt.hour

    most_common_hour = df['hour'].mode()[0]

    print('Most common start hour of the day is:\n', most_common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station

    most_common_start_station = df['Start Station'].mode()[0]

    print('Most common start station is: \n' , most_common_start_station)


    # TO DO: display most commonly used end station

    most_common_end_station = df['End Station'].mode()[0]

    print('Most common end station is:\n', most_common_end_station)


    # TO DO: display most frequent combination of start station and end station trip

    most_freq_combo=df.groupby(['Start Station', 'End Station']).size().nlargest(1)

    print('Most commonly used combination of Start station and End Stations is: \n', most_freq_combo)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time

    total_travel_time = df['Trip Duration'].sum()

    print('Total travel time is: \n', total_travel_time)


    # TO DO: display mean travel time

    mean_travel_time = df['Trip Duration'].mean()

    print('Mean travel time for a trip is:\n', mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users. It provides information regarding user's gender and birth year"""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types

    user_type = df['User Type'].value_counts()

    print('The count of user types is:\n', user_type)


    # TO DO: Display counts of gender

    if 'Gender' not in df.columns:
            print('There is no gender data available.')

    else:
        gender_count = df['Gender'].value_counts()
        print('The gender count of male and female users is:\n', gender_count)


    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df.columns:
            print('There is no year data available.')

    else:
        earliest_year = df['Birth Year'].min()

        print('The earliest birth year is:\n', earliest_year)

        recent_year = df['Birth Year'].max()

        print('The most recent birth year is:\n', recent_year)

        most_common_year = df['Birth Year'].mode()[0]

        print('The most common birth year is:\n', most_common_year)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        pd.set_option('display.max_columns', 12)

        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
        start_loc = 0
        while view_data.lower() == 'yes':
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
            view_data = input("Do you wish to continue?: ").lower()

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
