For the df variables for init site. when to update it? and how ? It's is possible for variable in the call backs but not the init variables
To address this : we can create a files that do the update and peordically update the variables we need




# Do this https://dash.plot.ly/performance
# https://github.com/plotly/dash-redis-celery-periodic-updates
About the global data
- Don't use global data and update it, Flask run multiple threads, u run update on 1 threads it will not update on others thread
- Global data update will be expensive computation


# NOTE TO IMPROVE DATA FLOW
1. Use celery to init data peoridcally
2. Don't use global data in init() Use return instead
