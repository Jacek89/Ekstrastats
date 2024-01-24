# Ekstrastats - Polish Ekstraklasa Statistics Web App
This web application is driven by an educational motive, centering on the statistics of the Polish Ekstraklasa. The fundamental idea is to visualize the most complex statistics possible through calculations based on an intentionally minimalistic database structure. This approach aims to demonstrate the effectiveness of extracting and presenting comprehensive insights with minimal data complexity.


<a href="http://ekstrastats.onrender.com/">Link to deployed web app</a> (Can take a very long time to load for the first time)

## Additional Goals:
### Enhancing Security
Throughout the application's development, my interest led me to explore the realm of security. I familiarized myself with potential vulnerabilities that hackers might exploit, such as XSS and SQL Injection, and learned essential countermeasures. Implementing numerous recommendations from <a href="https://observatory.mozilla.org/">Mozilla Observatory</a>, I subjected the application to thorough scans using the tool, achieving an outstanding A+ score. This proactive approach ensures robust security against potential threats.

![Mozilla Observatory Score](https://i.imgur.com/zfBzyp2.png)


### Optimizing Performance
Another key objective is to optimize the application, aiming for short loading times of individual pages by minimizing database calls. To accomplish this, I delved into the intricacies of crafting efficient queries in Django ORM, exploring non-standard solutions when necessary. The use of Django Debug Toolbar became instrumental in monitoring both loading speed and the number of database queries.

Prior to the optimization efforts, the program made over 400 database hits when calculating the table. Through adjustments, I managed to bring this number down to 6, resulting in a remarkable fivefold reduction in loading time.

### Testing for Reliability

One of the key objectives in the development is comprehensive testing of web application. I aspire to verify every functionality and as many as possible statistical features. To achieve this, I use meticulously crafted models from the Factories library that perfectly represent real-world scenarios. This approach makes it much faster to introduce new functionality without worrying about the proper operation of previous ones. 

## Features

