from database.regione_DAO import RegioneDAO
from database.tour_DAO import TourDAO
from database.attrazione_DAO import AttrazioneDAO

class Model:
    def __init__(self):
        self.tour_map = {} # Mappa ID tour -> oggetti Tour
        self.attrazioni_map = {} # Mappa ID attrazione -> oggetti Attrazione

        self._pacchetto_ottimo = []
        self._valore_ottimo: int = -1
        self._costo = 0

        # TODO: Aggiungere eventuali altri attributi

        # Caricamento
        self.load_tour()
        self.load_attrazioni()
        self.load_relazioni()

    @staticmethod
    def load_regioni():
        """ Restituisce tutte le regioni disponibili """
        return RegioneDAO.get_regioni()

    def load_tour(self):
        """ Carica tutti i tour in un dizionario [id, Tour]"""
        self.tour_map = TourDAO.get_tour()

    def load_attrazioni(self):
        """ Carica tutte le attrazioni in un dizionario [id, Attrazione]"""
        self.attrazioni_map = AttrazioneDAO.get_attrazioni()

    def load_relazioni(self):
        """
            Interroga il database per ottenere tutte le relazioni fra tour e attrazioni e salvarle nelle strutture dati
            Collega tour <-> attrazioni.
            --> Ogni Tour ha un set di Attrazione.
            --> Ogni Attrazione ha un set di Tour.
        """
        # TODO
        relazioni = TourDAO.get_tour_attrazioni()
        if relazioni is None:
            return

        for r in relazioni:
            id_t = r["id_tour"]
            id_a = r["id_attrazione"]

            tour = self.tour_map.get(id_t)
            attr = self.attrazioni_map.get(id_a)

            if tour is None or attr is None:
                continue

            tour.attrazioni.add(attr)
            attr.tour.add(tour)


    def genera_pacchetto(self, id_regione: str, max_giorni: int = None, max_budget: float = None):
        """
        Calcola il pacchetto turistico ottimale per una regione rispettando i vincoli di durata, budget e attrazioni uniche.
        :param id_regione: id della regione
        :param max_giorni: numero massimo di giorni (può essere None --> nessun limite)
        :param max_budget: costo massimo del pacchetto (può essere None --> nessun limite)

        :return: self._pacchetto_ottimo (una lista di oggetti Tour)
        :return: self._costo (il costo del pacchetto)
        :return: self._valore_ottimo (il valore culturale del pacchetto)
        """
        self._pacchetto_ottimo = []
        self._costo = 0
        self._valore_ottimo = -1

        # TODO

        lista_tour = [
            t for t in self.tour_map.values()
            if t.id_regione == id_regione
        ]

        lista_tour.sort(key=lambda t: t.durata_giorni)

        self._ricorsione(
            start_index=0,
            lista_tour=lista_tour,
            pacchetto_parziale=[],
            durata_corrente=0,
            costo_corrente=0,
            valore_corrente=0,
            attrazioni_usate=set(),
            max_giorni=max_giorni,
            max_budget=max_budget
        )

        return self._pacchetto_ottimo, self._costo, self._valore_ottimo




    def _ricorsione(self, start_index: int, lista_tour: list, pacchetto_parziale: list,
                        durata_corrente: int, costo_corrente: float, valore_corrente: int,
                        attrazioni_usate: set, max_giorni: int, max_budget: float):
        """ Algoritmo di ricorsione che deve trovare il pacchetto che massimizza il valore culturale"""

        # TODO: è possibile cambiare i parametri formali della funzione se ritenuto opportuno
        if valore_corrente > self._valore_ottimo:
            self._valore_ottimo = valore_corrente
            self._pacchetto_ottimo = pacchetto_parziale.copy()
            self._costo = costo_corrente

        for i in range(start_index, len(lista_tour)):
            tour = lista_tour[i]

            # vincolo giorni
            if max_giorni is not None and durata_corrente + tour.durata_giorni > max_giorni:
                continue

            # vincolo budget
            if max_budget is not None and costo_corrente + tour.costo > max_budget:
                continue

            # vincolo attrazioni duplicate
            if len(tour.attrazioni.intersection(attrazioni_usate)) > 0:
                continue


            pacchetto_parziale.append(tour)
            nuove_attr = set(tour.attrazioni)
            attrazioni_usate.update(nuove_attr)

            nuova_durata = durata_corrente + tour.durata_giorni
            nuovo_costo = costo_corrente + tour.costo
            nuovo_valore = valore_corrente + sum(a.valore_culturale for a in tour.attrazioni)

            self._ricorsione(
                start_index=i + 1,
                lista_tour=lista_tour,
                pacchetto_parziale=pacchetto_parziale,
                durata_corrente=nuova_durata,
                costo_corrente=nuovo_costo,
                valore_corrente=nuovo_valore,
                attrazioni_usate=attrazioni_usate,
                max_giorni=max_giorni,
                max_budget=max_budget
            )

            # Backtracking
            pacchetto_parziale.pop()
            for a in nuove_attr:
                attrazioni_usate.remove(a)