import promo_functions
import xml.etree.ElementTree as Tree

#read the inventory data file
try:
	tree = Tree.parse('inventory.xml')
	inventory = tree.getroot()
except:
	print "Error parsing the inventory.xml data file - exiting program"
	exit()

def populatePromoDict():
	global promo_dict
	promo_dict = {}
	for item in item_names:
		promo_nodes = inventory.findall("./item[@name='%s']/promo" % item)
		if (len(promo_nodes) > 0):
			promo_dict[item] = []
			for node in promo_nodes:
				nth = node.find('./nth')
				name = node.find('./name')
				discount = node.find('./discount')
				func = node.find('./func')
				# nth and (discount or func) are required - name is optional
				if (nth == None):
					continue
				else:
					nth_val = nth.text
					try:
						nth_int_val = int(nth_val)
					except:
						continue
				if (name == None):
					name_val = "Promotion Discount"
				else:
					name_val = name.text
					
				# keep track of either discount of func True
				have_a_promo = False
				if (discount != None):
					discount_val = discount.text
					try:
						discount_float_val = float(discount_val)
						have_a_promo = True
					except:
						discount_float_val = 0
				if (func != None):
					try:
						func_val = eval("promo_functions.%s" % func.text)
						have_a_promo = True
					except:
						func_val = None
				else:
					func_val = None
				
				# don't actually have any kind of promotion - skip this node
				if (not have_a_promo):
					continue
				
				# we should have all legit values to create a Promo instance
				promo = Promo(item, nth_int_val, name_val, discount_float_val, func_val)
				#print "PROMO: %s %d %s %f %s" % (promo.item, promo.nth, promo.name, promo.save, promo.func)
				promo_dict[item].append(promo)

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
	print '\n'
	print '{:<20}'.format('Purchase'), '{:>8}'.format('Price'), '{:>8}'.format('Total'), ' '*3, "Promotion"
	print '-'*20, '{:>8}'.format('-'*5), '{:>8}'.format('-'*5), ' '*3, '-'*9
	# tuple has (item name, item cost, item promo)
	for tuple in purchase:
		total += tuple[1]
		print '{:.<20}'.format(tuple[0]), '{:>8}'.format('{:.2f}'.format(tuple[1])), '{:>8}'.format('{:.2f}'.format(total)), ' '*3, tuple[2]
	
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

#used for debugging	
def printDailyDeals():
	global promo_dict
	label = "Today's Promotions:"
	print "%s\n" % label, '-'*len(label)
	for item, list in promo_dict.iteritems():
		for promo in list:
			print "%s: %s" % (promo.item, promo.name)

# make a list of the produce inventory item names
item_names = []
nodes = inventory.findall("./item[@name]")
for node in nodes:
	item_names.append( node.attrib['name'])
num_items = len(item_names)

promo_dict = {}
populatePromoDict()
printDailyDeals()

# print the inventory choices list
label = "Inventory"
print "\n%s\n" % label, '-'*len(label)
for item in item_names:
	print "-> ", item
print "Enter any other value to complete your transaction and print a receipt!\n"

purchased = []

# total spent
total = 0
# number of items purchased indexed by item
totals_for_items = {}

while True:
	try:
		fruit = raw_input(">> ")
	except:
		break

	if (fruit in item_names):
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
		print '{:<10}'.format(fruit), '{:>8}'.format('{:.2f}'.format(tuple[0])), '{:>8}'.format('{:.2f}'.format(total)),' '*3, tuple[1]
		
	else:
		break

# print the receipt
printReceipt(purchased)

