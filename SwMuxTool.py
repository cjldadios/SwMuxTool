from PyQt5 import QtWidgets, uic
import sys, webbrowser, os #webbrowser needed to open default browser, os neeeded to open file in its default program

from SwMuxTool_ui import Ui_MainWindow



# Defining a product class for easier product search
class Product:
    def __init__(self, name, inputCombinationsDictionary, url, description):
        self.name = name # String
        self.inputCombinationsDictionary = inputCombinationsDictionary
        self.url = url 
        self.description = description

        ## A sample inputCombinationsDictionary would look like this:
        # inputCombinationsDictionary = {
        #     # this is x : (this is y max & min)
        #     "+-15": (0.8, 2.0), 
        #     "+-5": (0.8, 2.0),
        #     "+12": (0.8, 2.0), # But is this supposed to be min, max or really max, min?
        # }
        


class Ui(QtWidgets.QMainWindow):
   
    global x,y,z,answer,d,t,label1 #[,,, answer string, description string, test circuit #, label string]
    x = 0;    y = 0;    z = 0;    t = 0
    answer = ""; d = ""; label1 = ""; label2=""

        
    def __init__(self, parent = None):
        super(Ui, self).__init__()
        # uic.loadUi('SwMuxTool.ui', self) # Old one
            
        ui = Ui_MainWindow()
        ui.setupUi(self)

        self.matchedProductsList = [] # Store here the appropriate products when searching for one, or more.
        # Declare a list of Product available.
        self.productList = [
            # Declare instances of class Product within this list...
            Product(
                # ...with this name, etc. 
                name = "ADG141X", # Separate with comma.
                inputCombinationsDictionary = {
                    # this is x : (this is y max & min)
                    "+-15": (0.8, 2.0), 
                    "+-5": (0.8, 2.0),
                    "+12": (0.8, 2.0),
                }, # See this comma.
                url = "https://www.analog.com/en/products/adg1411.html",
                description = "1.5 \u2126  On Resistance \n \u00b115 V/+12 V/\u00b15 V, iCMOS\n Quad SPST Switches"
            ), # Parameters must be separated by comma.
            Product(
                name = "ADG161X",
                inputCombinationsDictionary = {
                    "+-5": (0.8, 2.0), 
                    "+12": (0.8, 2.0),
                    "+5": (0.8, 2.0),
                    "+3.3": (0.8, 2.0),
                    # This product can have an x of +-5, +-12, +5 and +3.3
                    # with a y of 0.8V max and 2.0V min.
                },
                url = "https://www.analog.com/en/products/adg1611.html", 
                description = "1 \u2126 Typical On Resistance,\n \u00b15 V/ +12 V/ +5 V/ +3.3 V \n Quad SPST Switches"
            ),
            Product(
                name = "ADG61X",
                inputCombinationsDictionary = {
                    "+3": (0.8, 2.0), # x = +3 : 0.8V >= y >= 2.0V.
                    "+-5": (0.8, 2.4), # In other words, this is a combination of x=4 and y=2 assigned to this product
                    "+5": (0.8, 2.4),
                },
                url = "https://www.analog.com/en/products/adg1611.html", 
                description = "1 \u2126 Typical On Resistance,\n \u00b15 V/ +12 V/ +5 V/ +3.3 V \n Quad SPST Switches"
            ),                     
        ]
        
        
        self.btnExit = self.findChild(QtWidgets.QPushButton, 'btnExit') # Find the button
        self.btnExit.clicked.connect(self.btnExitPressed) # Remember to pass the definition/method, not the return value!

        self.comboAnalog = self.findChild(QtWidgets.QComboBox, 'comboAnalog') # Find [Analog Input Range] combobox
        self.comboAnalog.activated.connect(self.comboAnalogChanged)
        
        self.comboDigital = self.findChild(QtWidgets.QComboBox, 'comboDigital') # Find [Digital Input Range] combobox
        self.comboDigital.activated.connect(self.comboDigitalChanged)
        
        self.btnFind = self.findChild(QtWidgets.QPushButton, 'btnFind') # Find [Find Switch] button
        self.btnFind.clicked.connect(self.btnFindPressed)
        
        self.lblAnswer = self.findChild(QtWidgets.QLabel, 'lblAnswer') # Find lblAnswer
        self.lblDescription = self.findChild(QtWidgets.QLabel, 'lblDescription') # Find lblAnswer
        
        self.btnProduct = self.findChild(QtWidgets.QPushButton, 'btnProduct') # Find [Open Data Sheet] button
        self.btnProduct.clicked.connect(self.btnProductPressed)
        
        self.lblBlock = self.findChild(QtWidgets.QLabel, 'lblBlock')
        
        self.comboTest = self.findChild(QtWidgets.QComboBox, 'comboTest') # Find [Digital Input Range] combobox
        self.comboTest.activated.connect(self.comboTestChanged)
        
        self.btnGenerate = self.findChild(QtWidgets.QPushButton, 'btnGenerate') # Find [Generate Circuit] button
        self.btnGenerate.clicked.connect(self.btnGeneratePressed)
                  
        self.show()
  


    def btnExitPressed(root): # Function when Exit is Pressed
      #  root.destroy()
        window.close()
        print('Exit Pressed')
    
    def comboAnalogChanged(self, valueA): #get value of [Analog Input Range] combobox
        global x
        print("Analog changed", valueA)
        x = valueA
        self.lblAnswer.setText("No Product Selected Yet") #changing answer to default when an input changed
        d = ""
        self.lblDescription.setText(d)
        return x
    
    def comboDigitalChanged(self, valueD): #get value of [Digital Input Range] combobox
        global y
        print("Digital changed", valueD)
        y = valueD
        self.lblAnswer.setText("No Product Selected Yet") #changing answer to default when an input changed
        d = ""
        self.lblDescription.setText(d)
        return y   
    
    def btnFindPressed(self): # Function when Find is Pressed
        global x, y, z, answer, label, d
        # \u00b1 is ± ; \u2126 is Ω

        print("Clearing self.matchedProductsList...")
        self.matchedProductsList = [] # Reset list of selected/found products because we're searching again.
        print("self.matchedProductsList: " + str(self.matchedProductsList))
        
        answer = "" # Clear answer
        d = "" # Clear description

        # Define dictionary for converting numerical x and y to string equivalent.
        analogInputRangeDictionary = {
            1: "+-15",
            2: "+-5",
            3: "+12",
            4: "+5",
            5: "+3.3",
            6: "+3"
            # Don't forget to separate these with comma.
        }
        controlInputRangeDictionary = {
            1: (0.8, 2.0), # Is this (mix, min) or (min, max)?
            2: (0.8, 2.4) # Is this mislabeled?
        }

        # Find the product using x and y in the productList
        # using a for loop, traversing over each productList elements.
        for product in self.productList:
            convertedX = analogInputRangeDictionary.get(x)
            print("convertedX: " + str(convertedX))

            # Find if this x is available for this product, and return the associated y to it.
            productControlInputRange = product.inputCombinationsDictionary.get(convertedX)
            print("productControlInputRange: " + str(productControlInputRange))
            
            # If such x is not found in this product, since there's no y associated to it... 
            if productControlInputRange is None: 
                pass # ... Do nothing. Try searching in another product in the list.
            else: # Else, if the x is available, 
                # check if the returned/associated productControlInputRange
                # matches with the y that we're looking for.

                # First convert the numerical y to it's equivalent label
                # using the defined dictionary.
                convertedY = controlInputRangeDictionary.get(y)

                print("convertedY: " + str(convertedY))

                # Next, compare if the y matches.
                if convertedY == productControlInputRange:
                    # We've found the right product.

                    print("Found product: " + product.name)
                    print("Adding product to matchedProductsList...")
                    self.matchedProductsList.append(product) # Take note of the right product.
                    print(" self.matchedProductsList: " + str(self.matchedProductsList))

                    continue # Then, still proceed with looking to other products
                        # as there might still be other compatible products.
               

        print("x: " + str(x))
        print("y: " + str(y))


        # Collate the details of all selected products.
        for product in self.matchedProductsList:
            answer += product.name + "\n"                    
            z = -1 # z is now anything but zero because a product has been selected
            # Also, edit product descriptop here by appending each...
            d += product.description + " \n" # ...of the selected product's description.

        print("description: " + d)

        if x*y == 0: #if one input is unchanged from default
                answer = "Please select input values"
                z = 0
                d = ""
        elif not self.matchedProductsList: # if self.matchedProductsList is empty 
            answer = "We don't have that product."   
            z = 0
            d = ""
            
   # def lblAnswerOutput(): # Function when Exit is Pressed      
   #label1 = str(x) + ", " + str(y) + ", " + str(d) + ", " + answer + ", " + str(z)  
        print(answer)
        self.lblAnswer.setText(answer)
        self.lblDescription.setText(d)
    
    
    def btnProductPressed(self): # Function when Datasheet is Pressed
        global url2
        if (z==0): #if no product is selected yet (Find Switch not pressed)
            print("No Product Selected")
            label = "Press Find Switch Button"
            self.lblAnswer.setText(label)
            return

        # Open the url of all selected products.
        for product in self.matchedProductsList:
            webbrowser.open_new(product.url)


        # if (z==1):
        #     url  = "https://www.analog.com/en/products/adg1411.html"
        #     url2 = None
        # elif (z==2):
        #     url  =  "https://www.analog.com/en/products/adg1411.html"
        #     url2 = "https://www.analog.com/en/products/adg1611.html"
        # elif (z==3 ):
        #     url  = "https://www.analog.com/en/products/adg1611.html"
        #     url2 = None
        # elif (z==4):
        #     url  = "https://www.analog.com/en/products/adg611.html"
        #     url2 = None
        
        # # Open urls if not None, otherwise error will occur.
        # if url is not None:
        #     webbrowser.open_new(url)
        # if url2 is not None:
        #     webbrowser.open_new(url2)
        #         # Enclosing this line in an if statement is 
        #         # especially important, because url2 is sometimes None,
        #         # and webbrowser.open_new(url2) would produce an error
        #         # causing the progrom to stop running.
         
    def comboTestChanged(self, valueT): #get value of [Analog Input Range] combobox
        global t
        print("Circuit Changed", valueT)
        t = valueT
        return t
    
    def btnGeneratePressed(self, valueL): # Function when Generate is Pressed
        global t,z
        if (z != 0):
            if (t != 0):
                # file = open(r"C:/Users/K55VJ/Desktop/Work/SwMuxTool/TestCircuits/TestCircuits.asc","r")
                os.startfile('C:/Users/K55VJ/Desktop/Work/SwMuxTool/TestCircuits/TestCircuits.asc')
                print ("Opening LTspice")
            else:
                print ("Select Test Circuit")
        else: 
            print("No Product Selected Yet")
            



# Main script beginning
app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = Ui() # Create an instance of our class
app.exec_() # Start the application

