# Projectnaam  
Restaurant Robot

## Projectleden  
- Timothy – [Voorzitter]  
- Arion – [Kwaliteitsbewaker]  
- Tim – [Technisch-specialist/Developer]  
- Jaden – [Notulist]  
- Eninio – [Contacts-persoon]  
- Johannes – [Kwaliteitsbewaker]  

## Doel van het project  
Het doel van dit project is het ontwikkelen van een robot die bestellingen kan serveren in een restaurantomgeving. We maken gebruik van de OTAP-methodiek om gestructureerd te werken en de kwaliteit van de code te waarborgen.

## Werkwijze en proces  
We werken volgens het OTAP-proces met de volgende branches:  
- **main:** productie  
- **test-acceptatie:** testen en acceptatie  
- **feature/***: losse features en bugfixes  

### Werkwijze:  
- Elke wijziging gebeurt in een aparte feature-branch.  
- Voor elke wijziging wordt een merge request (MR) ingediend.  
- Code wordt lokaal getest voordat een MR wordt aangemaakt.  
- Minimaal één teamlid voert een code review uit voordat er wordt gemerged.  
- Alleen de teamleider mag mergen naar productie (main).  

## Codeconventies  
We hanteren de standaard PEP 8-richtlijnen voor Python:  

- **Programmeertaal:** Python  
- **Indentatie:** 4 spaties  
- **Branch-namen:** `feature/naam`, `bugfix/naam`  
- **Commit messages:** duidelijk en in het Engels, bijvoorbeeld: `feat: add order system`  
- **Bestandsnamen:** klein en duidelijk, gescheiden door underscores, bijvoorbeeld `order_system.py`  
- **Variabelen:** kleine letters met underscores (`order_number`)  
- **Klasse-namen:** CamelCase (`OrderProcessor`)  
- **Functies:** kleine letters met underscores (`process_order()`)  
- **Lijnen:** maximaal 79 tekens  
- **Docstrings:** volgens de PEP 257-conventies  

## Licentie  
Wij gebruiken de **MIT-licentie**.  
Deze licentie is gekozen omdat deze eenvoudig en vrij is. Het maakt hergebruik mogelijk zolang de originele auteurs worden vermeld. Dit sluit aan bij het educatieve doel van ons project.  
