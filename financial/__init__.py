#!/usr/bin/python
from decimal import *

getcontext().prec = 4

DEFAULT_PRICES_LIST = [("FR", Decimal("3.11")), ("CF", Decimal("11.23")), ("SR", Decimal("5.00"))]


class MarketingRule:
	def __init__(self):
		pass

	def apply(self, total, checque, prices_list):
		return total


class BuyOneGetOneForFree(MarketingRule):
	LABEL = "FR"

	def __init__(self, item_label = LABEL):
		MarketingRule.__init__(self)
		self.label = item_label

	def apply(self, total, checque, prices_list):
		count = checque.items.get(self.label, 0)
		if count > 1:
			if count % 2 == 0:
				return total - (count / 2) * prices_list.get(self.label)
			else:
				return total - ((count - 1) / 2) * prices_list.get(self.label)
		else:
			return total


class FewOrMore(MarketingRule):
	LABEL = "SR"
	THRESHOLD = 3
	DISCOUNT = Decimal("0.5")

	def __init__(self, item_label = LABEL, discount = DISCOUNT, threshold = THRESHOLD):
		MarketingRule.__init__(self)
		self.label = item_label
		self.threshold = threshold
		self.discount = discount

	def apply(self, total, checque, prices_list):
		count = checque.items.get(self.label, 0)
		if count >= self.threshold:
			return total - count * self.discount
		else:
			return total


DEFAULT_RULES = [BuyOneGetOneForFree(), FewOrMore()]


class Checque:
	def __init__(self, items = ""):
		self.items = self.from_string(items)

	def from_string(self, value):
		data = value.split(" ")
		data = dict((name, Decimal(data.count(name))) for name in data)
		return data
		

class Checkout:
	def __init__(self, rules = DEFAULT_RULES):
		self.rules = rules
		
	def total(self, cheque):
		result = 0
		for item in cheque.items:
			result += self.prices_list.get(item) * cheque.items.get(item)
		return result

	def calculate(self, cheque):
		total = self.total(cheque)
		for rule in self.rules:
			total = rule.apply(total, cheque, self.prices_list)
		return total

	def set_prices(self, value = DEFAULT_PRICES_LIST):
		self.prices_list = dict(value)
		return self


if __name__ == "__main__":
	assert Checque("FR FR").items.get("FR") == 2
	assert Checque("SR SR FR SR").items.get("FR") == 1
	assert Checque("SR SR FR SR").items.get("SR") == 3
	assert Checque("FR SR FR FR CF").items.get("FR") == 3
	assert Checque("FR SR FR FR CF").items.get("CF") == 1
	assert Checque("FR SR FR FR CF").items.get("SR") == 1
	assert Checkout(DEFAULT_RULES).set_prices(DEFAULT_PRICES_LIST).calculate(Checque("FR FR")) == Decimal("3.11")
	assert Checkout(DEFAULT_RULES).set_prices(DEFAULT_PRICES_LIST).calculate(Checque("SR SR FR SR")) == Decimal("16.61")
	assert Checkout(DEFAULT_RULES).set_prices(DEFAULT_PRICES_LIST).calculate(Checque("FR SR FR FR CF")) == Decimal("22.45")