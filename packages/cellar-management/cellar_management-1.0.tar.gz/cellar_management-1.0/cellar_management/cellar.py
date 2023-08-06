from datetime import date
import copy
from .bottle import __eq__, bottle

class cellar:

    def __init__(self, size=100):

        """ Cellar class used to represent a wine cellar and to store bottles.

        Attributes:
            size (int) the maximum bottle storage capacity of the cellar
            wine_list (list of int) the list of bottles in the cellar
    """
        self.size = size
        self.wine_list = []

    def __repr__(self):

        """ Function to output the characteristics of the cellar.

        Attributes:
            None

        Returns:
            string: characteristics of the cellar

        """
        return 'Maximum cellar storage capacity:{}\n{} bottles are stored in\
                the cellar'.format(self.size, len(self.wine_list))

    def add(self, bottle, quantity=1):

        """ Function to add bottles into the cellar.

        Args:
            bottle (Class object) the class object of the bottle to be stored
            quantity (int) number of similar bottles to be added

        Returns:
            None
        """

        for i in range(quantity):

            if len(self.wine_list) < self.size :
                self.wine_list.append(bottle)

            else:
                print('{} bottles of {} cannot be added because the cellar is\
                       full'.format(i, bottle.id))

    def subset(self, attribute, value):

        """ Function to return bottles with a specified value for a specified
            attribute.

        Args:
            bottle (Class object) the class object of the bottles to be removed
            quantity (int) number of similar bottles to be removed

        Returns:
            A cellar object filtered as per the selected attribute value.
        """
        
        filtered_list = []
        filtered_cellar = cellar(self.size)

        for i in range(len(self.wine_list)):

            if getattr(self.wine_list[i], attribute) == value:
                filtered_list.append(self.wine_list[i])

        filtered_cellar.wine_list = filtered_list

        return filtered_cellar

    def remove(self, bottle, quantity=1):

        """ Function to remove bottles from the cellar.

        Args:
            bottle (Class object) the class object of the bottles to be removed
            quantity (int) number of similar bottles to be removed

        Returns:
            None
        """
        counter = quantity
        counter_2 = quantity
        i = 0

        while counter > 0:

            counter -= 1

            for i in range(len(self.wine_list)-1):

                if self.wine_list[i].__eq__(bottle):
                    del self.wine_list[i]
                    counter_2 -= 1
                    break

        if counter_2 == quantity:
            print('No bottles of {} can be found in the cellar'\
            .format( bottle.id))

        elif counter_2 != 0:
            print('{} bottles of {} were removed, {} could not be found in the\
                   cellar'.format(quantity - counter_2, bottle.id, counter_2))

    def show(self):

        """ Function that print a list of bottles in the cellar and their
            quantities

        Args:
            none

        Returns:
            None
        """
        wines = []

        for i in range(len(self.wine_list)):
            wines.append(self.wine_list[i].id)

        for wine in set(wines):
            bottle_count = sum(w.id == wine for w in self.wine_list)
            print('{} bottles of {}'.format(bottle_count, wine))

    def find(self, style='all', producer='all', name='all', vintage='all',
             maturity='all'):

        """ Function that finds bottles in the cellar based on their attributes

        Args:
            style (str) the type of wine in the bottle (possible values are
            'white', 'red', 'rose', 'sparkling' and 'sweet')
            producer (str) the producer of the wine
            name (str) the name of the wine (ex: 'Saint-Joseph Cuve Septentrio')
            vintage (int) the vintage of the wine
            maturity (str)

        Returns:
            None
            
        """
        saved_args = locals()
        found_cellar = copy.deepcopy(self)


        for attr in saved_args.keys():

            if attr != 'all':
                found_cellar = found_cellar.subset(attr, saved_args[attr])


        for wine in set(found_cellar.wine_list):
            bottle_count = sum(w.id == wine for w in self.wine_list)
            print('{} bottles of {}'.format(bottle_count, wine))


    def read_data_file(self, file_name):

        """ Function to read in data from a txt file. The txt file should have
            one wine per line with its attributes separated by commas in the
            following order: style, producer, name, vintage,  best_after,
            best_before. The wines are stored in the wine_list attribute.

        Args:
        	file_name (string): name of a file to read from

        Returns:
        	None

        """

        with open(file_name) as file:
            
            line = file.readline()
            
            while line:
                attr_list = line.split(',')
                self.wine_list.append(bottle(attr_list[0],
                                             attr_list[1],
                                             attr_list[2],
                                             int(attr_list[3]),
                                             int(attr_list[4]),
                                             int(attr_list[5])))
                line = file.readline()
            
            file.close()