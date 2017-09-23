#!/usr/bin/env python2.7

import psycopg2
from pprint import pprint


def execute_query(query):
    """execute_query takes an SQL query as a parameter. Executes the query
    and returns the results as a list of tuples.
    args:
        query - an SQL query statement to be executed.

    returns:
        A list of tuples containig the results of the query.
    """
    try:
        db = psycopg2.connect("dbname=news")
        c = db.cursor()
        c.execute(query)
        return c.fetchall()
        db.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def top_articles():
    """ Return the top 3 most popular articles of all time with views total """
    query = """SELECT title, views
               FROM articleviews
               LIMIT 3; """

    rows = execute_query(query)

    # Return each top article with the amount of views
    print "\nThe top 3 most popular articles of all time:\n"

    for list, (title, views) in enumerate(rows, 1):
        print ('{}. \"{}\" - {} Views'.format(list, title, views))
    print


def top_articles_authors():
    """ Return the most popular article authors of all time """
    query = """SELECT authors.name, sum(views) AS views
               FROM authors, totalviews
               WHERE authors.id = totalviews.author
               GROUP BY authors.name
               ORDER BY views DESC;"""

    rows = execute_query(query)

    # Return each top article author witht the amount of total views
    print "\nThe top most popular article authors of all time:\n"

    for list, row in enumerate(rows, 1):
        author = row[:][0]
        views = row[:][1]
        print list, format(author, '<22'), ' - ', format(views, '>6'),\
            'Total Views'
    print


def lead_errors():
    """ Return the days in which more than 1'%' lead to errors"""
    query = """SELECT date, percentage
               FROM leaderrors
               WHERE percentage > 1.0;"""

    rows = execute_query(query)

    # Return each row with date 'MON-DD-YYYY' and percentage of errors
    print "\nDays in which more than 1 percent of requests lead to errors:\n"
    list = 0
    for list, row in enumerate(rows, 1):
        date = row[0]
        percent = row[1]
        print format(list, '<2'), date, ' - ', round(percent, 2), '% Errors'
    print


def assignment():
    top_articles()
    top_articles_authors()
    lead_errors()


if __name__ == '__main__':
    assignment()
