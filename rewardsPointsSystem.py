"""

PROBLEM: Management needs to know how many of each item they are selling each 
day and what each customer’s current reward points balance is.

Design a system that parses the log file and:
1) Calculates the reward points for each customer
2) Generates purchase counts for each item sold during the day

Here are some considerations for the rewards system you want to create:

- For each purchase, a customer can spend a certain amount of reward points for their purchase.
- Some customers come to the store multiple times per day.
- Customers earn 1 reward point for every 18 dollars spent, unless they spend more than $250 per day, in which case they earn 1 reward point for every 17 dollars spent. These reward points are given to the customers at the **end** of each day, not immediately after the purchase.
- For each LogEntry, we want to keep track of:
    - Customer ID
    - Number of reward points used for that purchase
    - List of items purchased and their prices

There can also be malformed logs in which any of the three properties in the LogEntry are 'None'.
If this is the case, please address them in the following ways:
- If there is no customer ID, do not count the rewards points. Instead, only calculate the purchase counts for the items
- If there is no rewards points specified, assume rewards points = 0
- If there is no list of items purchased, then this is an error in the system. Please add this LogEntry to a error log (a list of LogEntry called 'error')

Example- this is written in casual terms, and must be modified to actual data structures
	Items:
		- Banana- $50
		- Apple- $100
	Log Entries:
		- Customer 1 purchased 2 bananas and 1 apple; he used 100 rewards points
		- Customer 2 purchased 1 banana and 1 apple; she used 0 rewards points
		- Customer 1 purchased 1 banana; he used 0 rewards points

"""
from collections import defaultdict

class Item:
  def __init__(self, item_id, item_price):
    self.item_id = item_id 
    self.item_price = item_price

class RewardsSystem: 
  REWARDS_RATIO_BELOW = 18
  REWARDS_RATIO_ABOVE = 17 
  REWARDS_CUTOFF = 250

  def __init__(self):
    self.rewards_points = defaultdict(int)
    self.items_purchased = defaultdict(int)
    self.error_log = [] 

  def process_log(self, log):
    amount_spent = defaultdict(int)

    for log_entry in log:
      customer_id = log_entry[0]
      reward_points_used = log_entry[1]
      items_purchased = log_entry[2]

      if not customer_id:
        if (len(items_purchased) == 0):
          self.error_log = self.error_log.append(log_entry) 
          raise ValueError('Items purchased were not recorded.')

      else:
        self.rewards_points[customer_id] -= reward_points_used
        total_spent = 0
        for item in items_purchased:
          total_spent += item.item_id * item.item_price

        amount_spent[customer_id] += total_spent

      # Update items sold
      for purchase in items_purchased:
        self.items_purchased[purchase.item_id] += 1 

    # At end of day, award reward points back to customers based on how much they spent
    for customer_id in amount_spent:
      # Calculate rewards points received
      rewards_points = amount_spent[customer_id] // RewardsSystem.REWARDS_RATIO_BELOW
      if amount_spent > RewardsSystem.REWARDS_CUTOFF:
        rewards_points =  amount_spent[customer_id] // RewardsSystem.REWARDS_RATIO_ABOVE 
      # Update customer rewards points
      self.rewards_points[customer_id] += rewards_points
