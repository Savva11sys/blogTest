import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog

DATABASE = 'blog.db'


def init_db():
    """Инициализация базы данных."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        conn.commit()


def add_user(name):
    """Добавление нового пользователя."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (name) VALUES (?)', (name,))
            conn.commit()
            messagebox.showinfo("Успех", f'Пользователь "{name}" успешно добавлен.')
        except sqlite3.IntegrityError:
            messagebox.showwarning("Ошибка", f'Пользователь с именем "{name}" уже существует.')


def add_post(username, content):
    """Добавление нового поста."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE name = ?', (username,))
        user = cursor.fetchone()
        
        if not user:
            cursor.execute('INSERT INTO users (name) VALUES (?)', (username,))
            user_id = cursor.lastrowid
        else:
            user_id = user[0]
        
        cursor.execute('INSERT INTO posts (user_id, content) VALUES (?, ?)', (user_id, content))
        conn.commit()
        messagebox.showinfo("Успех", "Пост успешно добавлен.")


def view_blog():
    """Просмотр всех постов в блоге."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT posts.content, users.name 
            FROM posts 
            INNER JOIN users ON posts.user_id = users.id
        ''')
        posts = cursor.fetchall()
    
    if posts:
        blog_window = tk.Toplevel(root)
        blog_window.title("Все посты")
        blog_window.geometry("400x400")
        blog_text = tk.Text(blog_window, wrap=tk.WORD)
        blog_text.pack(fill=tk.BOTH, expand=True)
        blog_text.insert(tk.END, "--- Список постов ---\n\n")
        for idx, (content, author) in enumerate(posts, start=1):
            blog_text.insert(tk.END, f'{idx}. {author}: {content}\n')
        blog_text.config(state=tk.DISABLED)
    else:
        messagebox.showinfo("Блог пуст", "В блоге пока нет постов.")


def add_user_gui():
    """Окно добавления пользователя."""
    name = simpledialog.askstring("Добавить пользователя", "Введите имя пользователя:")
    if name:
        add_user(name)


def add_post_gui():
    """Окно добавления поста."""
    username = simpledialog.askstring("Добавить пост", "Введите имя пользователя:")
    if username:
        content = simpledialog.askstring("Добавить пост", "Введите текст поста:")
        if content:
            add_post(username, content)




#главное окно
root = tk.Tk()
root.title("Блог")
root.geometry("400x300")
root.resizable(False, False)

#элементы интерфейса
title_label = tk.Label(root, text="Добро пожаловать в блог!", font=("Arial", 16), pady=10)
title_label.pack()

add_user_button = tk.Button(root, text="Добавить пользователя", command=add_user_gui, width=25)
add_user_button.pack(pady=6)

add_post_button = tk.Button(root, text="Добавить пост", command=add_post_gui, width=25)
add_post_button.pack(pady=6)

view_blog_button = tk.Button(root, text="Просмотреть блог", command=view_blog, width=25)
view_blog_button.pack(pady=6)


exit_button = tk.Button(root, text="Выход", command=root.quit, width=25)
exit_button.pack(pady=6)


# Запускаем
if __name__ == '__main__':
    init_db()
    root.mainloop()
