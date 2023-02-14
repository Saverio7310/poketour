# import che permettono di collegarmi alla pagina desiderata, di cliccare su alcuni tasti per caricare la lista completa
# e di navigare al suo interno
import requests
import bs4
import re
import Classes.pokemon as poke
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


class Download():
    # insieme di variabili che vanno cambiate ad ogni utilizzo
    # url della pagina del torneo in question, in questo caso il codice finale va cambiato dato che è unico per ogni torneo
    # numero della colonna contenente il link della pagina del team
    CLASSIFICATION_URL = "https://rk9.gg/roster/"
    TEAMLIST_URL = "https://rk9.gg"
    TOURNAMENT_CODE = "df5AzRjKxTb62H7BsbOe"

    def establish_connection(self):
        # driver per andare a caricare la pagina html dato che la lista non viene caricata tutta subito. Non so nello specifico
        # a cosa servino. In questo caso ho usato ChromeOpitons dato che è uno dei browser più usati.
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # si carica la pagina html e tramite il Select si seleziona 'All' che mostra la lista completa di tutti gli iscritti
        web_driver = webdriver.Chrome('chromedriver', options=options)
        web_driver.get(self.CLASSIFICATION_URL + self.TOURNAMENT_CODE)
        select = Select(web_driver.find_element(By.NAME, "dtLiveRoster_length"))
        select.select_by_visible_text('All')
        # tramite bs4 mi prendo il codice html solo dopo aver caricato la lista, altrimenti non la potevo vedere. Tramite find
        # trovo la tabella contenente i dati
        soup = bs4.BeautifulSoup(web_driver.page_source, "html.parser")
        return soup.find(id="dtLiveRoster")

    # i due metodi seguenti servono a prendere i dati dei team. Se li si prende prima che i 
    # risultati con le posizioni siano usciti allora non bisogna prendere in considerazione la 
    # posizione perché ovviamente non c'è. Questa scelta la prendo attraverso un try - except
    def get_link_with_standing(self, tokens, items, set_teams):
        if 'Masters' in tokens:
            for item_anchor in items.find_all("a"):
                link = item_anchor['href']
            view_index = tokens.index('View')
            standing = int(tokens[view_index + 1])
            set_teams.add((link, standing))
            print('inserisco:', link, standing)

    def get_link_without_standing(self, tokens, items, set_teams):
        if 'Masters' in tokens:
            for item_anchor in items.find_all("a"):
                link = item_anchor['href']
            set_teams.add(link)
            print('inserisco:', link)

    def get_teams_link(self, table):
        # scandisco riga per riga "tr => table row" e prendo tutti i dati testuali contenuti. Splitto parola per parola tramite
        # l'attributo .text e prendo in considerazione solo i Masters. Per ognuno di loro salvo il link del team, contenuto nel
        # tag "a => anchor text for hyperlinking", in un set assieme alla posizione in classifica (che serve solo se voglio
        # analizzare la top 32 altrimenti non serve) ottenuta tramite l'indice successivo all'elemento 'View'. Infine salvo nel
        # set la tupla (link, posizione)

        # set che andrà a contenere tutti i link dei team partecipanti
        set_teams = set()
        for item_table_row in table.find_all("tr"):
            tokens_list_row = item_table_row.text.split()
            #print(*tokens_list_row, sep="\n")
            #print(type(tokens_ex), len(tokens_ex))
            try:
                try_index = tokens_list_row.index('View')
                tokens_list_row[try_index + 1]
            except IndexError:
                self.get_link_without_standing(tokens_list_row, item_table_row, set_teams)
                # trasformo il set in una lista e printo la linghezza per capire quanti elementi contiene
                list_teams = list(set_teams)
                print(len(list_teams))
            else:
                self.get_link_with_standing(tokens_list_row, item_table_row, set_teams)
                # ordino il set per ordine di arrivo se controllo la top 32
                list_teams = list(set_teams)
                list_teams = sorted(list_teams, key=lambda a: a[1])
                print(len(list_teams))
        return list_teams
            
        
    def get_all_teams(self, teams_link):
        # itero sul set di link per andare ad analizzare i dati di tutti i team. Il link in realtà è solo parziale, quindi devo
        # completarlo. Una volta fatto ciò possono iniziare a collegarmi ad ognuna delle pagine in questione tramite bs4. Cerco
        # la classe in questione che contiene i pokemon in lingua inglese e poi quella che contiene ogni singolo pokemon. Prima 
        # di tutto cerco le mosse tramite la loro classe e le inserisco in una lista da cui creo una stringa unica che mi 
        # servirà dopo per trovare l'oggetto. Fatto ciò, prendo i dati tramite un .text e creo un stringa unica da cui vado ad
        # eliminare eventuali soprannomi. Dopo splitto la stringa tramite regex per andare ad ottenere tutti i dati necessari 
        # all'interno di una lista. Per raccogliere nome, tera ed abilità accedo semplicemente alle prime 3 posizioni. Per trovare
        # l'oggetto la situazione di complica. Dato che il sito è fatto bene bene, tramite il .text si prendono anche le mosse 
        # oltre a tutte le altre informazioni. Per togliere le mosse dall'elemento della lista contenete l'oggetto uso la stringa
        # di prima con le mosse unificate. In questo modo, dato che la stringa finale è composta da oggetto + lista mosse, 
        # sottraendo da questa la stringa delle mosse rimango con l'oggetto. L'oggetto risultante è formato da una singola parola.
        # Uso quindi un piccolo ciclo con cui trasformo la stringa in una lista di caratteri ed inserisco una spazio vuoto prima
        # di ogni lettera maiuscola. Fatto ciò, ho raccolto tutti i dati che mi servivano e posso inserire il pokemon nel suo
        # team e il team nella lista di tutti i team.
        list_all_teams = list()

        for partial_link, _ in teams_link:
            general_link = self.TEAMLIST_URL + partial_link

            team_page = requests.get(url=general_link)
            team_soup = bs4.BeautifulSoup(team_page.text, "html.parser")

            team_table = team_soup.find("div", {"class": "my-3 mx-5 pt-2 px-3 translation lang-EN"})

            list_single_team = list()

            for single_pokemon in team_table.find_all("div", {"class": "pokemon bg-light-green-50 p-3"}):
                list_moves = list()

                for move in single_pokemon.find_all("span", {"class": "badge"}):
                    list_moves.append(move.text)

                string_moves_for_item = ''.join(list_moves).replace(' ','')

                tokens = single_pokemon.text.split()
                single_string = ' '.join(tokens)

                single_string = re.sub('\s*"\w*\D*"', '', single_string)
                list_all_attributes = re.split(' EN \w*\s*Tera Type: | Ability: | Held Item: ', single_string)

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
                    
                list_single_team.append(poke.Pokemon(name= name, typo= "Type",ability= ability,tera= tera,moves= list_moves,item_held= item))
                print(name, 'teratipo:', tera, 'mosse:', *list_moves, 'abilità:', ability, 'item held:', item)

            list_all_teams.append(list_single_team)
            team_page.close()

        return list_all_teams
    

    