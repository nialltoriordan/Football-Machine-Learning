I haven't updated this project in a while, though have been working on different elements of it. This is an informal overview/log. 

The goal of the project is to predict the result of a football league match with a 90% or better accuracy.  In order for this to be useful, I want to be able to predict at least 5% of matches.

I plan on doing this project badly; rather than research what machine learning approaches have shown success in this area and build on their work, I'm going to try to apply my own ideas first, examine how they perform, and compare them to similar approaches by other people.

Currently my best results seem to come from using a 'power rating' system (see powerrating.txt).  A large difference in power rating (2.0 or above) gives me around an 82% success rate for around 70 matches out of 1,232.  This breaks down as 86% for home matches and 66% for away matches.  If I add a +1 'handicap', I can get my success rate up to 92%, but that doesn't satisfy the goals of the project.

Adding more features (see formrating.txt) based on form and goal scores, doesn't initially seem to make much difference; teams with really low form and goal scoring ratings but a high power rating seem to have the same success rate as above.

I then generated many more features to feed into different machine learning algorithms.  I added league positions, goals for and against, and goal difference, and also generated half-time and home and away league stats.  Feature selection weeded out most of these, including all the half-time stats.  Best results seem to be achieved using around 10 features, the most important 2 being 'Home Rating' and 'Home Goal Difference'.

For testing different machine learning approaches, I used a modified version of findfeatures.py.  Using a Linear Support Vector classifier with SelectKBest features, I can get an accuracy of 57% More relevant here though is the precision score; the amount of predicted wins that were actually successful.  This currently stands at 68%.  I've been training with 70% of the 2016/17/18 data, and predicting with the remaining 30%.  If I use the trained classifier on the 2018/19 data, I get accuracy and precision scores that are about 10% worse.

At this point there's a few different things I'd like to pursue with my existing data.  For example I'd like to investigate my false positives and see if there's anything common/frequent (maybe days since last match) to be found.  For this I'd also have to add data from non-league matches, so would like to try to find larger data sets.  I could also generate data for a lot of my current features for many more years (usually back to 93/94) to give my classifiers more training data.  In the next few days I'm doing an operating system re-install.  When I'm back up and running I think it's time to start researching what other systems people have used.


