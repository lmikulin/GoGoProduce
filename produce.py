import promo_functions
import xml.etree.ElementTree as Tree

#read the inventory data file
tree = Tree.parse('inventory.xml')
inventory = tree.getroot()

def populatePromoDict():
	global promo_dict
	promo_dict = {}
	for item in item_names:
		promo_nodes = inventory.findall("./item[@name='%s']/promo" % item)
		if (len(promo_nodes) > 0):
			promo_dict[item] = []
			for node in promo_nodes:
				pass
	

def getRegularCostOfItem(item):
	price_node = inventory.find("./item[@name='%s']/price" % item)
	try:
		cost = float(price_node.text)
	except:
		# not found, so it must be free!
		cost = 0
	return cost

def getPriceAndPromoTuple(item, nth):
	cost = getRegularCostOfItem(item)
	deal = ""
	
	# check for promo
	if (item in promo_dict):
		for promo in promo_dict[item]:
			if (promo.promoDoesApply(item, nth)):
				cost += promo.discount(item, nth)
				deal = promo.name

	return (cost, deal)
		
def printReceipt(purchase):
	total = 0
	print '{:<20}'.format('Purchase'), '{:>8}'.format('Price'), '{:>8}'.format('Total'), "Promotion"
	print '-'*20, '{:>8}'.format('-'*5), '{:>8}'.format('-'*5), '-'*9
	# tuple has (item name, item cost, item promo)
	for tuple in purchase:
		total += tuple[1]
		print '{:.<20}'.format(tuple[0]), '{:>8}'.format('{:.2f}'.format(tuple[1])), '{:>8}'.format('{:.2f}'.format(total)), tuple[2]
	
	print "\nTotal: $", '{0:.2f}'.format(total)
        
class Promo:
	def __init__(self, item_type, this_many, promo_name, discount=0, expr=None):
		self.item = item_type
		self.nth = this_many
		self.name = promo_name
		self.save = discount
		self.func = expr
		
	def promoDoesApply(self, item, num):
		return num % self.nth == 0

	def discount(self, item, num):
		cost = getRegularCostOfItem( item)
		discount = 0

		if (self.promoDoesApply(item, num)):
			#apply the promo
			if (self.save > 0):
				discount = - self.save
			elif (self.func != None):
				try:
					# all promo functions are expected to have this argument list: item, cost, nth and return the new promo cost
					discount = self.func(self.item, cost, self.nth)
				except:
					#it didn't work, leave as is
					pass
		return discount

promo_dict = {
	"plum": [Promo("plum", 3, "Buy TWO Get one 1/2 off", 0, promo_functions.buyNGetOneHalfOff)],
	"pear": [],
	"apple": [Promo("apple", 4, "Buy three getone Free!", 0, promo_functions.buyNGetOneFree)], 
	"mango": [Promo("mango", 2, "Save 40c on two", 0.4, None)] }

# make a list of the produce inventory item names
item_names = []
nodes = inventory.findall("./item[@name]")
for node in nodes:
	item_names.append( node.attrib['name'])
num_items = len(item_names)

# print the inventory choices list
for index, item in enumerate(item_names):
	print index, ": ", item
print "Press any other key to complete your transaction"

purchased = []
session = True

# total spent
total = 0
# number of items purchased indexed by item
totals_for_items = {}

while session:
	# get user's choice
	user_input = raw_input(">> ")

	try:
		choice = int(user_input)
	except ValueError:
		choice = -1
	
	if (choice < num_items and choice >= 0):
		fruit = item_names[choice]
		# keep track of the number of each item bought
		if (not fruit in totals_for_items):
			totals_for_items[fruit] = 0

		num_bought = totals_for_items[fruit] + 1
		totals_for_items[fruit] = num_bought

		# expecting (price, promo text)
		tuple = getPriceAndPromoTuple(fruit, num_bought)
		#print "price and promo ", tuple[0], " num bought: ", num_bought, " ", tuple[1]
		total += tuple[0]
		purchased.append((fruit, tuple[0], tuple[1]))
		print '{:<20}'.format(fruit), '{:>8}'.format('{:.2f}'.format(tuple[0])), '{:>8}'.format('{:.2f}'.format(total)), tuple[1]
		
	else:
		print "Would you like to pay for your items [y/n]"
		user_input = raw_input()
		if (user_input == "y" or user_input == "Y"):
			session = False

# print the receipt
printReceipt(purchased)

