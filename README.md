# System rezerwacji Escape Room

Początkowy projekt Django z modelami pokoi zagadek i rezerwacji.

## Uruchomienie

1. Zainstaluj zależności: `pip install -r requirements.txt`.
2. Ustaw zmienną środowiskową `DJANGO_SECRET_KEY` na losowy, prywatny klucz.
3. Wykonaj migracje: `python manage.py migrate`.
4. Utwórz konto administratora: `python manage.py createsuperuser`.
5. Uruchom serwer: `python manage.py runserver`.

Modele `EscapeRoom` i `Booking` są dostępne w panelu administracyjnym pod `/admin/`.
