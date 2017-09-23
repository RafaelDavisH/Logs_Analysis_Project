# Newsqueries.py

**Newsqueries** is a reporting tool that uses information from a
newspaper site's database to discover what kind of articles the site's readers
like. **Newsqueries** will print out reports in plain text based on the data in the database. This program is a python program using the `psycopg2` module to connect to the database.

## Questions

**Newsqueries** will answer 3 important questions to get these reports.

1. What are the most popular three articles of all time?

2. Who are the most popular article authors of all time?

3. On which days did more than 1% of requests lead to errors?

## Requirements

1. [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
2. [Vagrant](https://www.vagrantup.com/)
3. [`newsdata.sql`](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
4. `create_views.sql`
5. [`newsqueries.py`](https://github.com/RafaelDavisH/Logs_Analysis_Project/raw/master/newsqueries.py)

## [Virtual Machine][1]

You'll need database software (provided by a Linux virtual machine) and the data to analyze. The VM is a Linux server system that runs on top of your own computer.  We're using tools called [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads) to install and manage the VM. You'll need to install these to run `newsqueries.py`

## [Use a Terminal][1]

You'll need to be using a Unix-style terminal on your computer. If you are using a **Mac or Linux** system, your regular terminal program will do just fine.  On **Windows**, we recommend using the **Git Bash** terminal that comes with the Git software.

## [Install VirtualBox][1]

**VirtualBox** is the software that actually runs the virtual machine. Install the *platform package* for your operation system - [click Here](https://www.virtualbox.org/wiki/Downloads).
You don't need the extension pack or the SDK. You do not need to launch **VirtualBox** after installing it; Vagrant will do that.

**Ubuntu users:** If you are running Ubuntu 14.94, install VirtualBox using the Ubuntu Software Center instead. Due to a reported bug, installing VirtualBox from the site may uninstall other software you need.

## [Install Vagrant][1]

**Vagrant** is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. [Download it from vagrantup.com](https://www.vagrantup.com/). Install the version for your operating system.

**Windows users:** The installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.

```shell
$ vagrant --version
vagrant 1.8.5
$
```
*if Vagrant is successfully installed, you will be able to run `vagrant --version` in your terminal to see the version number. The shell prompt in your terminal may differ. Here, the `$` sign is the shell prompt.*

## [Download the VM configuration][1]

There are couple of different ways you can download the VM configuration.

You can download and unzip this file: [FSND-Virtual-Machine.zip](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip) This will give you a directory called **FSND-Virtual-Machine**. It may be located inside your **Dowdloads** folder.

Alternately, you can use Github to fork and clone the repository [https://githhub.com/udacity/fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm)

Either way, you will end up with a new directory containing the VM files. Change to this directory in your terminal with `cd`. Inside, you will find another directory called **vagrant**. Change directory to the **vagrant** directory:

![alt text](https://d17h27t6h515a5.cloudfront.net/topher/2016/December/58487f12_screen-shot-2016-12-07-at-13.28.31/screen-shot-2016-12-07-at-13.28.31.png)

*Navigating to the FSND-Virtual-Machine directory and listing the files in it. This picture was taken on a Mac, but the commands will look the same on Git Bash on Windows.*

## [Start The Virtual Machine][1]

From your terminal, the **vagrant** subdirectory, run the command `vagrant up`. This will cause Vagrant to download the Linux operating system and install it. This may take quite a while (many minutes) depending on how fast your internet connection is.

![alt text](https://d17h27t6h515a5.cloudfront.net/topher/2016/December/58488603_screen-shot-2016-12-07-at-13.57.50/screen-shot-2016-12-07-at-13.57.50.png)

*Starting the Ubuntu Linux installation with `vagrant up`. This screenshot shows just the beginning of many pages of output in a lot of colors.*

When `vagrant up` is finished running, you will get your shell prompt back. At this point, you can run `vagrant ssh` to log in to your newly installed Linux VM!

![alt text](https://d17h27t6h515a5.cloudfront.net/topher/2016/December/58488962_screen-shot-2016-12-07-at-14.12.29/screen-shot-2016-12-07-at-14.12.29.png)

*Logging into the Linux VM with `vagrant ssh`.*

### [Wow, That Worked!][1]

If you've gotten logged into your Linux VM, congratulations. If not, take a look at the **Troubleshooting** section below.

### [The Files][1]

Inside the VM, change directory to `/vagrant` and look around with `ls`.

The files you see here are the same as the ones in the `vagrant` subdirectory on your computer (where you started Vagrant from). Any file you create in one will be automatically shared to the other. This means that you can edit code in your favorite text editor, and run it inside the VM.

Files in the VM's `/vagrant` directory are shared with the `vagrant` folder on your computer. But other data inside the VM is not. For instance, the PostgreSQL database itself lives only inside the VM.

### [Running The Database][1]

The PostgreSQL database server will automatically be started inside the VM. You can use the `psql` command-line tool to access it and run SQL statements:

![atl text](https://d17h27t6h515a5.cloudfront.net/topher/2016/December/58489186_screen-shot-2016-12-07-at-14.46.25/screen-shot-2016-12-07-at-14.46.25.png)

*Running psql, the PostgreSQL command interface, inside the VM.*

### [Logging Out And In][1]

If you type `exit` (or `Ctrl-D`) at the shell prompt inside the VM, you will be logged out, and put back into your host computer's shell. To log back in, make sure you're in the same directory and type `vagrant ssh` again.

If you reboot your computer, you will need to run `vagrant up` to restart the VM.

## Import the `Views`.

A `sql` script has been created named [`create_views.sql`]() to facilitate you with the views necessary for `newsqueries.py` run properly. You can import the views from the terminal by typing: `psql -d news -f create_views.sql`



To run **newsqueries** from your command line:

```
./newsqueries.py
```
or
```
python newsqueries.py
```

## Views

### View for question #1

#### Articleviews

In order to answer the first question two tables need to join: articles and
log. The **articles** table has a **slug** column almost identical as **log.path**. In order to join both tables they must have a similar content.

```sql
CREATE VIEW articleviews AS
    SELECT articles.title, count(*) AS views
    FROM articles, log
    WHERE '/article/' || articles.slug = log.path
    GROUP BY articles.title
    ORDER BY views DESC;
```

### Views for question #2

#### Totalviews

**Totalviews** brings articleviews and articles tables together to create a table with the authors' id and the total views per article ordered by authors' id.

```sql
CREATE VIEW totalviews AS
    SELECT articles.author, articleviews.views
    FROM articles, articleviews
    WHERE articles.title = articleviews.title
    ORDER BY articles.author;
```

### Views for question #3

#### Errorsday

**Errorsdate** counts all errors per day and groups them by date and order by errors most to least errors.

```sql
CREATE VIEW errorsday AS
    SELECT log.time::date as date, count(*) AS errors
    FROM log
    WHERE log.status = '404 NOT FOUND'
    GROUP BY date
    ORDER BY errors DESC;
```

#### Requestday

**Requestday** counts all requests per day and groups them by date order by errors most to least requests.

```sql
CREATE VIEW requestday AS
    SELECT log.time::date as date, count(*) as requests
    FROM log
    GROUP BY date
    ORDER BY requests DESC;
```

#### Leaderrors

**Leaderrors** adjust the date format to MON-DD-YYYY and gets the percentage of errors per day.

```sql
CREATE VIEW leaderrors AS
    SELECT to_char(errorspercent.date, 'MON DD, YYYY') AS date,
    (errorsday.errors / requestday.requests::float * 100.0) AS percentage
    FROM errorsday, requestday
    WHERE errorsday.date = requestday.date
    ORDER BY percentage DESC;
```

## [Troubleshooting][1]

#### I'm not sure if it worked.

If you can type `vagrant ssh` and log into your VM, then it worked! It's normal for the `vagrant up` process to display a lot of text in many colors, including sometimes scary-looking messages in red, green, and purple. If you get your shell prompt back at the end, and you can log in, it should be OK.

#### `vagrant up` is taking a long time. Why?

Because it's downloading a whole Linux operating system from the Internet.

#### I'm on Windows and getting an error about virtualization.

Sometimes other virtualization programs such as Docker or Hyper-V can interfere with VirtualBox. Try shutting these other programs down first.

In addition, some Windows PCs have settings in the BIOS or UEFI (firmware) or in the operating system that disable the use of virtualization. To change this, you may need to reboot your computer and access the firmware settings. [A web search](https://www.google.com/search?q=enable%20virtualization%20windows%2010) can help you find the settings for your computer and operating system. Unfortunately there are so many different versions of Windows and PCs that we can't offer a simple guide to doing this.

#### Why are we using a VM? It seems complicated.

It is complicated. In this case, the point of it is to be able to offer the same software (Linux and PostgreSQL) regardless of what kind of computer you're running on.

#### I got some other error message.

If you're getting a specific textual error message, try looking it up on your favorite search engine. If that doesn't help, take a screenshot and post it to the discussion forums, along with as much detail as you can provide about the process you went through to get there.

#### If all else fails, try an older version.

Udacity mentors have noticed that some newer versions of Vagrant don't work on all operating systems. Version 1.9.2 is reported to be stabler on some systems, and version 1.9.1 is the supported version on Ubuntu 17.04. You can download older versions of Vagrant from [the Vagrant releases index](https://releases.hashicorp.com/vagrant/).

*All the procedures given above to install the VirtualBox, Vagrant and Troubleshooting are from Udacity's 'Intro to Programming Nanodegree Program'*
[1]: https://classroom.udacity.com/nanodegrees/nd000/parts/b910112d-b5c0-4bfe-adca-6425b137ed12/modules/a3a0987f-fc76-4d14-a759-b2652d06ab2b/lessons/303a271d-bc69-4eba-ae38-e9875f841604/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0
