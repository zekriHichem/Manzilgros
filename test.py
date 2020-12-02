from base import Session, engine, Base
import json
import bonTransfertInterne as bti
from modals import *
from flask import jsonify
#products = Facture.get_all()
import pandas as pd

#print((json.dumps([ob.to_dict() for ob in products])))
'''
products= Product.read_excel("yyy.xlsx")
bti.run(products, 48)'''

#Facture.delete(1)

User.register("Hicham" , "admin", "admin")

a= User.login("Hicham" , "admin")
print(a)