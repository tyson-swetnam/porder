# Order state check

This tool allows you to get the list of orders based on the states and based on the start and end dates of orders. For example if you want to find out all orders that failed within the week you can use this tool to check that.

<b>
```
usage: porder ostate [-h] [--state STATE] [--start START] [--end END]
                     [--limit LIMIT]

optional arguments:
  -h, --help     show this help message and exit
  --state STATE  choose state between queued| running | success | failed |
                 partial
  --start START  start date in format YYYY-MM-DD
  --end END      end date in format YYYY-MM-DD

Optional named arguments:
  --limit LIMIT  Limit the maximum table size
```
</b>

The setup to check failed orders would be for example the following, You can place a limit on the number of orders to get by using --limit


![porder_ostate](https://user-images.githubusercontent.com/6677629/69604178-ad270180-0fea-11ea-8d84-34685f917ee5.gif)
