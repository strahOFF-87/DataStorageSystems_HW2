# Установка библиотеки Graphviz
!pip install graphviz

# Импорт необходимых библиотек
from google.colab import drive
import graphviz

# Подключение Google Drive
drive.mount('/content/drive/')

# Создание объекта графа
graph = graphviz.Digraph()

# Добавление узлов (сервисов) в граф
graph.node("API Service")
graph.node("Web Interface")
graph.node("Database")
graph.node("Message Queue")
graph.node("External Service 1")
graph.node("External Service 2")
graph.node("Processing Service")  # Добавление узла для сервиса обработки данных

# Установка связей (ребер) между узлами графа
graph.edge("API Service", "Processing Service")  # Связь между API Service и Processing Service
graph.edge("Processing Service", "Web Interface")
graph.edge("Processing Service", "Database")
graph.edge("Processing Service", "Message Queue")
graph.edge("Web Interface", "External Service 1")
graph.edge("Web Interface", "External Service 2")
graph.edge("Message Queue", "External Service 1")
graph.edge("Message Queue", "External Service 2")

# Отрисовка и сохранение графа в формате PNG в Google Drive
graph.render("/content/drive/MyDrive/system_diagram_", format="png")
