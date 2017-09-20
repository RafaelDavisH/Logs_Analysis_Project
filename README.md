# Newsqueries.py

**Newsqueries** is a reporting tool that uses information from a
newspaper site's database to discover what kind of articles the site's readers
like. **Newsqueries** will print out reports in plain text based on the data in the database. This program is a python program using the `psycopg2` module to connect to the database.

## Data

You will need `newsdata.sql` to be stored into the `vagrant` directory, which is shared with the Virtual Machine.

To load the the datam `cd` into the `vagrant` directory and use the command `psql -d news -f newsdata.sql`.

## Virtual Machine

:point_right: *This project makes use of a Linux-based virtual machine (VM) - `vagrant`. The VM needs to be online for this program to run.*

To connect to the database from your command line, run:

```
vagrant up
```
and to log into it with
```
vagrant ssh
```

To run **newsqueries** from your command line:

```
./newsqueries.py
```
or
```
python newsqueries.py
```

## Questions

**Newsqueries** will answer 3 important questions to get this reports.

1. What are the most popular three articles of all time?

2. Who are the most popular article authors of all time?

3. On which days did more than 1% of requests lead to errors?

## Views

### View for question #1
In order to answer the first question two tables need to join: articles and
log. The **articles** table has a **slug** column almost identical as **log.path**. In
order to join both tables they must have a similar content.

#### Articlespath

`'/article/'` will add the extra piece that **articles.slug** needs to match **log.path**.<br>
**articles,slug** column `bad-things-gone` and **log.path** column `/article/bad-things-gone/`
```
create view articlespath as
  select '/article/'::text || articles.slug
  as slugpath, articles.title from articles;
```

### Views for question #2

#### Articleviews

Previous question provided important information, total views per article, to answer question 2. By creating a view without a `..limit 3` all the views for each article belonging to an author can be added, then order by most to least views.
```
create view articleviews as
  select articlespath.title,count(*) as views
  from articlespath, log
  where articlespath.slugpath = log.path
  group by articlespath.title
  order by views desc;
```
#### Totalviews

**Totalviews** brings articleviews and articles tables together to create a table with the authors' id and the total views per article ordered by authors' id.

```
create view totalviews as
    select articles.author,
    articleviews.views
    from articles,
    articleviews
    where articles.title = articleviews.title
    order by articles.author;
```

### Views for question #3

#### Errorsdate

**Errordate** counts all errors per day and groups them by date and order by errors most to least errors.
```
create view errorsdate as
   select log.time::date as date, log.status, count(*) as errors
   from log
   where log.status = '404 NOT FOUND'
   group by date, log.status
   order by errors desc;
```

#### Totalerrors

**Totalerrors** adds all days' errors to get a total of errors.  This total will help with the equation to get the percentage of errors per day.

```
create view Totalerrors as
   select sum(errorsdate.errors) as sum
   from errorsdate;
```
