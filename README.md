# Система резервирования времени подъезда к пункту пропуска
Общее описание
1. API-сервис для системы резервирования времени проезда: API-сервис предоставляет набор API для бронирования пользователями времени проезда через пункт пропуска. Обрабатывает HTTP-запросы, взаимодействует с базой данных для управления расписанием и резервированием времени проезда. Также взаимодействует с внешними системами для уведомлений.

2. Сервис управления расписанием: отвечает за управление расписанием проезда. Обрабатывает запросы от API-сервиса для блокировки и освобождения времени проезда, обновляет расписание в базе данных.

3. Сервис обработки данных: Сервис обработки данных отвечает за анализ и обработку данных о бронированиях (резервировании времени). Выполняет операции по агрегации данных, подсчету статистики, генерации отчетов и прогнозированию бронирований.

4. Веб-интерфейс для резервирования времени проезда: Веб-интерфейс предоставляет ининтерфейс для пользователей (посетителей) для резервирования времени проезда через пункт пропуска. Позволяет просматривать доступные временные слоты, выбирать удобное время и подтверждать бронирование, а также удалять (отменять) и переносить время бронирования.

# Техническое описание
Система состоит из трех сервисов: API-сервиса, сервиса обработки данных и веб-интерфейса. Каждый сервис работает в своем отдельном контейнере, который запускается внутри Kubernetes.

Основные сервисы:

1. API-сервис для системы резервирования времени проезда:
Компоненты: Deployment, Service, ConfigMap, Secret
Образ: reservation-api-service:v1
Назначение: предоставляет API для взаимодействия с системой резервирования времени проезда, обрабатывает HTTP-запросы, взаимодействует с базой данных и системой управления расписанием.
Deployment: Определяет шаблон подов для API-сервиса. Управляет запуском и масштабированием экземпляров подов в кластере. Настроен с requests и limits.
Service: Обеспечивает устойчивый доступ к API-сервису внутри кластера. Маршрутизирует входящие запросы к API-сервису по его имени.
ConfigMap: Хранит конфигурационные данные для API-сервиса.
Secret: Хранит конфиденциальные данные, такие как токены, пароли или ключи шифрования, используемые для аутентификации или других операций.

2. Сервис управления расписанием:
Компоненты: Deployment, Job, ConfigMap
Образ: schedule-management-service:v1
Назначение: отвечает за управление расписанием проезда. Обрабатывает запросы от API-сервиса для блокировки и освобождения времени проезда, обновляет расписание в базе данных.
Deployment: Определяет шаблон подов для сервиса управления расписанием. Управляет запуском и масштабированием экземпляров подов.
Job: Определяет задачу для сервиса управления расписанием. Job обеспечивает запуск задач и контроль их выполнения.
ConfigMap: Хранит конфигурационные данные для сервиса управления расписанием.

3. Веб-интерфейс для резервирования времени проезда:
Компоненты: Deployment, Service, Ingress
Образ: reservation-web-interface:v1
Назначение: предоставляет интерфейс для пользователей (посетителей) для резервирования времени проезда через пункт пропуска. Позволяет просматривать доступные временные слоты, выбирать удобное время и подтверждать бронирование.
Deployment: Определяет шаблон подов для веб-интерфейса. Управляет экземплярами подов веб-интерфейса, позволяя масштабировать и обновлять его по необходимости.
Service: Обеспечивает доступ к веб-интерфейсу с помощью внутренней сети Kubernetes. Service маршрутизирует входящие запросы к веб-интерфейсу по имени сервиса.
Ingress: Обеспечивает управление внешним доступом к веб-интерфейсу. Настроен для маршрутизации входящих запросов к веб-интерфейсу.

4. Сервис обработки данных:

Компоненты: Deployment, Job, CronJob, ConfigMap
Образ: data-processing-service:v1
Назначение: обрабатывает данные, выполняет вычисления и операции над ними в фоновом режиме. Регулярно запускает задачи для обработки данных.
Deployment: Определяет шаблон подов для сервиса обработки данных. Управляет запуском и масштабированием экземпляров подов.
Job: Определяет задачу для сервиса обработки данных. Job обеспечивает запуск задач и контроль их выполнения.
CronJob: Запускает задачу обработки данных периодически с использованием образа data-processing-service:v1.
ConfigMap: Хранит конфигурационные данные для сервиса обработки данных.

**Внешние зависимости (вне K8s):**
1. Сервис базы данных: API-сервис использует базу данных для хранения информации о бронироаниях, клиентах и других сущностях.

База данных:
- Порт: 5432
- Сервер: db.example.com
- Системные требования: 2 CPU, 6GB RAM, 150GB дисковое пространство

2. REST сервисы: API-сервис взаимодействует с REST сервисами платежных шлюзов для обработки онлайн-платежей и с сервисами доставки для отслеживания статуса доставок.

Сервис 1: Сервис аутентификации и авторизации пользователей. Может обрабатывать запросы на регистрацию, вход, обновление пароля и другие операции, связанные с безопасностью и идентификацией пользователей.

Сервис 1 (Сервис аутентификации и авторизации пользователей):
- Порт: 8000
- Сервер: auth-service.example.com
- Системные требования: 1 CPU, 4GB RAM, 40GB дискового пространства

Сервис 2: Сервис для управления расписанием проезда. Он может предоставлять функциональность по планированию и организации времени проезда через пункты пропуска. Такие как: Блокировка временных слотов, Выделение временных слотов для специальных случаев, Гибкость в управлении расписанием.

Сервис 2:
- Порт: 8080
- Сервер: schedule-service.example.com
- Системные требования: 1 CPU, 2GB RAM, 20GB дискового пространства

3. Очередь сообщений.
API-сервис использует очередь сообщений для выполнения следующих задач:
  - Асинхронная Обработка Задач:
  API-сервис может отправлять сообщения в очередь для обработки различных задач, таких как обработка платежей, обновление статистики, отправка уведомлений и других фоновых операций.
Это позволяет API-сервису продолжать обрабатывать запросы от пользователей без блокировки на длительные операции.
  - Повышение Отказоустойчивости:
  При использовании очереди сообщений для фоновой обработки, система становится более отказоустойчивой. Если, например, какая-то задача в очереди завершится с ошибкой, она не блокирует основной поток обработки запросов.
  - Улучшение Производительности:
  Операции, которые могут занять много времени, могут быть перемещены в фоновую обработку, что позволяет API-сервису быть более отзывчивым к запросам пользователей.
Например, генерация отчетов, обновление статистики и другие тяжеловесные операции могут быть перенесены в фоновую очередь.
  - Балансировка Нагрузки:
  Очередь сообщений может служить инструментом для балансировки нагрузки в системе. Операции обработки, которые могут быть распределены во времени, могут быть равномерно распределены с использованием очереди.

Очередь сообщений:
  - Порт: 5672
  - Сервер: messaging.example.com
  - Системные требования: 1 CPU, 4GB RAM, 20GB дисковое пространство

## Диаграмма системы:

![system_diagram_](https://github.com/strahOFF-87/DataStorageSystems_HW2/assets/147749583/b16a9a10-496c-4950-9a94-a1c765ef26ee)


