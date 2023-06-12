# import che permettono di collegarmi alla pagina desiderata, di cliccare su alcuni tasti per caricare la lista completa
# e di navigare al suo interno
import requests
import bs4
import re
from urllib3.exceptions import ProtocolError
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException


class Download():
    # insieme di variabili che vanno cambiate ad ogni utilizzo
    # url della pagina del torneo in question, in questo caso il codice finale va cambiato dato che è unico per ogni torneo
    # numero della colonna contenente il link della pagina del team
    CLASSIFICATION_URL = "https://rk9.gg/roster/"
    TEAMLIST_URL = "https://rk9.gg"
    TOURNAMENT_CODE = "df5AzRjKxTb62H7BsbOe"

    # header della chiamata http che serve a farsi sgamare di meno dai siti durante le connessioni
    header = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15',
        'Accept-Language':'en-GB,en;q=0.5',
        'Referer':'https://google.com',
        'DNT':'1'
    }

    # connessione alla pagina rk9 del torneo specificato
    def establish_connection(self, code):
        # driver per andare a caricare la pagina html dato che la lista non viene caricata tutta subito. Non so nello specifico
        # a cosa servino. In questo caso ho usato ChromeOpitons dato che è uno dei browser più usati.
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # si carica la pagina html e tramite il Select si seleziona 'All' che mostra la lista completa di tutti gli iscritti
        web_driver = webdriver.Chrome('chromedriver', options=options)
        try:
            web_driver.get(self.CLASSIFICATION_URL + code)
            print(self.CLASSIFICATION_URL + code)
        except WebDriverException:
            raise Exception('Link errato. Connessione non riuscita!')
        try:
            select = Select(web_driver.find_element(By.NAME, "dtLiveRoster_length"))
        except NoSuchElementException:
            raise Exception('Codice torneo non valido!')    
        select.select_by_visible_text('All')
        # tramite bs4 mi prendo il codice html solo dopo aver caricato la lista, altrimenti non la potevo vedere. Tramite find
        # trovo la tabella contenente i dati
        soup = bs4.BeautifulSoup(web_driver.page_source, "html.parser")
        return soup.find(id="dtLiveRoster")

    def get_teams_link(self, table):
        # scandisco riga per riga "tr => table row" e prendo tutti i dati testuali contenuti. Splitto parola per parola tramite
        # l'attributo .text e prendo in considerazione solo i Masters. Per ognuno di loro salvo il link del team, contenuto nel
        # tag "a => anchor text for hyperlinking", in un set assieme alla posizione in classifica (nel caso non siano state 
        # pubblicate le posizioni inserisco un placeholder '-1') ottenuta tramite l'indice successivo all'elemento 'View'. 
        # Infine salvo nel set la tupla (link, posizione)

        # set che andrà a contenere tutti i link dei team partecipanti
        set_teams = set()
        for item_table_row in table.find_all("tr"):
            tokens_list_row = item_table_row.text.split()
            #print(*tokens_list_row, sep="\n")
            #print(type(tokens_ex), len(tokens_ex))
            #self.__get_link_with_standing(tokens_list_row, item_table_row, set_teams)
            if 'Masters' in tokens_list_row:
                for item_anchor in item_table_row.find_all("a"):
                    link = item_anchor['href']
                try:
                    standing = int(tokens_list_row[tokens_list_row.index('View') + 1])
                except ValueError:
                    raise ValueError('Le teamlist non sono state ancora pubblicate')
                except IndexError:
                    set_teams.add((link, -1))
                else:
                    set_teams.add((link, standing))
                #print('inserisco:', link, standing)
        print(len(set_teams))
        return set_teams
    
    # una volta salvati i link, posso collegarmi alle pagine dei team tramite una nuova connessione. Non scandisco sui link
    # presenti nell'insieme ritornato dalla funzione precedente perché questa funzione la chiamo tramite Thread, quindi
    # i link li passo con quella chiamta e qui il codice deve funzionare sul singolo link. È possibile che per le troppe 
    # connessioni il sito blocchi la connessione al mio indirizzo IP, generando 3 eccezioni una dentro l'altra. Per questo
    # uso un try except usando un generico 'Exception' dato che non saprei quale scegliere delle 3+ che vengono lanciate. 
    # Per velocizzare il tutto, questa funzione ritorna tutto il codice html che viene lavorato trmaite un'altra funzione.
    def get_table_html(self, team_link):
        try:
            with requests.Session() as s:
                team_page = s.get(url=self.TEAMLIST_URL + team_link[0], headers=self.header)
            team_soup = bs4.BeautifulSoup(team_page.text, "html.parser")
            return (team_soup.find("div", {"class": "my-3 mx-5 pt-2 px-3 translation lang-EN"}), team_link[0])
        except (ConnectionError, OSError, ProtocolError):
            raise Exception('Errore di comunicazione tra applicazione e server!')
        
    def get_all_teams(self, table_link_tuple):
        # itero sul set di link per andare ad analizzare i dati di tutti i team. Il link in realtà è solo parziale, 
        # quindi devo completarlo. Fatto ciò, mi collego ad ogni pagina tramite bs4. Cerco la classe che contiene i
        #  pokemon in lingua inglese e poi quella che contiene ogni singolo pokemon. Per prima cosa 
        # cerco le mosse tramite la loro classe e le inserisco in una lista da cui creo una stringa unica che mi 
        # servirà dopo per trovare l'item. Poi prendo i dati tramite un .text e creo un stringa unica da cui vado ad
        # eliminare eventuali soprannomi ed altre parti della stringa che non mi servono. Dopo splitto la stringa 
        # tramite regex per andare ad ottenere tutti i dati necessari all'interno di una lista. Per raccogliere nome, 
        # tera ed abilità accedo semplicemente alle prime 3 posizioni. Per trovare l'oggetto il procedimento complica.
        #  Dato che il sito è fatto bene bene, tramite il .text si prendono anche le mosse oltre a tutte le altre
        #  informazioni. Per togliere le mosse dall'elemento della lista contenete l'oggetto uso la stringa
        # di prima con le mosse unificate. In questo modo, dato che la stringa finale è composta da oggetto + lista mosse, 
        # sottraendo da questa la stringa delle mosse rimango con l'oggetto. L'oggetto risultante è formato da una singola
        # parola. Uso quindi un piccolo ciclo con cui trasformo la stringa in una lista di caratteri ed inserisco una 
        # spazio vuoto prima di ogni lettera maiuscola. Fatto ciò, ho raccolto tutti i dati che mi servivano e posso 
        # inserire il pokemon nel suo team e il team nella lista di tutti i team.
        list_tuple_all_poke = list()

        for single_pokemon in table_link_tuple[0].find_all("div", {"class": "pokemon bg-light-green-50 p-3"}):
            list_moves = list()

            for move in single_pokemon.find_all("span", {"class": "badge"}):
                list_moves.append(move.text)

            string_moves_for_item = ''.join(list_moves).replace(' ','')

            tokens = single_pokemon.text.split()
            single_string = ' '.join(tokens)

            #print(single_string)

            # levo tutti gli elementi che non servono e che non permettono il corretto funzionamento
            # tipo i soprannomi e la ripetizione del nome in alcune righe. Fatto ciò partiziono la 
            # stringa ed ottengo le info che mi servono, a parte l'oggetto che richiede ulteriori
            # passaggi per essere preso
            single_string = re.sub('\s*"(.*?)"', '', single_string)
            single_string = re.sub('EN (\w|\D|\s)*Tera Type:', 'EN Tera Type:', single_string)
            list_all_attributes = re.split(' EN Tera Type: | Ability: | Held Item: ', single_string)
            #print(list_all_attributes)

            name = list_all_attributes[0]
            tera = list_all_attributes[1]
            ability = list_all_attributes[2]

            list_item_and_moves = list_all_attributes[3].split()
            string_item_moves = ''.join(list_item_and_moves).replace(' ','')

            single_item_to_separate = re.split(string_moves_for_item, string_item_moves)[0]

            list_chars = list(single_item_to_separate)
            list_chars.reverse()
            for index, char in enumerate(list_chars):
                if char.isupper():
                    list_chars.insert(index + 1, ' ')
            list_chars.reverse()
            item = ''.join(list_chars).strip()
                
            list_tuple_all_poke.append((table_link_tuple[1][-20:], name, ability, tera, item, list_moves[0], list_moves[1], list_moves[2], list_moves[3]))
            #print(name, 'teratipo:', tera, 'mosse:', *list_moves, 'abilità:', ability, 'item held:', item)
        return list_tuple_all_poke