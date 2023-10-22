
from collections import Counter
class ManyEpisode :

    def __init__(self,data):
        self.data = data
    

    def calculByMonth(self):
        
        channel= []
      
        for episode in self.data :
             channel.append(episode['channel'])
             
        
        a = dict(Counter(channel))
        print(a)

    def calculByCountry(self):
        country= []
      
        for episode in self.data :
             country.append(episode['country'])
             
        
        a = dict(Counter(country))
        print(a)
    
    def calculByName(self):
        series= []
        for episode in self.data :
            ##print(episode['name'].split(' '))
            series.append(str(episode['name'].split(' ')))
            ##series.append(episode['name'])
        a = dict(Counter(series))
        #print(series)
        print(a)
      
    def mostEpisode(self):
        date = {}
    
        for episode in self.data :
             episode['date'],episode['channel']
             date[episode['channel']] =episode['date']
        #print(date)
        ##a = date.sort(key=)
        ##print(a)

        
