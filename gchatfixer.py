#!/usr/bin/env python3

"""
Copyright (c) <year>, <copyright holder>
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""


import sys
import json
import click
import pytz
import datetime as dt
from utils import timeit
from output import message


@click.command()
@click.option('--gchat_file','-f',help='Google Chat file from takeout',required=True)
@click.option('--time_zone','-tz',help='Time zone to normalize the chats into (sorry, only one is allowed for now)')
@click.option('--output_file','-o',help='File to write to')
@click.option('--show_messages',help='Print the messages as we go. This will take a very long time.',is_flag=True)
@click.option('--verbose','-v',help='Increase verbosity',count=True)


@timeit
def main(gchat_file, time_zone, output_file, show_messages, verbose):

    if show_messages:
        message('showing all the messages will take a very long time. are you really sure? [y/n]', status='error')
        proceed = input('... ').lower()[0]
        if proceed != 'y':
            message('did not get permission to proceed. EXITING', status='error')
            sys.exit()

    # first validate the time zone
    if time_zone:
        message(f"validating local time zone specified as: {time_zone}")
        try:
            local_tz = pytz.timezone(time_zone)
            message(f"{time_zone} is valid!", level=1)
        except Exception as e:
            error_message = f"looks like something went wrong with your specified time zone. try one of the time zones below or run pytz.all_timeozones in a python3 shell to see all valid time zones.\n"
            error_message += f"'US/Pacific\n"
            error_message += f"'US/Mountain\n"
            error_message += f"'US/Central\n"
            error_message += f"'US/Eastern\n"
            error_message += f"the full error message is: {e}"
            message(error_message, status='error')
            sys.exit()

    # read in the file
    with open(gchat_file, 'r') as f:
        gchat_file = json.load(f)

    messages = gchat_file['messages']
    
    if verbose:
        message("messages successfully loaded! here's the first!")
        message(messages[0], level=1)

    human_messages = [f"PLEASE NOTE: All messages have been converted to time zone: {local_tz}"]

    for m in messages:

        try:
            # parse it into human kind of strings
            # name = first name only
            name = m['creator']['name'].split(' ', 1)[0]

            # date = human date with timezone applied
            mdate = dt.datetime.strptime(m['created_date'], '%A, %B %d, %Y at %I:%M:%S %p %Z')
            mdate = pytz.utc.localize(mdate)
            mdate = f"{mdate.astimezone(local_tz):%D %I:%M:%S %p}"

            human_message = f"[{mdate}] {name}: {m['text']}"
            human_messages.append(human_message)

            if show_messages: message(human_message, level=1)
        
        except Exception as e:
            continue

    # write it out to a txt doc
    if output_file:
        message(f'now writing to {output_file}')
        with open(output_file, 'w') as f:
            f.write('\n'.join(human_messages))

    return


if __name__ == '__main__':
    main()
