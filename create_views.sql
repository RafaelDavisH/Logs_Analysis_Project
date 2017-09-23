
--
--  Views for newsqueries.py
--

CREATE VIEW articleviews AS
    SELECT articles.title, count(*) AS views
    FROM articles, log
    WHERE '/article/' || articles.slug = log.path
    GROUP BY articles.title
    ORDER BY views DESC;

CREATE VIEW totalviews AS
    SELECT articles.author, articleviews.views
    FROM articles, articleviews
    WHERE articles.title = articleviews.title
    ORDER BY articles.author;

CREATE VIEW errorsday AS
    SELECT log.time::date as date, count(*) AS errors
    FROM log
    WHERE log.status = '404 NOT FOUND'
    GROUP BY date
    ORDER BY errors DESC;

CREATE VIEW requestday AS
    SELECT log.time::date as date, count(*) as requests
    FROM log
    GROUP BY date
    ORDER BY requests DESC;

CREATE VIEW leaderrors AS
    SELECT to_char(errorspercent.date, 'FMMonth FMDDth, YYYY') AS date,
    (errorsday.errors / requestday.requests::float * 100.0) AS percentage
    FROM errorsday, requestday
    WHERE errorsday.date = requestday.date
    ORDER BY percentage DESC;
