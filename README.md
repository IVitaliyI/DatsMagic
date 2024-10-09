# DatsMagic
Repository for DatsMagic gameton from Dats.Team

Установить зависимости проекта с помощью Poetry: После клонирования проекта, другой разработчик может легко установить все зависимости и настроить виртуальное окружение с помощью команды:
```bash
poetry install
```

Сборка контенера Docker:
```bash
docker build -t datsmagic .
```

Запуск контейнера Docker:
```bash
docker run -p 8080:8080 datsmagic
```
