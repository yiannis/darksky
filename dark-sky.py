#!/usr/bin/python

import math
import ephem

import sys, getopt

# Astronomical dawn or dusk is when the Sun is >18deg below horizon
# For the Moon 5deg should(?) be OK
# Also, MOON_MAX_ALT could be a function of moon.phase so that
# we get a more extended nightfall duration when a cresent moon rises/sets
MOON_MAX_ALT = ephem.degrees('-5')
SUN_MAX_ALT  = ephem.degrees('-18')
HOURS_IN_DAY = 24

# The sky could(?) be considered dark if the moon phase is less than 2%
MOON_MAX_PHASE = 2


# Command line options
USAGE= sys.argv[0] \
 + ' --begin <YYYY/MM/DD hh:mm:ss> --end <YYYY/MM/DD hh:mm:ss> --lat <DD.xxx> -lon <DD.xxx> --elev <meters> [output file]' \
 + "\n\n\tE.g.: --begin '2015/03/31 12:00:00' --end '2015/05/01 12:00:00' --lon '23.716667' --lat '37.966667' --elev 100" \
 + "\n\nDefault location is Athens, Greece\n"

try:
    opts, args = getopt.getopt( sys.argv[1:], "hv", ['help', 'verbose', 'begin=', 'end=', 'lat=', 'lon=', 'elev='] )
except getopt.GetoptError:
    print USAGE
    sys.exit(2)

opt_begin = ''
opt_end   = ''
opt_lon   = '23.716667'
opt_lat   = '37.966667'
opt_elev  = 100
opt_verbose = 0

for option, argument in opts:
    if option in ('-h', '--help'):
        print USAGE
        sys.exit(1)
    elif option in ('-v', '--verbose'):
        opt_verbose = 1
    elif option == '--begin':
        opt_begin = argument
    elif option == '--end':
        opt_end = argument
    elif option == '--lat':
        opt_lat = argument
    elif option == '--lon':
        opt_lon = argument
    elif option == '--elev':
        opt_elev = argument

if not opt_begin or not opt_end:
	print USAGE
	sys.exit(1)

if args:
    outfile = args[0]
else:
    outfile = 'dark-sky.csv'

print 'Saving calendar to file: ', outfile


# Init ephemeris objects
start_date = ephem.Date(opt_begin)
end_date   = ephem.Date(opt_end)
step       = ephem.minute

athens = ephem.Observer()
athens.lon = opt_lon
athens.lat = opt_lat
athens.elevation = opt_elev


# Write calendar in .csv
csv = open( outfile, 'w' )
csv.write( 'Subject,Start Date,Start Time,End Date,End Time\n' )

nightfall_previous   = 0
nightfall_start_date = 0
current_date = start_date
while current_date < end_date:
	athens.date = current_date

	moon = ephem.Moon(athens)
	sun  = ephem.Sun(athens)

	if sun.alt < SUN_MAX_ALT and (moon.alt < MOON_MAX_ALT or moon.phase < MOON_MAX_PHASE):
	  nightfall = 1
	else:
	  nightfall = 0

	local_date = ephem.localtime( ephem.Date( current_date ) )

	if opt_verbose:
		print '{date},{sun_alt},{moon_alt},{moon_phase},{night}'.format(
			date       = local_date,
			sun_alt    = sun.alt,
			moon_alt   = moon.alt,
			moon_phase = moon.phase,
			night      = nightfall,
		)

	if nightfall and not nightfall_previous:
		nightfall_start_date = current_date
	if not nightfall and nightfall_previous:
		duration = (current_date - nightfall_start_date) * HOURS_IN_DAY
		local_nightfall_start_date = ephem.localtime( ephem.Date( nightfall_start_date ) )
		csv.write( 'Dark Sky ({span:.1f}h) Moon {phase:.0f}%,{date0},{time0},{date1},{time1}\n'.format(
			date0       = local_nightfall_start_date.date(),
			date1       = local_date.date(),
			time0       = local_nightfall_start_date.strftime('%H:%M:%S'),
			time1       = local_date.strftime('%H:%M:%S'),
			phase       = moon.phase,
			span        = duration
		))

	nightfall_previous = nightfall
	current_date += step
