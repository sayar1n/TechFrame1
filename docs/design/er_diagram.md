# ER-диаграмма базы данных

Ниже представлена ER-диаграмма (Entity-Relationship Diagram), описывающая структуру базы данных системы управления дефектами. Диаграмма показывает сущности (таблицы), их атрибуты и взаимосвязи.

```mermaid
erDiagram
    User ||--o{ Project : owns
    User ||--o{ Defect : reports
    User ||--o{ Defect : assigns
    User ||--o{ Comment : authors
    User ||--o{ Attachment : uploads
    Project ||--o{ Defect : has
    Defect ||--o{ Comment : has
    Defect ||--o{ Attachment : has

    User {
        int id PK
        string username UK
        string email UK
        string hashed_password
        string role "engineer, manager, observer"
        bool is_active
    }

    Project {
        int id PK
        string title
        string description
        datetime created_at
        int owner_id FK "references User.id"
    }

    Defect {
        int id PK
        string title
        string description
        string priority "Низкий, Средний, Высокий, Критический"
        string status "Новая, В работе, На проверке, Закрыта, Отменена"
        datetime created_at
        datetime updated_at
        datetime due_date
        int reporter_id FK "references User.id"
        int assignee_id FK "references User.id"
        int project_id FK "references Project.id"
    }

    Comment {
        int id PK
        string content
        datetime created_at
        int author_id FK "references User.id"
        int defect_id FK "references Defect.id"
    }

    Attachment {
        int id PK
        string filename
        string file_path
        datetime uploaded_at
        int uploader_id FK "references User.id"
        int defect_id FK "references Defect.id"
    }
```
