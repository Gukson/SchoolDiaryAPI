# School Management API

API umożliwia zarządzanie szkołami, klasami, uczniami oraz nauczycielami w systemie szkolnym. Poniżej znajduje się opis dostępnych endpointów oraz ich funkcjonalności.

---

## Spis Treści

- [logowanie](#endpoint-logowania)
- [użytkownicy](#zarządzanie-użytkownikami)
  - [dyrektor](#zarządzanie-dyrektorami)
  - [nauczyciel](#zarządzanie-nauczycielami)
  - [uczniowie](#zarządzanie-uczniami)
- [wiadomości](#wiadomości)
- [klasy](#zarządzanie-klasami)
- [zajęcia](#zajęcia)
  - [dodawanie zajęć](#zarządzanie-zajęciami)
  - [pobieranie zajęć ucznia](#pobieranie-planu-zajęć-przez-ucznia)
  - [pobieranie_zajęć_nauczyciela](#pobieranie-planu-zajęć-przez-nauczyciela)
- [Frekwencja](#zarządzanie-frekwencją)
  - [Frekwencja klasy](#zarządzanie-frekwencją-klasy)
  - [Frekwencja_Ucznia](#zarządzanie-frekwencją-indywidualnego-ucznia)



## Endpoint logowania

### **Logowanie i uzyskiwanie tokenu**
- **URL:** `/auth/token/login/`
- **Metoda:** `POST`

**Przykład żądania:**
```json
{
    "login": "john_doe",
    "password": "securepassword123"
}
```

**Przykład odpowiedzi:**
```json
{
    "auth_token": "a4b9c1d4e5f6g7h8i9j0k1l2m3n4o5p6"
}
```

---

## Używanie tokenu

Po zalogowaniu i uzyskaniu tokenu można go używać do autoryzacji w kolejnych zapytaniach, dodając go do nagłówka `Authorization`.

**Przykład nagłówka:**
```
Authorization: Token a4b9c1d4e5f6g7h8i9j0k1l2m3n4o5p6
```

---

## Endpoint wylogowania

### **Wylogowanie**
- **URL:** `/auth/token/logout/`
- **Metoda:** `POST`

**Przykład żądania:**
Nie wymaga żadnych danych w ciele żądania.

**Przykład odpowiedzi:**
```json
{}
```

Po wylogowaniu token staje się nieważny.

---

## Zarządzanie użytkownikami

### **Endpoint:** `/classes/frequency/`
**Metody:** `GET`, `POST`

#### **POST**:
Dodaje frekwencję dla uczniów w danej klasie.

**Body (JSON):**
```json
{
    "classes_id": 1,
    "frequency": [
        {
            "student_id": 101,
            "type": "P"  // "P" = obecność, "A" = nieobecność
        },
        {
            "student_id": 102,
            "type": "A"
        }
    ]
}
```

**Odpowiedź (201 CREATED):**
```json
[
    {
        "id": 1,
        "type": "P",
        "student": 101,
        "class_id": 1
    },
    {
        "id": 2,
        "type": "A",
        "student": 102,
        "class_id": 1
    }
]
```

- **URL:** `/api/teachers/`
- **Metoda:** `GET` `POST` `DELETE`

`POST`
```json
{
    "username": "teacher_anna",
    "email": "anna.teacher@example.com",
    "password": "SecurePass123!",
    "pesel": "86020512345",
    "login": "anna_teacher",
    "Name": "Anna",
    "Surname": "Nowak",
    "birth_date": "1986-02-05",
    "user_type": "Teacher"
}

```

`DELETE`
```json
  "teacher_id" : 1
```

### Zarządzanie uczniami

- **URL:** `/api/students/`
- **Metoda:** `GET` `POST` `PATCH` `DELETE` 

`POST`
```json
{
    "username": "student_julia",
    "email": "julia.student@example.com",
    "password": "StrongPassword123!",
    "pesel": "05030712345",
    "login": "julia_student",
    "Name": "Julia",
    "Surname": "Kowalska",
    "birth_date": "2005-03-07",
    "user_type": "Student"
}
```

`PATCH`
```json
{
  "student_id": 1,
  "class_id" : 3
}
```


`DELETE`
DELETE nie usuwa tylko archiwizuje (czyli usuwa przypisanie ucznia do szkoły)
```json
{
  "student_id" : 1
}
```

## Wiadomości

### **Odbieranie wiadomości**
- **URL:** `/api/get_received_messages/`
- **Metoda:** `GET`

#### Opis:
Zwraca listę wszystkich wiadomości otrzymanych przez użytkownika, posortowanych w kolejności od najnowszych.

#### Przykład odpowiedzi:
```json
[
    {
        "id": 1,
        "content": "Wiadomość testowa.",
        "topic": "Informacja",
        "sender": {
            "id": 2,
            "username": "teacher_anna"
        },
        "date": "2025-01-05",
        "read": false
    },
    {
        "id": 2,
        "content": "Spotkanie o 14:00.",
        "topic": "Organizacja",
        "sender": {
            "id": 3,
            "username": "director_john"
        },
        "date": "2025-01-04",
        "read": true
    }
]
```

---

### **Wysłane wiadomości**
- **URL:** `/api/get_sent_messages/`
- **Metoda:** `GET`

#### Opis:
Zwraca listę wszystkich wiadomości wysłanych przez użytkownika, posortowanych w kolejności od najnowszych.

#### Przykład odpowiedzi:
```json
[
    {
        "id": 3,
        "content": "Czy mogę liczyć na pomoc?",
        "topic": "Pytanie",
        "address": {
            "id": 4,
            "username": "student_julia"
        },
        "date": "2025-01-05",
        "read": false
    }
]
```

---

### **Wysyłanie wiadomości**
- **URL:** `/api/send_message/`
- **Metoda:** `POST`

#### Opis:
Umożliwia wysłanie nowej wiadomości do użytkownika.

#### Przykład żądania:
```json
{
    "content": "Cześć, czy możesz mi pomóc?",
    "topic": "Pomoc",
    "address_id": 3
}
```


---

### **Aktualizacja statusu wiadomości**
- **URL:** `/api/update_message_status/<int:message_id>/`
- **Metoda:** `PATCH`

#### Opis:
Umożliwia zaktualizowanie statusu wiadomości (np. oznaczenie jako odczytane).

#### Przykład żądania:
```json
{
    "read": true
}
```

---

## Zarządzanie klasami

- **URL:** `/api/class/`
- **Metoda:** `Get` `POST` `PATCH` `DELETE`


`POST`
```json
{
  "name" : "3a"
}
```

`PATCH`
Można zmieniać nazwę i wychowawcę - nie trzeba zmianiać obu rzeczy na raz

```json
{
  "class_id" : 2,
  "name" : "4a",
  "teacher_id" : 3
}
```

`DELETE`
```json
{
  "class_id" : 2
}
```

## Zarządzanie przedmiotami
- **URL:** `/api/subjects/`
- **Metoda:** `Get` `POST`

`POST`
```json
{
  "name": "WDŻ"
}
```


## Zajęcia

## Zarządzanie zajęciami
- **URL:** `/classes/`
- **Metody:** `GET` `POST` `DELETE`

#### **POST**:
Tworzy zajęcia cyklicznie (co tydzień lub co dwa tygodnie) w określonym przedziale czasowym z uwzględnieniem godziny.

**Przykład żądania:**
```json
{
    "class_name": "1A",
    "subject_id": 2,
    "teacher_id": 3,
    "start_date": "2024-01-15",
    "end_date": "2024-03-31",
    "start_time": "08:30",
    "lesson_num": 1,
    "frequency": 1
}
```

**Przykład odpowiedzi:**
```json
{
    "message": "Utworzono 11 zajęć cyklicznych."
}
```

## Pobieranie planu zajęć przez ucznia
- **URL:** `/students/classes/`
- **Metody:** `GET` 


## Pobieranie planu zajęć przez nauczyciela
- **URL:** `/teachers/classes/`
- **Metody:** `GET` 


## Zarządzanie frekwencją

## Zarządzanie frekwencją klasy
### **Endpoint:** `/classes/frequency/`
**Metody:** `GET`, `POST`

#### **POST**:
Dodaje frekwencję dla uczniów w danej klasie.

**Body (JSON):**
```json
{
    "class_id": 1,
    "frequency": [
        {
            "student_id": 101,
            "type": "P"
        },
        {
            "student_id": 102,
            "type": "A"
        }
    ]
}
```


## Zarządzanie frekwencją indywidualnego ucznia

### **Endpoint:** `/students/frequency/`
**Metody:** `GET`, `POST`, `PATCH`, `DELETE`

### **POST**:
Dodaje frekwencję dla konkretnego ucznia w określonej klasie.

**Body (JSON):**
```json
{
    "student_id": 101,
    "class_id": 1,
    "type": "P"
}
```


### **GET**:
Zwraca wszystkie frekwencje dla konkretnego ucznia.

**Body (JSON):**
```json
{
    "student_id": 101
}
```


### **PATCH**:
Aktualizuje typ frekwencji dla ucznia.

**Body (JSON):**
```json
{
    "frequency_id": 1,
    "type": "A"
}
```


### **DELETE**:
Usuwa wpis dotyczący frekwencji ucznia.

**Body (JSON):**
```json
{
    "frequency_id": 1
}
```


---