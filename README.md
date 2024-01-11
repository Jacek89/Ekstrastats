# Ekstrastats
Web application presenting polish ekstraklasa statistics. The motivation for creating this application is educational reason. 
The main idea of this application is to visualize as complex as possible statistics using calculations based on as minimalistic as possible database. 

<a href="http://ekstrastats.onrender.com/">Link to deployed web app</a>

## Additional Goals:
### Security
During the development of the application, I became interested in the topic. I learned about the ways in which hackers can break security of application or its users (XSS, SQL Injection) and basics about how to counteract it.
I implemented many of the recommendations from <a href="https://observatory.mozilla.org/">Mozilla Observatory</a> getting an A+ score after a scan through the tool.

![Mozilla Observatory Score](https://i.imgur.com/zfBzyp2.png)


### Optimization
Another stated goal is to optimize the application so that the loading time of individual pages is short by reducing calls to the database. 
To achieve this I had to delve into the topic of how to make correct queries in Django ORM, also using non-standard solutions. I use Django Debug Toolbar To monitor loading speed and number of database queries. Before implementing the optimization, when calculating the table, the program hit the database more than 400 times. I was able to go down to 22, this resulted in reducing the loading time by 5 times. 

## Features
