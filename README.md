
# School Management API

API umożliwia zarządzanie użytkownikami różnych grup w systemie szkolnym: `Student`, `Parent`, `Teacher`, `Director`, `Admin`. Poniżej znajduje się opis dostępnych endpointów oraz ich funkcjonalności.

---

## Endpointy

### 1. Zarządzanie studentami

#### **Lista wszystkich studentów i dodawanie nowego studenta**
- **URL:** `/students/`
- **Metody:** `GET`, `POST`

##### **GET**:
Zwraca listę wszystkich studentów w systemie.

**Przykład odpowiedzi:**
```json
[
    {
        "id": 1,
        "user": {
            "id": 1,
            "username": "john_doe",
            "email": "john.doe@example.com",
            "pesel": "12345678901",
            "login": "john_doe",
            "Name": "John",
            "Surname": "Doe",
            "birth_date": "2005-09-15",
            "user_type": "Student"
        },
        "parent": null
    }
]
```

##### **POST**:
Tworzy nowego użytkownika o typie `Student`.

**Przykład żądania:**
```json
{
    "username": "jane_doe",
    "email": "jane.doe@example.com",
    "password": "securepassword123",
    "pesel": "98765432109",
    "login": "jane_doe",
    "Name": "Jane",
    "Surname": "Doe",
    "birth_date": "2006-07-20"
}
```

**Przykład odpowiedzi:**
```json
{
    "id": 2,
    "user": {
        "id": 2,
        "username": "jane_doe",
        "email": "jane.doe@example.com",
        "pesel": "98765432109",
        "login": "jane_doe",
        "Name": "Jane",
        "Surname": "Doe",
        "birth_date": "2006-07-20",
        "user_type": "Student"
    },
    "parent": null
}
```

#### **Pobieranie szczegółów pojedynczego studenta**
- **URL:** `/students/<id>/`
- **Metody:** `GET`

**Przykład odpowiedzi:**
```json
[
    {
        "id": 1,
        "user": {
            "id": 1,
            "username": "john_doe",
            "email": "john.doe@example.com",
            "pesel": "12345678901",
            "login": "john_doe",
            "Name": "John",
            "Surname": "Doe",
            "birth_date": "2005-09-15",
            "user_type": "Student"
        },
        "parent": null
    }
]
```

---

### 2. Zarządzanie rodzicami

#### **Lista wszystkich rodziców i dodawanie nowego rodzica**
- **URL:** `/parents/`
- **Metody:** `GET`, `POST`

##### **GET**:
Zwraca listę wszystkich rodziców.

##### **POST**:
Tworzy nowego użytkownika o typie `Parent`.

#### **Pobieranie szczegółów pojedynczego rodzica**
- **URL:** `/parents/<id>/`
- **Metody:** `GET`

---

### 3. Zarządzanie nauczycielami

#### **Lista wszystkich nauczycieli i dodawanie nowego nauczyciela**
- **URL:** `/teachers/`
- **Metody:** `GET`, `POST`

##### **GET**:
Zwraca listę wszystkich nauczycieli.

##### **POST**:
Tworzy nowego użytkownika o typie `Teacher`.

#### **Pobieranie szczegółów pojedynczego nauczyciela**
- **URL:** `/teachers/<id>/`
- **Metody:** `GET`

---

### 4. Zarządzanie dyrektorami

#### **Lista wszystkich dyrektorów i dodawanie nowego dyrektora**
- **URL:** `/directors/`
- **Metody:** `GET`, `POST`

##### **GET**:
Zwraca listę wszystkich dyrektorów.

##### **POST**:
Tworzy nowego użytkownika o typie `Director`. Należy podać dodatkowo pole `school` z ID szkoły.

**Przykład żądania:**
```json
{
    "username": "director01",
    "email": "director01@example.com",
    "password": "securepassword123",
    "pesel": "12312312312",
    "login": "director01",
    "Name": "Alice",
    "Surname": "Smith",
    "birth_date": "1975-01-01",
    "school": 1
}
```

#### **Pobieranie szczegółów pojedynczego dyrektora**
- **URL:** `/directors/<id>/`
- **Metody:** `GET`

---

### 5. Zarządzanie administratorami

#### **Lista wszystkich administratorów i dodawanie nowego administratora**
- **URL:** `/admins/`
- **Metody:** `GET`, `POST`

##### **GET**:
Zwraca listę wszystkich administratorów.

##### **POST**:
Tworzy nowego użytkownika o typie `Administrator`.

#### **Pobieranie szczegółów pojedynczego administratora**
- **URL:** `/admins/<id>/`
- **Metody:** `GET`

---

## Uwagi
1. **Walidacja haseł**: Hasła przesyłane w żądaniach `POST` są przechowywane w postaci zaszyfrowanej.
2. **Identyfikacja użytkownika**: Każda grupa (`Student`, `Parent`, `Teacher`, `Director`, `Admin`) jest powiązana z modelem `CustomUser`.
3. **Autoryzacja**: Niektóre endpointy mogą wymagać odpowiednich uprawnień. Upewnij się, że użytkownik jest zalogowany i ma wymagane role.
4. **Super admin**: login: admin, password: admin