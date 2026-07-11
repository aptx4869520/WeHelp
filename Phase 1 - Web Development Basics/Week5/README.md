# Week 5 Assignment

## Task 2: Create Database and Table

### 2-1 Create the `website` database

```sql
CREATE DATABASE website;
```

![Create website database](images/Task2-1.png)

### 2-2 Create the `member` table

```sql
USE website;

CREATE TABLE member (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    follower_count INT UNSIGNED NOT NULL DEFAULT 0,
    time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

![Create member table](images/Task2-2.png)

---

## Task 3: SQL CRUD

### 3-1 Insert five members

```sql
INSERT INTO member (name, email, password, follower_count)
VALUES
    ('test', 'test@test.com', 'test', 10),
    ('Alice', 'alice@example.com', 'alice123', 25),
    ('Bob', 'bob@example.com', 'bob123', 5),
    ('Cathy', 'cathy@example.com', 'cathy123', 40),
    ('Eason', 'eason@example.com', 'eason123', 15);
```

![Insert members](images/Task3-1.png)

### 3-2 Select all members

```sql
SELECT * FROM member;
```

![Select all members](images/Task3-2.png)

### 3-3 Select all members ordered by time descending

```sql
SELECT * FROM member
ORDER BY time DESC;
```

![Order members by time](images/Task3-3.png)

### 3-4 Select the second to fourth rows

```sql
SELECT * FROM member
ORDER BY time DESC
LIMIT 3 OFFSET 1;
```

![Select second to fourth rows](images/Task3-4.png)

### 3-5 Select members where email is `test@test.com`

```sql
SELECT * FROM member
WHERE email = 'test@test.com';
```

![Select by email](images/Task3-5.png)

### 3-6 Select members where name contains `es`

```sql
SELECT * FROM member
WHERE name LIKE '%es%';
```

![Select name containing es](images/Task3-6.png)

### 3-7 Select by email and password

```sql
SELECT * FROM member
WHERE email = 'test@test.com'
AND password = 'test';
```

![Select by email and password](images/Task3-7.png)

### 3-8 Update the member name

```sql
UPDATE member
SET name = 'test2'
WHERE email = 'test@test.com';
```

![Update member name](images/Task3-8.png)

---

## Task 4: SQL Aggregation Functions

### 4-1 Count all members

```sql
SELECT COUNT(*) AS total_members
FROM member;
```

![Count members](images/Task4-1.png)

### 4-2 Sum all follower counts

```sql
SELECT SUM(follower_count) AS total_followers
FROM member;
```

![Sum follower counts](images/Task4-2.png)

### 4-3 Calculate the average follower count

```sql
SELECT AVG(follower_count) AS average_followers
FROM member;
```

![Average follower count](images/Task4-3.png)

### 4-4 Calculate the average of the top two follower counts

```sql
SELECT AVG(follower_count) AS average_top_two
FROM (
    SELECT follower_count
    FROM member
    ORDER BY follower_count DESC
    LIMIT 2
) AS top_two;
```

![Average top two follower counts](images/Task4-4.png)

---

## Task 5: SQL JOIN

### 5-1 Create the `message` table

```sql
CREATE TABLE message (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    member_id BIGINT UNSIGNED NOT NULL,
    content TEXT NOT NULL,
    like_count INT UNSIGNED NOT NULL DEFAULT 0,
    time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES member(id)
);
```

![Create message table](images/Task5-1.png)

### 5-1_2 Insert message data

```sql
INSERT INTO message (member_id, content, like_count)
VALUES
    (1, 'Hello, this is my first message.', 5),
    (1, 'Learning SQL is interesting.', 8),
    (2, 'Nice to meet everyone.', 3),
    (3, 'This is a message from Bob.', 12),
    (4, 'Database practice is useful.', 20),
    (5, 'I am practicing JOIN queries.', 7),
    (1, 'Another message from test user.', 15);
```

![Insert message data](images/Task5-1_2.png)

### 5-2 Select all messages with sender names

```sql
SELECT
    message.id,
    member.name,
    message.content,
    message.like_count,
    message.time
FROM message
INNER JOIN member
ON message.member_id = member.id;
```

![Select all messages](images/Task5-2.png)

### 5-3 Select messages from `test@test.com`

```sql
SELECT
    message.id,
    member.name,
    member.email,
    message.content,
    message.like_count,
    message.time
FROM message
INNER JOIN member
ON message.member_id = member.id
WHERE member.email = 'test@test.com';
```

![Select messages by email](images/Task5-3.png)

### 5-4 Average like count from `test@test.com`

```sql
SELECT AVG(message.like_count) AS average_like_count
FROM message
INNER JOIN member
ON message.member_id = member.id
WHERE member.email = 'test@test.com';
```

![Average like count by email](images/Task5-4.png)

### 5-5 Average like count grouped by email

```sql
SELECT
    member.email,
    AVG(message.like_count) AS average_like_count
FROM message
INNER JOIN member
ON message.member_id = member.id
GROUP BY member.email;
```

![Average like count grouped by email](images/Task5-5.png)