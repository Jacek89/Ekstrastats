# Ekstrastats - Polish Ekstraklasa Statistics Web App
This web application is driven by an educational motive, centering on the statistics of the Polish Ekstraklasa. The fundamental idea is to visualize the most complex statistics possible through calculations based on an intentionally minimalistic database structure. This approach aims to demonstrate the effectiveness of extracting and presenting comprehensive insights with minimal data complexity.


<a href="http://ekstrastats.onrender.com/">Link to deployed web app</a> (Initial loading may take longer because the servers need to wake up from standby mode)

## Additional Goals:
### Enhancing Security
Throughout the application's development, my interest led me to explore the realm of security. I familiarized myself with potential vulnerabilities that hackers might exploit, such as XSS and SQL Injection, and learned essential countermeasures. Implementing numerous recommendations from <a href="https://observatory.mozilla.org/">Mozilla Observatory</a>, I subjected the application to thorough scans using the tool, achieving an outstanding A+ score. This proactive approach ensures robust security against potential threats.

![Mozilla Observatory Score](https://i.imgur.com/zfBzyp2.png)


### Optimizing Performance
Another key objective is to optimize the application, aiming for short loading times of individual pages by minimizing database calls. To accomplish this, I delved into the intricacies of crafting efficient queries in Django ORM, exploring non-standard solutions when necessary. The use of Django Debug Toolbar became instrumental in monitoring both loading speed and the number of database queries.

Prior to the optimization efforts, the program made over 400 database hits when calculating the table. Through adjustments, I managed to bring this number down to 6, resulting in a remarkable fivefold reduction in loading time.

### Testing for Reliability

One of the key objectives in the development is comprehensive testing of web application. I aspire to verify every functionality and as many as possible statistical features. To achieve this, I use meticulously crafted models from the Factories library that perfectly represent real-world scenarios. This approach makes it much faster to introduce new functionality without worrying about the proper operation of previous ones. 

## Features:

### Calculated Statistics

Comprehensive statistical analysis generated from the database for clubs, entire league, or specific rounds. This feature provides valuable insights into team performances, player statistics, and league trends.

### League Table

The league table offers users the flexibility to filter data based on specific dates. Its dynamic functionality comes from the direct calculation of match results stored in the database. Using recursive functions, I designed the table to generate smaller tables of direct match results. This complex process provides an accurate determination of each team's position in the league.

### Analysis

The data analysis section uses fundamental machine learning algorithms or classical data analysis techniques for prediction or dynamic data visualization, directly fetching data from the database. At present, it offers one option: predicting the outcome of selected team matches and distributing the probability of specific match results based on the Poisson distribution.
