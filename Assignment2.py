#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Assignment 2."""


import argparse
import csv
import datetime
import logging
import urllib2
from pprint import pprint


def downloadData(url=str):
    """This function opens an inputed url and return the result to the caller.

    Args:

        url (str): A string that is a URL address.

    Returns:

        file object (various): A file object assigned to the variable
        downloadcsvfie.

    Example:

        >>> downloadData(
        'https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv')
        <addinfourl at 140707426406128 whose fp =
        <socket._fileobject object at 0x7ff9003234d0>>
    """
    downloadcsvfile = urllib2.urlopen(url)
    return downloadcsvfile
#test1 = downloadData(url)
#print test1

logging.basicConfig(filename='error.log', level=logging.ERROR)
logger = logging.getLogger('assignment2')

def processData(downloadcsvfile):
    """This function takes a variable that has an assigned file object to it,
       then converts it into a dict.

       The dict is keyed by ID#, with its value a two item tuple. The first item
       in the tuple is a persons name, the second item is there birthdate as a
       datetime object.

       Any line in the file that cannot be converted is logged to an error.log
       file.

    Args:
        downloadcsvfile (file object): A file downloaded from a URL by the
        downloadData() function.

    Returns:

        dictcsv (dict): A dictionary keyed by a string that reffers to an ID#.
        Each key in dict has a value of a two item tuple.The first item in the
        tuple is a string of a persons name. The second item in the tuple is the
        persons birthdate as a datetime object.

        {'ID#' : ('Persons Name', datetime.datetime(YYYY, MM, DD, O, O))}

    Example:

        >>> test2 = processData(test1)
        >>> from pprint import pprint
        >>> print pprint(test2)
        {'1': ('Charles Paige', datetime.datetime(1963, 1, 6, 0, 0)),
         '10': ('Una James', datetime.datetime(1981, 9, 5, 0, 0)),
         '100': ('Austin Burgess', datetime.datetime(1979, 6, 4, 0, 0)),
         '11': ('Angela Watson', datetime.datetime(1994, 4, 15, 0, 0)),
         '12': ('Rebecca Hudson', datetime.datetime(1975, 9, 6, 0, 0)),
         '14': ('Adam Hudson', datetime.datetime(1975, 5, 7, 0, 0)),
         '15': ('Jack Walsh', datetime.datetime(2012, 10, 29, 0, 0)),
         '16': ('Felicity Churchill', datetime.datetime(1983, 11, 9, 0, 0)),
         '17': ('Melanie Mills', datetime.datetime(2007, 2, 12, 0, 0)),
         '18': ('Neil Turner', datetime.datetime(2008, 5, 18, 0, 0)),
         '19': ('Deirdre Mathis', datetime.datetime(2010, 1, 2, 0, 0)),}
    """
    reader = csv.DictReader(downloadcsvfile)
    dictcsv = {}
    for line, row in enumerate(reader):
        try:
            dictcsv[row['id']] = (row['name'], datetime.datetime.strptime(row['birthday'], '%d/%m/%Y'))
        except:
            logging.error('Error processing line #{} for ID#{}'.format(line, row['id']))
    return dictcsv
#test2 = processData(test1)
#from pprint import pprint
#print pprint(test2)


def displayPerson(id=int, personData=dict):
    formatdate = '%Y-%m-%d'
    #if personData[str(id)]:
    #    data=personData.get(str(id))
        #print 'Person {} is {} with a birthday of {}'.format(str(id), str(data[0]), (data[1].strftime(formatdate)))
    #    print 'Person {} is {} with a birthday of {}'.format(id, data[0], (data[1].strftime(formatdate)))
    #else:
    #    print 'No user found with that id'
    key = str(id)
    if key in personData.keys():
        print 'Person #{} is {} with a birthday of {}'.format(id, personData[key][0], datetime.datetime.strftime(personData[key][1], formatdate))
    else:
        print 'No user found with that ID#.'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", "-u", help="Enter a URL to begin.", required=True)
    args = parser.parse_args()
    
    try:
        csvData = downloadData(args.url)
    except:
        print 'An error has occured session terminated.'
        raise SystemExit
    else:
        personData = processData(csvData)
        idlookup = raw_input('Please enter an ID# to lookup. ')
        print idlookup
        idlookup = int(idlookup)
        if idlookup <= 0:
            print 'Invalid ID Number entered (Number must be greater than Zero [0]).\n\
            Exiting program......Good Bye.'
            raise SystemExit
        else:
            displayPerson(idlookup, personData)
            main()

if __name__ == '__main__':
    main()
