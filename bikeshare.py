from typing import Any, Callable, Iterator

import time
import pandas as pd


CITY_DATA: dict[str, str] = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

MONTH_MAP: dict[str, int] = {
    'january': 1,
    'february': 2,
    'march': 3,
    'april': 4,
    'may': 5,
    'june': 6
}

MONTH_REVERSE_MAP: dict[int, str] = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June'
}

DAY_MAP: dict[str, int] = {
    'monday': 0,
    'tuesday': 1,
    'wednesday': 2,
    'thursday': 3,
    'friday': 4,
    'saturday': 5,
    'sunday': 6
}

DAY_REVERSE_MAP: dict[int, str] = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday'
}


def draw_hr() -> None:
    """
    Draws a horizontal rule to visually separate pages of output.
    """
    print('-' * 40)


def start_printed_timer() -> Callable[[], None]:
    """
    Returns a function that prints the time elapsed since the time this function was called.
    """  # noqa
    start_time = time.time()
    return lambda: print(
        "\nThis took %.2f seconds." % (time.time() - start_time)
    )


def mode(series: pd.Series) -> Any:
    """
    Returns a single mode value of a series.
    """
    return series.mode()[0]


def get_filters() -> tuple[str, str, str]:
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """  # noqa
    print("Hello! Let's explore some US bikeshare data!")

    city: str = get_user_input(
        'Type the name of the city you want to view data for ' +
        '(Chicago, New York City, or Washington):',
        CITY_DATA.keys()
    )

    filter_type: str = get_user_input(
        'Would you like to filter the data by month, day, or not at all? ' +
        'Type "none" for no time filter:',
        ['month', 'day', 'none']
    )

    month: str = get_user_input(
        'Type the name of the month you want to view data for ' +
        '(January, February, March, April, May, or June):',
        MONTH_MAP.keys()
    ) if filter_type == 'month' else 'all'

    day: str = get_user_input(
        'Type the name of the day of the week you want to view data for ' +
        '(Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday):',
        DAY_MAP.keys()
    ) if filter_type == 'day' else 'all'

    draw_hr()
    return city, month, day


def get_user_input(prompt: str, options: list[str]) -> str:
    """
    Returns user input from a list of options.

    Args:
        (str) prompt - the prompt to display to the user
        (list) options - the list of options to present to the user
    Returns:
        (str) the user's input
    """
    print(prompt)

    while True:
        response: str = input().lower()
        if response in options:
            return response

        print("Sorry, I don't understand your input. Please try again!")


def load_data(city: str, month: str, day: str) -> pd.DataFrame:
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """  # noqa

    df: pd.DataFrame = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    return df[
        df['Start Time'].map(
            lambda start_time:
            (month == 'all' or start_time.month == MONTH_MAP[month]) and
            (day == 'all' or start_time.day_of_week == DAY_MAP[day])
        )
    ]


def time_stats(df: pd.DataFrame) -> None:
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    print_time_taken: Callable[[], None] = start_printed_timer()

    month_series: pd.Series = pd.Series(df['Start Time']).map(
        lambda x: MONTH_REVERSE_MAP[x.month]
    )
    print('The most common month was: %s' % mode(month_series))

    day_series: pd.Series = pd.Series(df['Start Time']).map(
        lambda x: DAY_REVERSE_MAP[x.day_of_week]
    )
    print('The most common day was: %s' % mode(day_series))

    hour_series: pd.Series = pd.Series(df['Start Time']).map(
        lambda x: x.hour
    )
    print('The most common start hour was: %s' % mode(hour_series))

    print_time_taken()
    draw_hr()


def station_stats(df: pd.DataFrame) -> None:
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    print_time_taken: Callable[[], None] = start_printed_timer()

    start_end_df: pd.DataFrame = df[['Start Station', 'End Station']]

    print(
        'The most common start station was: %s' %
        mode(start_end_df["Start Station"])
    )

    print(
        'The most common end station was: %s' %
        mode(start_end_df["End Station"])
    )

    most_common_start_end_combination: tuple[str, str] = start_end_df.groupby(
        ['Start Station', 'End Station'], sort=False
    ).value_counts().idxmax()
    print(
        'The most common start/end station combination was: %s' % (
            ' to '.join(most_common_start_end_combination)
        )
    )

    print_time_taken()
    draw_hr()


def trip_duration_stats(df: pd.DataFrame) -> None:
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    print_time_taken: Callable[[], None] = start_printed_timer()

    trip_duration_series: pd.Series = (
        df['End Time'] - df['Start Time']
    ).map(lambda x: x.total_seconds())

    print(
        'The total travel time was: %.1f days' %
        (trip_duration_series.sum() / 86_400)
    )

    print(
        'The average travel time was: %.1f minutes' %
        (trip_duration_series.mean() / 60)
    )

    print_time_taken()
    draw_hr()


def user_stats(df: pd.DataFrame) -> None:
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    print_time_taken: Callable[[], None] = start_printed_timer()

    def print_group_counts(group_name: str) -> None:
        group_series: pd.Series = df[group_name].groupby(
            df[group_name], sort=False
        ).count()

        for (group, count) in group_series.items():
            print('%d %s users' % (count, group))

        print()

    print('User type statistics:')
    print_group_counts('User Type')

    if 'Gender' in df:
        print('Gender statistics:')
        print_group_counts('Gender')

    if 'Birth Year' in df:
        birth_year_series: pd.Series = df['Birth Year']
        print('The youngest user was born in %d' % birth_year_series.max())
        print('The oldest user was born in %d' % birth_year_series.min())
        print('The most common year of birth was %d' % mode(birth_year_series))

    print_time_taken()
    draw_hr()


def get_batched_dataframe_iterator(
    df: pd.DataFrame, batch_size: int
) -> Iterator[list[dict]]:
    offset: int = 0
    while offset < len(df):
        yield df[offset:offset + batch_size].to_dict('records')
        offset += batch_size


def raw_data(df: pd.DataFrame, batch_size: int) -> None:
    """
    Displays raw data with the specified number of rows at a time.
    """
    first_display: bool = True
    for batch in get_batched_dataframe_iterator(df, batch_size):
        # This check is done at the start of the loop to avoid displaying
        # the prompt when the list has already been exhausted.
        if not first_display:
            if input(
                '\nSee more raw data? Enter yes or no.\n'
            ).lower() != 'yes':
                return
        print(batch)
        first_display = False
    print('No more data to display!')


def main() -> None:
    try:
        while True:
            city, month, day = get_filters()
            df: pd.DataFrame = load_data(city, month, day)

            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            if input('\nSee raw data? Enter yes or no.\n').lower() == 'yes':
                print()
                raw_data(df, 5)

            if input(
                '\nWould you like to restart? Enter yes or no.\n'
            ).lower() != 'yes':
                print('Bye!')
                break
    except (KeyboardInterrupt, EOFError):
        print('Bye!')


if __name__ == "__main__":
    main()
