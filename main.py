from series import Series,Insert,Episode
from calcul import ManyEpisode
def main():
    url = "https://www.spin-off.fr/calendrier_des_series.html"
   
    datas = Series(url=url)
    episode = Episode(data = datas.recup() )
    manyEp = ManyEpisode(data = datas.recup())
    ############################################
    #Definition des appels pour creation tables#
    ############################################
    ##print(datas.recup())
    episode.detail_episode()
    ##print(Insert.create())
    #################################################
    #Definition des appels pour calcul algorithmique#
    #################################################
    ##manyEp.calculByMonth()
    ##manyEp.calculByCountry()
    #manyEp.calculByName()
    ##manyEp.calculByName()
    ##manyEp.mostEpisode()
    
    
if __name__ == "__main__":
    main()
    