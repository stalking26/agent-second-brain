import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Конфигурация
VAULT_PATH = "../vault"
WATCH_DIRS = [
    ".claude/tasks_inbox",
    "вводные_данные",
    "мысли/идеи"
]

TAGS_TO_ACTIONS = {
    "#action/analyze": "analyze_tasks",
    "#ai/research": "start_research",
}

class VaultHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".md"):
            self.process_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(".md"):
            self.process_file(event.src_path)

    def process_file(self, file_path):
        print(f"Обнаружен файл: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            for tag, action in TAGS_TO_ACTIONS.items():
                if tag in content:
                    self.trigger_action(action, file_path)
        except Exception as e:
            print(f"Ошибка при чтении файла {file_path}: {e}")

    def trigger_action(self, action, file_path):
        print(f"Триггер: {action} для файла {file_path}")
        # Здесь будет вызов Claude CLI или внутреннего процессора
        # Пример: subprocess.run(["claude", "do", f"Выполни {action} для {file_path}"])
        pass

if __name__ == "__main__":
    event_handler = VaultHandler()
    observer = Observer()
    
    # Мониторим каждую директорию из списка
    for d in WATCH_DIRS:
        path = os.path.join(VAULT_PATH, d)
        if os.path.exists(path):
            observer.schedule(event_handler, path, recursive=False)
            print(f"Мониторинг запущен для: {path}")
        else:
            print(f"Предупреждение: Директория не найдена: {path}")

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
