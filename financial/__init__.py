class MarketingRule:
	def __init__(self):
		pass

	def apply(self, total, checque, prices_list):
		return cheque

class Checque:
	def __init__(self, items = ""):
		self.items = self.from_string(items)

	def from_string(self, value):
		data = value.split(" ")
		return dict((name, data.count(name)) for name in data)
		
class CashDesk:
	def __init__(self, rules, prices_list):
		self.rules = rules
		self.prices_list = dict(prices_list)

	def calculate(self, cheque):
		total = reduce(lambda acc, x: acc + y.price, cheque.items, 0)
		for rule in self.rules:
			total = rule.apply(total, cheque, self.prices_list)
		return total

DEFAULT_RULES = []
DEFAULT_PRICES_LIST = [("FR", 3.11), ("CF", 11.23), ("SR", 5.00)]

if __name__ == "__main__":
	assert CashDesk(DEFAULT_RULES, DEFAULT_PRICES_LIST).calculate(Checque("FR FR")) == 3.11
	assert CashDesk(DEFAULT_RULES, DEFAULT_PRICES_LIST).calculate(Checque("SR SR FR SR")) == 16.61
	assert CashDesk(DEFAULT_RULES, DEFAULT_PRICES_LIST).calculate(Checque("FR SR FR FR CF")) == 22.45