#!/usr/bin/env python2.7

import psycopg2
from pprint import pprint


def question1():
    """ Return the top 3 most popular articles of all time with views total """
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    """articlespath its a view to return '/article/' + path.slug for table join
     to work"""
    query = "select title, count(*) as views from articlespath, log where \
    articlespath.slugpath = log.path group by articlespath.title order by \
    views desc limit 3;"
    c.execute(query)
    rows = c.fetchall()

    # Return each top article with the amount of views
    print "\nThe top 3 most popular articles of all time:\n"
    list = 0
    for row in rows:
        list += 1
        print list, row[:][0], ' - ', row[:][1], 'Views'
    print
    db.close()


def question2():
    """ Return the most popular article authors of all time """
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    query = "select authors.name, sum(views) as views from authors, \
    totalviews where authors.id = totalviews.author group by \
    authors.name order by views desc;"
    c.execute(query)
    rows = c.fetchall()

    # Return each top article author witht the amount of total views
    print "\nThe top most popular article authors of all time:\n"
    list = 0
    for row in rows:
        list += 1
        author = row[:][0]
        views = row[:][1]
        print list, format(author, '<22'), ' - ', format(views, '>6'),\
            'Total Views'
    print
    db.close()


def question3():
    """ Return the days in which more than 1'%' lead to errors"""
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    query = "select to_char(date,'MON DD, YYYY') as date, \
    round(100*(errors/totalerrors.sum),1) as percentage from totalerrors,\
    errorsdate;"
    c.execute(query)
    rows = c.fetchall()

    # Return each row with date 'MON-DD-YYYY' and percentage of errors
    print "\nDays in which more than 1% of requests lead to errors:\n"
    list = 0
    for row in rows:
        list += 1
        date = row[:][0]
        percent = row[:][1]
        print format(list, '<2'), date, ' - ', percent, '% Errors'
    print
    db.close()


def assignment():
    question1()
    question2()
    question3()


assignment()
