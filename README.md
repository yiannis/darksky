## Description
If you are an amateur astronomer and want to make deep sky observations under a dark sky, you want to know the times when the sun and moon will be below the horizon.

This script - given a start and end date and the observer coordinates - will print a list of times and durations where the sky can be considered dark enough for deep sky observing.
That means the sun should be lower than 18 degrees below the horizon and the moon should be below the horizon also (5 degrees is hardcoded right now, although this depends on moon phase).

The output is a csv file with the following columns:
Description,Start Date,Start Time,End Date,End Time

You can open this file with a spreadsheet application for viewing / editing.
Alternatively, you can import it in a calendar (eg. you can directly import the .csv file in your Google calendar)

## Usage:
./dark-sky --begin '2015/03/31 12:00:00' --end '2015/05/01 12:00:00' --lon '23.716667' --lat '37.966667' --elev 100" [file.csv]
The default location is Athens, Greece.


## Disclaimer :-P
I wrote this script for myself - learning Python on the way...
It looks that it is working OK, but I'm not making any bold claims about accuracy.
Here is an output:
Subject,Start Date,Start Time,End Date,End Time
Dark Sky (0.1h) Moon 88%,2015-06-05,22:38:00,2015-06-05,22:42:00
Dark Sky (0.8h) Moon 80%,2015-06-06,22:39:00,2015-06-06,23:28:00
Dark Sky (1.5h) Moon 70%,2015-06-07,22:40:00,2015-06-08,00:10:00
Dark Sky (2.2h) Moon 59%,2015-06-08,22:41:00,2015-06-09,00:50:00
Dark Sky (2.8h) Moon 47%,2015-06-09,22:41:00,2015-06-10,01:27:00
Dark Sky (3.4h) Moon 35%,2015-06-10,22:42:00,2015-06-11,02:04:00
Dark Sky (4.0h) Moon 25%,2015-06-11,22:43:00,2015-06-12,02:41:00
Dark Sky (4.6h) Moon 15%,2015-06-12,22:43:00,2015-06-13,03:21:00
Dark Sky (5.3h) Moon 8%,2015-06-13,22:44:00,2015-06-14,04:02:00

As you can see even a 5 minute window will be printed
