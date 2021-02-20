Instrukcja obsługi (ostatnia aktualizacja 20.02.2021)

Działa :
- dodawanie użytkownika, logowanie

- wejście na widok wydatków (połączony z formularzem dodawania): ExpensesListFormView 
ma zaimplementowaną konieczność bycia zalogowanym i odsyła do formularza logowania
  
- Kategorie (które są do wyboru potem w formularzu do Expenses) są możliwe do zainicjalizowania z JSONa w fixtures

- dodawanie Expenses


Nie działa :

- wyświetlanie wydatków (prawdopodobnie przekombinowałem odniesienia do htmla i z html do widoku)
spróbuje jeszcze jutro rano to naprawić
  

Po korekcie, uwagi :

class Budget:
	start_date = datetime
	end_date = datetime
	amount = 
	category = ManytoMany
	
	
class Regions(miasta)

docstringi^^
