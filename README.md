# School Management API

API umożliwia zarządzanie szkołami, klasami, uczniami oraz nauczycielami w systemie szkolnym. Poniżej znajduje się opis dostępnych endpointów oraz ich funkcjonalności.

---


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

## Endpointy

### 1. Zarządzanie klasami (dyrektor)

#### **Lista wszystkich klas w danej szkole oraz dodawanie nowej klasy**
- **URL:** `/schools/<int:school_id>/classes/`
- **Metody:** `GET`, `POST`

##### **GET**:
Zwraca listę wszystkich klas przypisanych do konkretnej szkoły.

**Przykład odpowiedzi:**
```json
[
    {
        "id": 1,
        "name": "Class A",
        "supervising_teacher": 2
    },
    {
        "id": 2,
        "name": "Class B",
        "supervising_teacher": 3
    }
]
```

##### **POST**:
Dodaje nową klasę do konkretnej szkoły.

**Przykład żądania:**
```json
{
    "name": "Class C",
    "supervising_teacher": 2
}
```

**Przykład odpowiedzi:**
```json
{
    "id": 3,
    "name": "Class C",
    "school": 1,
    "supervising_teacher": 2
}
```

---

#### **Zarządzanie pojedynczą klasą**
- **URL:** `/schools/<int:school_id>/classes/<str:name>/`
- **Metody:** `GET`, `PATCH`, `DELETE`

##### **GET**:
Zwraca szczegóły konkretnej klasy w danej szkole.

##### **PATCH**:
Aktualizuje nazwę klasy lub wychowawcę.

**Przykład żądania:**
```json
{
    "name": "Class D",
    "supervising_teacher": 3
}
```

##### **DELETE**:
Usuwa konkretną klasę.

---

### 2. Zarządzanie uczniami (dyrektor)

#### **Lista wszystkich uczniów w danej szkole oraz dodawanie nowego ucznia**
- **URL:** `/students/<int:school_id>/`
- **Metody:** `GET`, `POST`

##### **GET**:
Zwraca listę wszystkich uczniów przypisanych do konkretnej szkoły.

##### **POST**:
Dodaje nowego ucznia do danej szkoły.

**Przykład żądania:**
```json
{
    "username": "john_doe",
    "email": "john.doe@example.com",
    "password": "securepassword123",
    "pesel": "12345678901",
    "login": "john_doe",
    "Name": "John",
    "Surname": "Doe",
    "birth_date": "2005-09-15"
}
```

#### **Zarządzanie szczegółami ucznia**
- **URL:** `/students/<int:pk>/`
- **Metody:** `GET`

##### **GET**:
Zwraca szczegóły pojedynczego ucznia.

---

#### **Zarządzanie przypisaniem ucznia do klasy**
- **URL:** `/students/class/`
- **Metody:** `PATCH`

##### **PATCH**:
Aktualizuje przypisanie ucznia do konkretnej klasy.

**Przykład żądania:**
```json
{
    "student_id": 1,
    "class_name": "2c"
}
```

---

### 3. Zarządzanie nauczycielami (dyrektor)

#### **Lista wszystkich nauczycieli oraz dodawanie nowego nauczyciela**
- **URL:** `/teachers/`
- **Metody:** `GET`, `POST`

##### **GET**:
Zwraca listę wszystkich nauczycieli w systemie.

##### **POST**:
Dodaje nowego nauczyciela.

**Przykład żądania:**
```json
{
    "username": "teacher_john",
    "email": "john.teacher@example.com",
    "password": "strongpassword123",
    "pesel": "98010112345",
    "login": "john_teacher",
    "Name": "John",
    "Surname": "Doe",
    "birth_date": "1980-01-01"
}
```

#### **Zarządzanie szczegółami nauczyciela**
- **URL:** `/teachers/<int:pk>/`
- **Metody:** `GET`, `PATCH`, `DELETE`

##### **GET**:
Zwraca szczegóły konkretnego nauczyciela.

##### **PATCH**:
Aktualizuje dane nauczyciela.

**Przykład żądania:**
```json
{
    "email": "updated.teacher@example.com",
    "Name": "Updated Name"
}
```

##### **DELETE**:
Usuwa nauczyciela.

---

### Zarządzanie tematami zajęć (Subjects)

#### **Lista wszystkich tematów zajęć oraz dodawanie nowego tematu**
- **URL:** `/subjects/`
- **Metody:** `GET`, `POST`

#### **GET**:
Zwraca listę wszystkich tematów zajęć.

**Przykład odpowiedzi:**
```json
[
    {
        "id": 1,
        "name": "Mathematics"
    },
    {
        "id": 2,
        "name": "Physics"
    }
]
```

#### **POST**:
Dodaje nowy temat zajęć.

**Przykład żądania:**
```json
{
    "name": "Biology"
}
```

**Przykład odpowiedzi:**
```json
{
    "id": 3,
    "name": "Biology"
}
```

---

### Zarządzanie zajęciami (Classes)

#### **Tworzenie zajęć cyklicznych**
- **URL:** `/classes/`
- **Metody:** `POST`

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
    "start_time": "08:30:00",
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
## Wiadomości

### 1. Odebrane wiadomości
**Path:** `/get_received_messages/`  
**Metoda:** `GET`  
**Opis:** Zwraca listę wszystkich wiadomości odebranych przez aktualnie zalogowanego użytkownika.  

**Przykładowa odpowiedź:**
```json
[
    {
        "id": 1,
        "date": "2025-01-05T12:34:56",
        "topic": "Zaproszenie",
        "content": "Cześć, zapraszam na spotkanie.",
        "read": false,
        "sender": 2,
        "address": 1
    }
]
```

---

### 2. Wysłane wiadomości
**Path:** `/get_sent_messages/`  
**Metoda:** `GET`  
**Opis:** Zwraca listę wszystkich wiadomości wysłanych przez aktualnie zalogowanego użytkownika.  

**Przykładowa odpowiedź:**
```json
[
    {
        "id": 2,
        "date": "2025-01-04T14:30:00",
        "topic": "Podziękowanie",
        "content": "Dziękuję za Twoją pomoc!",
        "read": true,
        "sender": 1,
        "address": 3
    }
]
```

---

### 3. Aktualizacja statusu wiadomości
**Path:** `/update_message_status/<int:message_id>/`  
**Metoda:** `PATCH`  
**Opis:** Aktualizuje status wiadomości, np. pole `read`, oznaczając wiadomość jako odczytaną lub nieodczytaną.  

**Przykładowa odpowiedź:**
```json
{
    "message": "Status wiadomości został zaktualizowany."
}
```

---

### 4. Wysyłanie nowej wiadomości
**Path:** `/send_message/`  
**Metoda:** `POST`  
**Opis:** Tworzy nową wiadomość z podanym tematem, treścią, nadawcą i adresatem.  
**Przykładowe użycie (curl):**
```json
{
    "content": "Cześć, jak się masz? To wiadomość testowa.",
    "topic": "Zapytanie",
    "address_id": 2
}
```
**Przykładowa odpowiedź:**
```json
{
    "message": "Wiadomość została pomyślnie wysłana."
}
```

---

## Wymagania:
- Wszystkie endpointy wymagają uwierzytelnienia tokenem (`Authorization: Token <your-token>`).
- Token musi być powiązany z zalogowanym użytkownikiem.

## Uwagi:
- Endpointy `/get_received_messages/` i `/get_sent_messages/` sortują wiadomości według daty w kolejności od najnowszych do najstarszych.
- Pola `read` pozwalają na śledzenie, czy wiadomość została odczytana.

# Zarządzanie Frekwencją

API umożliwia zarządzanie frekwencją uczniów dla zajęć oraz indywidualnych uczniów. Poniżej znajduje się opis endpointów, ich działania oraz przykładowych zapytań.

---

## 1. Zarządzanie frekwencją w klasach

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

#### **GET**:
Zwraca listę uczniów oraz ich frekwencję w danej klasie.

**Parametry URL:**
- `class_id` - ID zajęć, dla których chcemy pobrać frekwencję.

**Przykład zapytania:**
```
GET /api/classes/frequency/?class_id=1
```

**Odpowiedź (200 OK):**
```json
[
    {
        "id": 101,
        "student": "John Doe",
        "frequency": [
            {
                "id": 1,
                "type": "P",
                "class_id": 1
            }
        ]
    },
    {
        "id": 102,
        "student": "Jane Smith",
        "frequency": [
            {
                "id": 2,
                "type": "A",
                "class_id": 1
            }
        ]
    }
]
```

---

## 2. Zarządzanie frekwencją indywidualnego ucznia

### **Endpoint:** `/students/frequency/`
**Metody:** `GET`, `POST`, `PATCH`, `DELETE`

#### **POST**:
Dodaje frekwencję dla konkretnego ucznia w określonej klasie.

**Body (JSON):**
```json
{
    "student_id": 101,
    "class_id": 1,
    "type": "P"
}
```

**Odpowiedź (201 CREATED):**
```json
{
    "id": 1,
    "type": "P",
    "student": 101,
    "class_id": 1
}
```

#### **GET**:
Zwraca wszystkie frekwencje dla konkretnego ucznia.

**Body (JSON):**
```json
{
    "student_id": 101
}
```

**Odpowiedź (200 OK):**
```json
[
    {
        "id": 1,
        "type": "P",
        "class_id": 1
    },
    {
        "id": 2,
        "type": "A",
        "class_id": 2
    }
]
```

#### **PATCH**:
Aktualizuje typ frekwencji dla ucznia.

**Body (JSON):**
```json
{
    "frequency_id": 1,
    "type": "A"
}
```

**Odpowiedź (200 OK):**
```json
{
    "id": 1,
    "type": "A",
    "class_id": 1
}
```

#### **DELETE**:
Usuwa wpis dotyczący frekwencji ucznia.

**Body (JSON):**
```json
{
    "frequency_id": 1
}
```

**Odpowiedź (204 NO CONTENT):**
```json
{
    "message": "Frequency deleted successfully."
}
```

---
# Endpoint: Pobieranie ocen ucznia

## Opis

Endpoint umożliwia zalogowanemu uczniowi pobranie wszystkich ocen, które zostały mu przypisane.

---

## Ścieżka

**URL:** `/students/grates/`  
**Metody:** `GET`

---

## Wymagania

- Użytkownik musi być zalogowany.
- Użytkownik musi być powiązany z modelem `Student` (czyli być uczniem).

---

## Przykład żądania

### Zapytanie HTTP:
**GET** `/students/grates/`

**Nagłówki:**
```http
Authorization: Token <your_auth_token>
```

---

## Przykład odpowiedzi

Jeśli uczeń ma dwie oceny:

```json
[
    {
        "subject": "Matematyka",
        "grades": [
            {
                "id": 1,
                "value": 5.0,
                "weight": 1,
                "description": "Test 1",
                "class_id": 101,
                "category": "Sprawdzian"
            },
            {
                "id": 2,
                "value": 4.0,
                "weight": 1,
                "description": "Test 2",
                "class_id": 101,
                "category": "Kartkówka"
            }
        ]
    },
    {
        "subject": "Fizyka",
        "grades": [
            {
                "id": 3,
                "value": 3.0,
                "weight": 2,
                "description": "Sprawdzian",
                "class_id": 102,
                "category": "Sprawdzian"
            },
            {
                "id": 4,
                "value": 2.5,
                "weight": 1,
                "description": "Kartkówka",
                "class_id": 102,
                "category": "Kartkówka"
            }
        ]
    }
]
```
# API Ogłoszeń

To API umożliwia użytkownikom pobieranie i tworzenie ogłoszeń dla szkoły, do której należą. Dostęp do tych endpointów mają wyłącznie użytkownicy będący częścią grupy związanej ze szkołą (Dyrektor, Nauczyciel lub Uczeń).

---

## Endpointy

### 1. Pobieranie ogłoszeń

- **URL:** `/get_announcements/`
- **Metoda:** `GET`
- **Wymagane uprawnienia:** 
  - Dyrektor
  - Nauczyciel
  - Uczeń

#### Opis:
Pobiera wszystkie ogłoszenia dla szkoły, do której należy zalogowany użytkownik. Ogłoszenia są sortowane według daty malejąco.

#### Przykład żądania:
```http
GET /get_announcements/ HTTP/1.1
Authorization: Token <TOKEN_UŻYTKOWNIKA>
```

#### Przykład odpowiedzi:
```json
[
    {
        "id": 1,
        "topic": "Szkoła zamknięta",
        "content": "Szkoła będzie zamknięta w poniedziałek z powodu konserwacji.",
        "date": "2025-01-15",
        "author": 3
    },
    {
        "id": 2,
        "topic": "Nowości w bibliotece",
        "content": "Nowe książki są już dostępne w bibliotece.",
        "date": "2025-01-10",
        "author": 4
    }
]
```

#### Przykład odpowiedzi w przypadku braku uprawnień:
Jeśli użytkownik nie należy do grupy związanej ze szkołą:
```json
{
    "error": "Użytkownik nie należy do grupy związanej ze szkołą."
}
```

---

### 2. Tworzenie ogłoszeń

- **URL:** `/post_announcements/`
- **Metoda:** `POST`
- **Wymagane uprawnienia:** 
  - Dyrektor
  - Nauczyciel

#### Opis:
Pozwala Dyrektorom i Nauczycielom tworzyć ogłoszenia dla ich szkoły.

#### Przykład żądania:
```http
POST /post_announcements/ HTTP/1.1
Authorization: Token <TOKEN_UŻYTKOWNIKA>
Content-Type: application/json

{
    "topic": "Spotkanie z rodzicami",
    "content": "Spotkanie z rodzicami odbędzie się w piątek o godzinie 10:00.",
    "date": "2025-01-20"
}
```

#### Przykład odpowiedzi:
```json
{
    "id": 3,
    "topic": "Spotkanie z rodzicami",
    "content": "Spotkanie z rodzicami odbędzie się w piątek o godzinie 10:00.",
    "date": "2025-01-20",
    "author": 5
}
```

#### Przykład odpowiedzi w przypadku błędu:
1. Jeśli użytkownik nie należy do grupy związanej ze szkołą:
    ```json
    {
        "error": "Użytkownik nie należy do grupy związanej ze szkołą."
    }
    ```

2. Jeśli dane żądania są nieprawidłowe:
    ```json
    {
        "topic": [
            "To pole jest wymagane."
        ],
        "content": [
            "To pole jest wymagane."
        ],
        "date": [
            "To pole jest wymagane."
        ]
    }
    ```

---

## Uwagi:
- **Autoryzacja:** Oba endpointy wymagają, aby użytkownik podał ważny token.
- **Uprawnienia:** 
  - Tylko Dyrektorzy i Nauczyciele mogą tworzyć ogłoszenia.
  - Uczniowie mogą jedynie przeglądać ogłoszenia.

---