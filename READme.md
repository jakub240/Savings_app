Update 28.02.2021

Manual:\
initialize model Cities and Category with  
python manage.py loaddata data_category.json\
python manage.py loaddata data_cities.json \
python manage.py makemigrations\
python manage.py migrate\
python manage.py runserver

1. Try to log in.
2. If you don't have an account Create a profile
3. Go to "list of expenses"
4. Enjoy

Zawartość:
- dodawanie, usuwanie, modyfikacja wydatków i budżetów (z walidacją że 
  wyświetlają się tylko te dodane przez zalogowanego użytkownika)
- logowanie, wylogowywanie, zakładanie konta (widok wydatków jest dostępny 
  tylko dla zalogowanych)
- na razie jest proste sumowanie wydatków i budżetów. Docelowo będa jakieś podziały na procenty 
  itp.

Do zrobienia:
- testy
  
- w tej chwili relacja modelu Budget do Category jest Foreign Key. Pewnie fajnie byłoby gdyby to
	było ManytoMany (wtedy Budżet można byłoby przenaczyć na kilka(lub żadną) kategorii naraz). 
  Z tym miałem problem z metodą post do tworzenia + pewien problem logiczny o którym niżej.
  
- ideą dodania Budżetu (poza tym żę można wyświetlać prostą różnicę Budżet minus Wydatki) było wyświetlanie
 wyniku działania Budżet / liczba dni od datetime.now do końca end_date = dzienna norma do wydania minus suma 
  wydatków na daną kategorię (aktualizowałoby się na bieżąco). Nie wiem czy dodanie ManytoMany troche tego nie rozwali, gdyż w obecnej sytuacji
  sensowne jest robienie jednego Budżetu na kategorie (i wyświetlanie razem z tym wynikiem co opisane wyżej).
  Budżety mogą miec dowolne start_end_date więc branie ich razem i próba agregacji tego wyniku "normy dziennej do wydawania"
  chyba nie zadziała.
  
- do tego co wyżej na pewno warto zrobić sortowanie i paginacje (przynajmniej do wydatków bo ich będzie dużo więcej niż budżetów)
 Nie wiem czy to tez troche nie rozsypie pomysłu z problemu opisanego wyżej. 
