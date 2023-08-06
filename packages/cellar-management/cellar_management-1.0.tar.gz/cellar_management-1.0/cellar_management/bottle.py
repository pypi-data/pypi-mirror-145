from datetime import datetime
import math

class bottle:
    
    def __init__(self, style, producer, name, vintage,  best_after, best_before):
        
        """ Bottle class used to represent a bottle to be stored in a cellar.
	
		Attributes:
			style (str) the type of wine in the bottle (recommended values are 'white', 'red', 'rose', 'sparkling' and 'sweet')
            producer (str) the producer of the wine
            name (str) the name of the wine (ex: 'Saint-Joseph Cuvee Septentrio') 
            vintage (int) the vintage of the wine
            best_after (int) the expected year when the wine will reach maturrity
            best_before (int) the expected year when the wine will start to go bad
            id (str) a unique identifier with all unique elements of the wine concatenated in a string
			"""
        
        self.style =  style
        self.name = name
        self.producer = producer
        self.vintage = vintage
        self.id = style + ' '+ name + ' ' +str(vintage) + ' from ' + producer
        
        if math.isnan(best_after):
            self.best_after = vintage
        else:
            self.best_after = best_after
        
        
        if math.isnan(best_before):
            self.best_before = vintage + 2
        else:
            self.best_before = best_before
        
        if self.best_after <= datetime.today().year <= self.best_before:
            self.maturity = 'ready'
            
        elif self.best_after > datetime.today().year:
            self.maturity = 'young'
        
        else:
            self.maturity = 'old'

    def __eq__(self, other):
        
        """ Function to check if two bottle objects have the same values for each attributes.
	
		Attributes:
			None
            
        Returns:
			boolean: do both bottle objects have all the same attributes
        """
        return self.id == other.id
        

        