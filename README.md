# saved-parser
Reddit saved content parser

saved-parser parses and organizes your reddit saved content
      
## Usage: 
  * Fill out the dict in catagories-stub.py
   ..* Each key is a different catagory. The value is 
   ... a list of subreddits belonging to that catagory.
      
  * Run catagories-stub.py, it will store the dict in a file `catagories.pickle`
      
  * Run saved-parser.py, it will load the catagories dict and use it to organize your saved content
      
  * For each catagory, saved-parser will create a file of the same name with a entry for each saved
  ..item belonging to that catagory.     
