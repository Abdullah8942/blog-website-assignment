# Database Schema Diagram

## Blog Application Database Structure

```mermaid
erDiagram
    User ||--o{ Post : creates
    User ||--o{ Comment : writes
    User ||--|| Profile : has
    Category ||--o{ Post : contains
    Post }o--o{ Tag : has
    Post ||--o{ Comment : receives

    User {
        int id PK
        string username UK
        string email
        string password
        string first_name
        string last_name
        boolean is_staff
        boolean is_active
        boolean is_superuser
        datetime date_joined
        datetime last_login
    }

    Profile {
        int id PK
        int user_id FK_UK
        string role
        text bio
        image avatar
        string website
        string twitter
        string linkedin
        datetime created_at
        datetime updated_at
    }

    Category {
        int id PK
        string name UK
        string slug UK
        text description
        datetime created_at
    }

    Tag {
        int id PK
        string name UK
        string slug UK
        datetime created_at
    }

    Post {
        int id PK
        string title
        string slug UK
        richtext content
        text excerpt
        int author_id FK
        int category_id FK
        string status
        image featured_image
        int views
        datetime created_at
        datetime updated_at
    }

    Comment {
        int id PK
        int post_id FK
        int user_id FK
        text content
        boolean approved
        datetime created_at
        datetime updated_at
    }

    Post_Tags {
        int id PK
        int post_id FK
        int tag_id FK
    }
```

---

## Detailed Table Descriptions

### 1. **User Table** (auth_user)
- **Primary Key:** `id`
- **Unique Fields:** `username`
- **Purpose:** Stores user authentication and basic profile information
- **Relationships:**
  - One-to-Many with `Post` (via `author_id`)
  - One-to-Many with `Comment` (via `user_id`)
  - One-to-One with `Profile`

---

### 2. **Profile Table** (accounts_profile)
- **Primary Key:** `id`
- **Foreign Keys:** `user_id` → User
- **Unique Fields:** `user_id` (one-to-one relationship)
- **Purpose:** Extended user information and role management
- **Fields:**
  - `role`: ENUM('reader', 'author', 'admin') - User role
  - `bio`: TEXT - User biography
  - `avatar`: IMAGE - Profile picture
  - `website`: URL - Personal website
  - `twitter`: VARCHAR(100) - Twitter handle
  - `linkedin`: VARCHAR(100) - LinkedIn profile
  - `created_at`: TIMESTAMP
  - `updated_at`: TIMESTAMP

---

### 3. **Category Table** (blog_category)
- **Primary Key:** `id`
- **Unique Fields:** `name`, `slug`
- **Purpose:** Organize posts into categories
- **Fields:**
  - `name`: VARCHAR(100) - Category name
  - `slug`: VARCHAR(100) - URL-friendly name
  - `description`: TEXT - Category description
  - `created_at`: TIMESTAMP
- **Relationships:**
  - One-to-Many with `Post`

---

### 4. **Tag Table** (blog_tag)
- **Primary Key:** `id`
- **Unique Fields:** `name`, `slug`
- **Purpose:** Tag posts with keywords for better organization
- **Fields:**
  - `name`: VARCHAR(50) - Tag name
  - `slug`: VARCHAR(50) - URL-friendly name
  - `created_at`: TIMESTAMP
- **Relationships:**
  - Many-to-Many with `Post` (via `Post_Tags`)

---

### 5. **Post Table** (blog_post)
- **Primary Key:** `id`
- **Foreign Keys:**
  - `author_id` → User
  - `category_id` → Category (nullable, SET_NULL on delete)
- **Unique Fields:** `slug`
- **Purpose:** Main content storage for blog posts
- **Fields:**
  - `title`: VARCHAR(200) - Post title
  - `slug`: VARCHAR(200) - URL-friendly identifier
  - `content`: RICHTEXT - Post body (CKEditor)
  - `excerpt`: TEXT(300) - Short description
  - `status`: ENUM('draft', 'published')
  - `featured_image`: IMAGE - Post thumbnail
  - `views`: INTEGER - View counter
  - `created_at`: TIMESTAMP
  - `updated_at`: TIMESTAMP
- **Indexes:**
  - Index on `created_at` (descending)
  - Index on `status`
- **Relationships:**
  - Many-to-One with `User` (author)
  - Many-to-One with `Category`
  - Many-to-Many with `Tag`
  - One-to-Many with `Comment`

---

### 6. **Comment Table** (blog_comment)
- **Primary Key:** `id`
- **Foreign Keys:**
  - `post_id` → Post (CASCADE on delete)
  - `user_id` → User (CASCADE on delete)
- **Purpose:** Store user comments on blog posts
- **Fields:**
  - `content`: TEXT - Comment text
  - `approved`: BOOLEAN - Moderation flag (default: true)
  - `created_at`: TIMESTAMP
  - `updated_at`: TIMESTAMP
- **Relationships:**
  - Many-to-One with `Post`
  - Many-to-One with `User`

---

### 7. **Post_Tags Table** (blog_post_tags)
- **Primary Key:** `id`
- **Foreign Keys:**
  - `post_id` → Post
  - `tag_id` → Tag
- **Purpose:** Many-to-Many relationship between Post and Tag
- **Composite Unique:** (`post_id`, `tag_id`)

---

## Key Relationships

### 1. **User → Profile** (One-to-One)
- Each user has exactly one profile
- Created automatically when user is registered
- Contains extended user information

### 2. **User → Post** (One-to-Many)
- A user (author) can create multiple posts
- Each post has exactly one author
- Related name: `blog_posts`

### 3. **User → Comment** (One-to-Many)
- A user can write multiple comments
- Each comment belongs to one user
- Related name: `comments`

### 4. **Category → Post** (One-to-Many)
- A category can contain multiple posts
- Each post belongs to zero or one category (nullable)
- Related name: `posts`
- On category delete: SET_NULL

### 5. **Post ↔ Tag** (Many-to-Many)
- A post can have multiple tags
- A tag can be associated with multiple posts
- Related name: `posts`
- Implemented via junction table `Post_Tags`

### 6. **Post → Comment** (One-to-Many)
- A post can have multiple comments
- Each comment belongs to one post
- Related name: `comments`
- On post delete: CASCADE

---

## Indexes

### Post Table Indexes:
1. **created_at (DESC)**: Optimizes queries for recent posts
2. **status**: Speeds up filtering published vs draft posts

---

## Constraints & Rules

### Delete Behaviors:
- **User deleted** → Profile CASCADE
- **User deleted** → Posts CASCADE
- **User deleted** → Comments CASCADE
- **Category deleted** → Posts SET_NULL
- **Post deleted** → Comments CASCADE
- **Tag deleted** → Post_Tags CASCADE

### Validation Rules:
- **Profile.role**: Must be one of ('reader', 'author', 'admin')
- **Post.status**: Must be one of ('draft', 'published')
- **Category.slug**: Auto-generated from name, must be unique
- **Tag.slug**: Auto-generated from name, must be unique
- **Post.slug**: Auto-generated from title with uniqueness check

### Default Values:
- **Profile.role**: 'reader'
- **Post.status**: 'draft'
- **Post.views**: 0
- **Comment.approved**: True

---

## Database Statistics (After Sample Data)

- **Users**: 3 (admin, author1, reader1)
- **Profiles**: 3 (automatically created)
- **Categories**: 5 (Technology, Lifestyle, Travel, Food, Health)
- **Tags**: 9 (Python, Django, Web Development, etc.)
- **Posts**: 5 (sample blog posts)
- **Comments**: 0 (initially)

---

## SQL Table Names (Django Convention)

```
auth_user                  # Django built-in
accounts_profile           # Custom Profile model
blog_category              # Category model
blog_tag                   # Tag model
blog_post                  # Post model
blog_post_tags             # Many-to-Many junction table
blog_comment               # Comment model
```

---

## Additional Notes

### Auto-generated Fields:
- All `created_at` fields use `auto_now_add=True`
- All `updated_at` fields use `auto_now=True`
- `slug` fields are auto-generated from their respective name/title fields

### Image Storage:
- **Profile avatars**: `media/avatars/`
- **Post featured images**: `media/post_images/`
- **CKEditor uploads**: `media/uploads/`

### Ordering:
- **Categories**: Alphabetically by name
- **Tags**: Alphabetically by name
- **Posts**: Newest first (descending created_at)
- **Comments**: Newest first (descending created_at)

---

## Entity Relationship Summary

```
User (1) ←→ (1) Profile
User (1) ←→ (N) Post
User (1) ←→ (N) Comment
Category (1) ←→ (N) Post
Post (N) ←→ (N) Tag
Post (1) ←→ (N) Comment
```

**Total Tables**: 7  
**Total Relationships**: 6  
**Many-to-Many Relations**: 1 (Post ↔ Tag)  
**One-to-Many Relations**: 4  
**One-to-One Relations**: 1 (User ↔ Profile)

---

## How to View This Diagram

To view the Mermaid diagram:
1. Open this file in GitHub (it will render automatically)
2. Use a Mermaid preview extension in VS Code
3. Use online tools like https://mermaid.live/
4. Use tools like draw.io to import the relationships
