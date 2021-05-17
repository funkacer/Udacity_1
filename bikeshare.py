import time
import pandas as pd
import numpy as np

pd.options.display.max_columns = 15

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def check_input(inp, lst):
    """
    Check if input is in the list of options.

    Args:
        (str) inp - user input to check
        (list) lst - list of options to choose from
    Returns:
        (str) out - selected option from list or None
    """
    found = 0
    for inp_check in lst:
        if inp_check.startswith(inp):
            out = inp_check
            found += 1
    if found == 1:
        print('OK, you have chosen ' +  out.title() + '.')
    else:
        out = None
        print('Your answer fits to {} possible options. Please try again.'.format(found))
    return out


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while city not in CITY_DATA:
        city = input('\nPlease enter name of the city to analyze (Chicago, New York City, Washington):\n').lower()
        city = check_input(city, CITY_DATA)


    # TO DO: get user input for month (all, january, february, ... , june)
    month = ''
    while month not in MONTHS + ['all']:
        month = input('\nPlease enter name of the month to filter by (January thru June), or "all" to apply no month filter:\n').lower()
        month = check_input(month, MONTHS + ['all'])


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while day not in DAYS + ['all']:
        day = input('\nPlease enter name of the day of week to filter by, or "all" to apply no day filter:\n').lower()
        day = check_input(day, DAYS + ['all'])


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

    filename = CITY_DATA[city]
    df = pd.read_csv(filename)

    # convert dtype object to datetime

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # I need these fiels to filters
    df['month'] = df['Start Time'].dt.month
    # int month: 1 is January
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    # int day: The day of the week with Monday=0, Sunday=6

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month_index = MONTHS.index(month)
        # filter by month to create the new dataframe
        df = df[df['month'] == month_index + 1]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        day_index = DAYS.index(day)
        df = df[df['day_of_week'] == day_index]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month_index = df['month'].mode()[0] - 1
    popular_month = MONTHS[popular_month_index]
    print('Most Frequent Start Month:', popular_month.title())


    # TO DO: display the most common day of week
    popular_day_of_week_index = df['day_of_week'].mode()[0]
    popular_day_of_week = DAYS[popular_day_of_week_index]
    print('Most Frequent Start Day:', popular_day_of_week.title())

    # TO DO: display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)


    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['Start End Station'] = 'from ' + df['Start Station'] + ' to ' + df['End Station']
    popular_start_end_station = df['Start End Station'].mode()[0]
    print('Most Popular Trip:', popular_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    years = total_travel_time // (365*24*3600)
    days = total_travel_time % (365*24*3600) // (24*3600)
    hours = total_travel_time % (24*3600) // 3600
    minutes = total_travel_time % 3600 // 60
    seconds = total_travel_time % 60
    #print('Total Trip Duration: ', total_travel_time)
    print('Total Travel Time: {} years, {} days, {} hours, {} minutes, {} seconds'.format(years, days, hours, minutes, seconds))

    # TO DO: display mean travel time
    average_travel_time = df['Trip Duration'].mean().astype(int)
    hours = average_travel_time // 3600
    minutes = average_travel_time % 3600 // 60
    seconds = average_travel_time % 60
    #print('Average Trip Duration: ', average_travel_time)
    print('Mean Travel Time: {} hours, {} minutes, {} seconds'.format(hours, minutes, seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('Counts of user types:')
    print(df['User Type'].value_counts().to_string())


    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        print('\nCounts of gender:')
        print(df['Gender'].value_counts().to_string())
    else:
        print('\nGender statistics not available in Washington.')


    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nStatistics of year of birth:')
        print('Earliest year of birth is', df['Birth Year'].min().astype(int))
        print('Most recent year of birth is', df['Birth Year'].max().astype(int))
        print('Most common year of birth is', df['Birth Year'].mode()[0].astype(int))
    else:
        print('\nYear of birth statistics not available in Washington.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_output(df):
    """Displays raw data 5 rows at a time."""

    answer = ''
    while answer not in ['yes', 'no']:
        answer = input('\nWould you like to see raw data? Enter yes or no.\n').lower()
        answer = check_input(answer, ['yes', 'no'])

    if answer == 'yes':
        row_index = 0
        while answer == 'yes':
            to = row_index + 5
            if to > len (df): to = len(df)
            print(df.iloc[row_index : row_index + 5, : ])
            row_index = to
            if row_index >= len(df):
                print('No more data to show!')
                answer = 'no'
                break
            answer = ''
            while answer not in ['yes', 'no']:
                answer = input('\nWould you like to see more data? Enter yes or no.\n').lower()
                answer = check_input(answer, ['yes', 'no'])


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_output(df)

        answer = ''
        while answer not in ['yes', 'no']:
            answer = input('\nWould you like to restart? Enter yes or no.\n').lower()
            answer = check_input(answer, ['yes', 'no'])
        if answer.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
