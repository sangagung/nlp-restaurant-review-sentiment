



class Review(object):
	def __init__(self, rid, text, aspects: set, trainer): 
		self.rid = rid
		self.text = text
		self.aspects = aspects
		self.trainer = trainer
	
	def __eq__(self, other): 
		if not isinstance(other, Review):
			return False	
		return self.rid == other.rid
	
	def __hash__(self):
		return 31 * hash(self.rid) +  17 * hash(self.text)

	def __str__(self):
		return '==============================================' + '\n' + self.rid + '  ' + self.trainer + '\n' + self.text + '\n' + self.aspects.get('FOOD', '-') + '  ' + self.aspects.get('PRICE', '-') + '  ' + self.aspects.get('SERVICE', '-') + '  ' + self.aspects.get('AMBIENCE', '-') + '\n'

	def add_trainer(self, trainer):
		self.trainer = self.trainer + trainer


def printcsv(review):
	return [review.rid, review.text, 
		review.aspects.get('FOOD', '-'), 
		review.aspects.get('PRICE', '-'), 
		review.aspects.get('SERVICE', '-'), 
		review.aspects.get('AMBIENCE', '-'),]


# class Aspect(object):
#     def __init__(self, category, price, service, ambience): 
#         self.food = food
#         self.price = price
#         self.service = service
#         self.ambience = ambience
	
# 	def __eq__(self): pass
	
# 	def __hash__(self): pass