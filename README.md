# FANTOIR_scan

FANTOIR is the official database of public roads in France.

The idea behind this Python script to see how recurrent are certain names given to French streets, avenues, squares, etc.; in order to reveal the importance of certain personnalities in France (National ones like De Gaulle or Aristide Briand, and foreign ones like Winston Churchill or Pablo Neruda).

To do so, the script:
- counts names without paying attention to the type of road (avenue, street, square, etc.);
- evaluates whether the name is a common word or a proper noun;
- scraps city population data from the French National Statistic Institute (INSEE)
- attribute a score to each name according to number of appearances in FANTOIR and the population of the cities where they appear (total population exposed)

As no data on the length of the streets could be found, no weighting of the score according to the actual size of the road could be done.
