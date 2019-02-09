#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Assignment 2."""


import argparse
import csv
import datetime
import logging
import urllib2


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


#logging.basicConfig(filename='error.log', level=logging.ERROR)
#logger = logging.getLogger('assignment2')



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
        tuple is a string of a persons name. The second item in the tuple is
        the persons birthdate as a datetime object.

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
            dictcsv[row['id']] = (
                row['name'], datetime.datetime.strptime(
                    row['birthday'], '%d/%m/%Y'))
        except:
            logging.basicConfig(filename='error.log', level=logging.ERROR)
            logger = logging.getLogger('assignment2')
            logger.error(
                "Error processing line #%d for ID #%s", line, row['id'])
    return dictcsv


def displayPerson(id=int, personData=dict):
    """ This function finds an id number in a dictionary, and returns the key
        and value assigned to the id number.

    Args:

        id (int, str): args to find, and return, key and value of id entered
        in dict provided in personData.
        personData (dict): args to be serched by key endered in id.

    Returns:

        (str): a string formated with the id number entered and its
        corresponding values found in the dict entered in personData.
        'Person #{id} is {dict[key][0]} with a birthday of{dict[key][1]}'
        If id not in dict provided in personData a string is returned stating
        'No user found with that id'

    Examples:

        >>> test1 = downloadData(
        'https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv')
        >>> test2 = processData(test1)
        >>> displayPerson(34, test2)
        Person #34 is Rachel Cameron with a birthday of 1999-02-22
        >>> displayPerson(10000, test2)
        No user found with that id.
        >>> displayPerson(98, test2)
        Person #98 is Alexander Dyer with a birthday of 1982-05-14
        >>> displayPerson(0, test2)
        No user found with that id.
        >>> displayPerson(-34, test2)
        No user found with that id.
    """
    formatdate = '%Y-%m-%d'
    key = str(id)
    if key in personData.keys():
        print 'Person #{} is {} with a birthday of {}'.format(
            id, personData[key][0], datetime.datetime.strftime(
                personData[key][1], formatdate))
    else:
        print 'No user found with that id.'


def main():
    """ This function combines the downloadData(), processData(), and
        displayPerson() functions into a single function to be run on the
        command line.

        main() dowloads a file from a provided --url, processes the data,
        then ask the user to enter an ID# to look up. The number entered
        by the user is used to search for the coresponding key in the processed
        data and displays the persons number, name, and birthdate.

        If an impropper --url is input, an error message is raised and the
        program exits.

        if a number <= 0 is entered,an error message is raised and the
        program exits.

    Exsample:

        $ python Assignment2.py --url
        'https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.cv'
        An error has occured session terminated.
                Exiting the program......Good Bye.
        $ python Assignment2.py --url
        'https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv'
        Please enter an ID# to lookup. 100
        Person #100 is Austin Burgess with a birthday of 1979-06-04
        Please enter an ID# to lookup. 45
        Person #45 is Audrey Butler with a birthday of 1979-09-20
        Please enter an ID# to lookup. 66
        Person #66 is Colin Payne with a birthday of 1975-02-17
        Please enter an ID# to lookup. 10000
        No user found with that id.
        Please enter an ID# to lookup. -34
        Invalid ID entered (Number must be greater than Zero [0]).
                    Exiting the program......Good Bye.

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="Enter a URL to begin.", required=True)
    args = parser.parse_args()
    try:
        csvData = downloadData(args.url)
    except:
        print 'An error has occured session terminated.\n\
        Exiting the program......Good Bye.'
        raise SystemExit
    else:
        personData = processData(csvData)
        idlookup = raw_input('Please enter an ID# to lookup. ')
        idlookup = int(idlookup)
        if idlookup <= 0:
            print 'Invalid ID entered (Number must be greater than Zero[0]).\n\
            Exiting the program......Good Bye.'
            raise SystemExit
        else:
            displayPerson(idlookup, personData)
            main()

if __name__ == '__main__':
    main()
