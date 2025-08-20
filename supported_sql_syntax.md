MVP (Minimum Viable Product)

1. DDL

- table creation

```sql
CREATE TABLE user (id INT, name TEXT, age INT, is_active BOOLEAN);
```

- table deletion

```sql
DROP TABLE user;
```

2. DML

- Insertion

```sql
INSERT INTO users VALUES (1, 'Alice', 30, true);
INSERT INTO users (id, name, age) VALUES (2, 'Bob', 25);

```

- Selection

```sql
SELECT * FROM users;
SELECT name, age FROM users;
SELECT DISTINCT age FROM users;
```

- Filtering

```sql
SELECT * FROM users WHERE age > 25;
SELECT * FROM users WHERE name = 'Alice' AND age > 20;
```

- Deletion

```sql
DELETE FROM users WHERE id = 2;
```
