import os

TASKS_FILE = "tasks.txt"

# загрузка задач из файла
def load_tasks():
    tasks = {}
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            for line in file:
                task_data = line.strip().split("|")      
                if len(task_data) == 5:
                    task_id = int(task_data[0])
                    tasks[task_id] = {
                        "title": task_data[1],
                        "description": task_data[2],
                        "priority": task_data[3],
                        "status": task_data[4]
                    }
    return tasks

# сохранения задач в файл
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        for task_id, task in tasks.items():
            file.write(f"{task_id}|{task['title']}|{task['description']}|{task['priority']}|{task['status']}\n")

# создания новой задачи
def create_task(tasks):
    task_id = max(tasks.keys(), default=0) + 1
    title = input("Введите название задачи: ")
    description = input("Введите описание задачи: ")

    while True:
        priority = input("Введите приоритет задачи (1 - низкий, 2 - средний, 3 - высокий): ")
        if priority in ['1', '2', '3']:
            break
        else:
            print("Неверный ввод. Попробуйте снова.")

    while True:
        status = input("Введите статус задачи (1 - новая, 2 - в процессе, 3 - завершена): ")
        if status in ['1', '2', '3']:
            break
        else:
            print("Неверный ввод. Попробуйте снова.")

    tasks[task_id] = {
        "title": title,
        "description": description,
        "priority": {'1': 'низкий', '2': 'средний', '3': 'высокий'}[priority],
        "status": {'1': 'новая', '2': 'в процессе', '3': 'завершена'}[status]
    }
    save_tasks(tasks)
    print(f"Задача с ID {task_id} создана!")

# отображения задач
def display_tasks(tasks, sort_key=None):
    if not tasks:
        print("Задач нет.")
        return
    
    sorted_tasks = list(tasks.items())
    if sort_key == "priority":
        sorted_tasks.sort(key=lambda x: x[1]['priority'])
    elif sort_key == "status":
        sorted_tasks.sort(key=lambda x: x[1]['status'])
    
    for task_id, task in sorted_tasks:
        print(f"ID: {task_id} | Название: {task['title']} | Описание: {task['description']} | "
              f"Приоритет: {task['priority']} | Статус: {task['status']}")

# поиск задач
def search_tasks(tasks, query):
    results = [task for task in tasks.values() if query.lower() in task['title'].lower() or query.lower() in task['description'].lower()]
    if results:
        for task in results:
            print(f"Название: {task['title']} | Описание: {task['description']} | "
                  f"Приоритет: {task['priority']} | Статус: {task['status']}")
    else:
        print("Задачи не найдены.")

# обновления задачи
def update_task(tasks):
    task_id = int(input("Введите ID задачи для обновления: "))
    if task_id not in tasks:
        print(f"Задачи с ID {task_id} не существует.")
        return

    print("Что вы хотите обновить?")
    print("1 - Название")
    print("2 - Описание")
    print("3 - Приоритет")
    print("4 - Статус")

    choice = input("Введите номер поля для обновления: ")
    
    if choice == '1':
        tasks[task_id]['title'] = input("Введите новое название задачи: ")
    elif choice == '2':
        tasks[task_id]['description'] = input("Введите новое описание задачи: ")
    elif choice == '3':
        while True:
            priority = input("Введите новый приоритет задачи (1 - низкий, 2 - средний, 3 - высокий): ")
            if priority in ['1', '2', '3']:
                tasks[task_id]['priority'] = {'1': 'низкий', '2': 'средний', '3': 'высокий'}[priority]
                break
            else:
                print("Неверный ввод. Попробуйте снова.")
    elif choice == '4':
        while True:
            status = input("Введите новый статус задачи (1 - новая, 2 - в процессе, 3 - завершена): ")
            if status in ['1', '2', '3']:
                tasks[task_id]['status'] = {'1': 'новая', '2': 'в процессе', '3': 'завершена'}[status]
                break
            else:
                print("Неверный ввод. Попробуйте снова.")
    else:
        print("Неверный выбор.")
        return

    save_tasks(tasks)
    print(f"Задача с ID {task_id} обновлена.")

# удаления задачи
def delete_task(tasks):
    task_id = int(input("Введите ID задачи для удаления: "))
    if task_id in tasks:
        del tasks[task_id]
        save_tasks(tasks)
        print(f"Задача с ID {task_id} удалена.")
    else:
        print(f"Задачи с ID {task_id} не существует.")

# интерфейс программы
def main():
    tasks = load_tasks()

    while True:
        print("\nМеню:")
        print("1 - Создать новую задачу")
        print("2 - Просмотреть задачи")
        print("3 - Обновить задачу")
        print("4 - Удалить задачу")
        print("0 - Выйти из программы")

        choice = input("Введите команду: ")

        if choice == '1':
            create_task(tasks)
        elif choice == '2':
            print("1 - Отобразить задачи в изначальном виде")
            print("2 - Отсортировать по статусу")
            print("3 - Отсортировать по приоритету")
            print("4 - Поиск по названию или описанию")
            sub_choice = input("Введите команду: ")

            if sub_choice == '1':
                display_tasks(tasks)
            elif sub_choice == '2':
                display_tasks(tasks, sort_key="status")
            elif sub_choice == '3':
                display_tasks(tasks, sort_key="priority")
            elif sub_choice == '4':
                query = input("Введите строку для поиска: ")
                search_tasks(tasks, query)
            else:
                print("Неверный ввод.")
        elif choice == '3':
            update_task(tasks)
        elif choice == '4':
            delete_task(tasks)
        elif choice == '0':
            print("Выход из программы.")
            break
        else:
            print("Неверный ввод. Попробуйте снова.")

if __name__ == "__main__":
    main()