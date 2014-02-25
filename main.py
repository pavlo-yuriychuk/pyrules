#!/usr/bin/python

from financial import Checkout, Checque


def main():
	print "FR FR", round(Checkout().set_prices().calculate(Checque("FR FR")), 2)
	print "SR SR FR SR", round(Checkout().set_prices().calculate(Checque("SR SR FR SR")), 2)
	print "FR SR FR FR CF", round(Checkout().set_prices().calculate(Checque("FR SR FR FR CF")), 2)
	
if __name__ == "__main__":
	main()
	