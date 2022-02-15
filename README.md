#Portfolio Rebalancer

---

###Objective:

The purpose of this project is to make my investment decisions a bit easier 
by creating custom visualizations and data representations to help me 
understand how each of my positions are performing.

At it's core, this program is meant to make re-balancing my portfolio easier
by automating the necessary calculations. But there's other features I'd like
to include. I have found that my brokerage's app presents a very high-level 
view of my portfolio and I would like to see more fine detail. I would also 
like to have some tools to easily compare decisions that I've made concerning 
my investments. A suite of research tools, such as a Monte Carlo simulation 
engine, random walk generator, etc. would be very useful for considering an 
investment. There's potential to create my own Bloomberg terminal. 

Some very advanced features that I'd like to include are a NLP engine capable 
of taking a question as input and searching the academic literature for information
about that topic, and possibly even suggesting a course of action. Another 
idea is to represent a portfolio as a visual tree, decisions as branches. Here
I may be able to use Git as a template for tracking the changes. 

###Implementation

The class structure of the program is as follows: Portfolio objects are composed 
of Position objects, which are themselves composed of Transaction objects. All 
the data to create these objects are stored in a SQLite database locally. 

Initially the yFinance Python library will be used to fetch current and 
historical stock prices and metrics. Hopefully one day I can get access to a
professional research database like the CRSP database.

GUI design will be decided at a later time.

###Challeneges 

The class structure gave me the most difficulty. I kept starting out with the  
idea that the smallest unit should be a share of a stock because that's how 
the stock market is actually organized. But somewhere along the way I realized
that, for my purpose, actual purchase or sell events are really all that is
needed. The information is readily available to download via my brokerage's 
API and this structure eliminates the need for thousands of 'share' objects 
to be created. In thinking about this project I got my first experience in 
software design decisions and I really enjoyed the process of coming to this
conclusion. 

In preparation for writing this application I had to learn SQL, SQLite, the 
sqlite3 and openpyxl Python libraries, database architecture, and evetually 
SQLalchemy in order to use its ORM. All of this was great experience as there 
were a number of nuances to all these elements that I had to learn to navigate
in order to get them to work together. 