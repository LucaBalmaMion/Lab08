from database import distributore_DAO
from database.distributore_DAO import DistributoreDAO
from database.prezzo_DAO import PrezzoDAO


'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._distributori = None
        self.load_distributori()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_distributori(self):
        """ Carica tutti i distributori e li setta nella variabile self._distributori """
        self._distributori = DistributoreDAO.get_distributori()

    def get_prezzo_medio(self, mese:int):
        """
        Calcola, per ogni distributore, il prezzo medio al litro per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome del distributore, media), es. (Distributore A, 1.789)
        """
        # TODO
        result = []
        for distributore in self._distributori:
            lista_prezzi_mese = []
            prezzi_distributore = distributore.get_prezzi()
            for prezzo in prezzi_distributore:
                if prezzo.data.month == mese:
                    lista_prezzi_mese.append(prezzo.prezzo_litro)
            media = sum(lista_prezzi_mese) / len(lista_prezzi_mese)
            result.append((distributore.nome, media))
        return result



    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di rifornimenti nei primi 7 giorni
        :return: sequenza di nomi distributore ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        prezzi_settimana = self.__get_prezzi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, prezzi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {distributore.id: distributore.nome for distributore in self._distributori}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, round(self.__costo_ottimo, 2)

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_distributore, costo_corrente, prezzi_settimana):
        """ Implementa la ricorsione """
        # TODO
        if giorno > 7:
            if self.__costo_ottimo == -1 or costo_corrente < self.__costo_ottimo:
                self.__costo_ottimo = costo_corrente
                self.__sequenza_ottima = list(sequenza_parziale)
            return
        for id_distributore in prezzi_settimana:
            costo_corrente_nuovo = costo_corrente + prezzi_settimana[id_distributore][giorno - 1] * 100
            if id_distributore != ultimo_distributore and ultimo_distributore is not None:
               costo_corrente_nuovo += 5
            sequenza_parziale.append(id_distributore)
            self.__ricorsione(sequenza_parziale, giorno + 1, id_distributore, costo_corrente_nuovo, prezzi_settimana)
            sequenza_parziale.pop()

    def __get_prezzi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i prezzi dei primi 7 giorni del mese selezionato per ciascun distributore.
        :return: un dizionario: {id_distributore: [prezzo_giorno1, ..., prezzo_giorno7]}
        """
        # TODO
        diz_distributori_prezzi = {}
        for distributore in self._distributori:
            lista_prezzi = distributore.get_prezzi()
            lista_prezzi_primi_mese = [0]*7
            for prezzo in lista_prezzi:
                if prezzo.data.month == mese and prezzo.data.day <= 7:
                    lista_prezzi_primi_mese[prezzo.data.day-1] = prezzo.prezzo_litro
            diz_distributori_prezzi[distributore.id] = lista_prezzi_primi_mese
        return diz_distributori_prezzi

