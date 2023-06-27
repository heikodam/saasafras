# Revenue Calculator Script

This Python script calculates the maximum possible revenue given the number of months and the size of the team. 

## Requirements

- Python 3.x

## How to Run

This script accepts the following command line arguments:

-t, --type : The type of revenue calculation. Options include "normal" and "am_last_month".
If this argument is not provided, "normal" is used by default.
-m, --months : The number of months for which the revenue should be calculated. This argument is required.
-s, --team_size : The total team size. This argument is required.


Here is an example of how to run the script:

`python your_script_name.py -t normal -m 3 -s 10`


In this example, the script will calculate the maximum possible revenue in the last month for a team of size 10 over 3 months, using the "normal" calculation type.


