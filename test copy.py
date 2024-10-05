from geopy import distance

btf = (51.634253,12.317041)
lpz = (51.343732,12.380317)


print(distance.distance(btf, lpz).km)

from datetime import datetime
d0 = datetime.strptime("2022-05-30","%Y-%m-%d")
d1 = datetime.now()
delta = d1 - d0
print(delta.days)




import spacy
nlp = spacy.load('en_core_web_sm')
doc1 = nlp(u'Haus Auensee')
doc2 = nlp(u'Haus AUENSEE')
doc3 = nlp(u'Auensee')
doc4 = nlp(u'Arena')
doc5 = nlp(u'Leipzig Arena')
doc6 = nlp(u'Quarterback Immobilien Arena')
print (doc1.similarity(doc2)) # 0.999999954642
print (doc2.similarity(doc3)) # 0.699032527716
print (doc1.similarity(doc3)) # 0.699032527716
print (doc1.similarity(doc4)) # 0.699032527716
print (doc4.similarity(doc5)) # 0.699032527716
print (doc4.similarity(doc6)) # 0.699032527716



