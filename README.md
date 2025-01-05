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
    "class_id": 2
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

## Uwagi
1. **Autoryzacja:** Niektóre endpointy mogą wymagać odpowiednich uprawnień (np. rola `Director`).
2. *