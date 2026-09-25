# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Лабораторные работы II - Валидация данных с Pydantic v2
#
# В этой лабе вы познакомитесь с Pydantic v2 - современной библиотекой для валидации данных в Python.
#
# **Зачем это нужно для ML?**
# - Валидация конфигураций экспериментов
# - Проверка входных данных моделей
# - Сериализация/десериализация настроек
# - Типизация в FastAPI (для деплоя моделей)
#
# **Pydantic v2** - это стандарт де-факто в Python-экосистеме (FastAPI, LangChain, MLflow)
#
# **Время выполнения:** 1-1.5 часа
#
# **Установка:**
# ```bash
# pip install pydantic
# ```

# %% [markdown]
# ## Секция 1: Введение в Pydantic v2 (15 мин)
#
# ### Базовая концепция
#
# Pydantic использует **Python type hints** для автоматической валидации данных. Вы описываете схему данных через класс, а Pydantic проверяет соответствие.
#
# **Основные преимущества:**
# - Автоматическая валидация типов
# - Понятные сообщения об ошибках
# - Поддержка JSON
# - Интеграция с IDE (автодополнение)
#
# ### Первая модель
#
# Начнем с простой модели для описания ML-эксперимента:

# %%
from pydantic import BaseModel, Field, ValidationError
from typing import Dict, List


# %%
# Создаем первую модель
class MLExperiment(BaseModel):
    """Модель для описания ML-эксперимента."""
    name: str
    accuracy: float
    epochs: int

# Создаем экземпляр
experiment = MLExperiment(
    name="Logistic Regression",
    accuracy=0.85,
    epochs=100
)

print(f"Эксперимент: {experiment.name}")
print(f"Точность: {experiment.accuracy}")
print(f"Эпохи: {experiment.epochs}")

# %% [markdown]
# ### Автоматическая валидация и приведение типов
#
# Pydantic автоматически приводит типы, если это возможно:

# %%
# Автоматическое приведение типов
exp1 = MLExperiment(
    name="Random Forest",  # str
    accuracy="0.92",        # str -> float (автоматически)
    epochs="50"             # str -> int (автоматически)
)

print(f"Тип accuracy: {type(exp1.accuracy)}")
print(f"Значение accuracy: {exp1.accuracy}")
print(f"Тип epochs: {type(exp1.epochs)}")
print(f"Значение epochs: {exp1.epochs}")

# %% [markdown]
# ### Обработка ошибок валидации
#
# Когда данные не соответствуют типу, Pydantic выбрасывает `ValidationError`:

# %%
try:
    # Невозможно преобразовать строку в float
    bad_exp = MLExperiment(
        name="Bad Model",
        accuracy="high",      # Error!
        epochs=100
    )
except ValidationError as e:
    print("Ошибка валидации:")
    print(e)


# %% [markdown]
# ### Сравнение с dataclasses
#
# **Dataclasses (из lab1):**
# - Только хранение данных
# - Нет автоматической валидации
# - Нет приведения типов
#
# **Pydantic:**
# - Автоматическая валидация
# - Приведение типов
# - Сообщения об ошибках
# - JSON сериализация/десериализация

# %% [markdown]
# ## Секция 2: Валидация и Field (30 мин)
#
# ### Стандартные типы данных
#
# Pydantic поддерживает все стандартные типы Python:

# %%
class DetailedExperiment(BaseModel):
    """Расширенная модель эксперимента."""
    name: str                    # Строка
    accuracy: float              # Число с плавающей точкой
    epochs: int                  # Целое число
    is_production: bool          # Булево значение
    tags: list[str]              # Список строк (Pydantic v2 синтаксис)
    metrics: dict[str, float]    # Словарь: метрика -> значение

# Создаем экземпляр
detailed_exp = DetailedExperiment(
    name="Neural Network",
    accuracy=0.95,
    epochs=1000,
    is_production=True,
    tags=["deep-learning", "classification"],
    metrics={"precision": 0.93, "recall": 0.89, "f1": 0.91}
)

print(f"Теги: {detailed_exp.tags}")
print(f"Метрики: {detailed_exp.metrics}")
print(f"F1-score: {detailed_exp.metrics['f1']}")


# %% [markdown]
# ### Использование Field() для ограничений
#
# `Field()` позволяет добавить ограничения на значения:

# %%
class ValidatedExperiment(BaseModel):
    """Модель с валидацией полей."""
    
    # accuracy должен быть от 0 до 1
    accuracy: float = Field(ge=0.0, le=1.0, description="Точность модели от 0 до 1")
    
    # epochs должен быть >= 1
    epochs: int = Field(ge=1, description="Количество эпох (минимум 1)")
    
    # learning_rate должен быть положительным
    learning_rate: float = Field(gt=0.0, description="Learning rate (строго > 0)")
    
    # batch_size должен быть >= 1
    batch_size: int = Field(ge=1, description="Размер батча")
    
    name: str = Field(min_length=1, description="Название модели")

# Валидный пример
valid_exp = ValidatedExperiment(
    name="Valid Model",
    accuracy=0.87,
    epochs=50,
    learning_rate=0.001,
    batch_size=32
)
print(f"Валидный эксперимент создан: {valid_exp.name}")

# %%
# Примеры ошибок валидации
test_cases = [
    {
        "name": "Negative accuracy",
        "data": {"name": "Bad", "accuracy": -0.5, "epochs": 10, "learning_rate": 0.01, "batch_size": 32}
    },
    {
        "name": "Accuracy > 1",
        "data": {"name": "Bad", "accuracy": 1.5, "epochs": 10, "learning_rate": 0.01, "batch_size": 32}
    },
    {
        "name": "Zero epochs",
        "data": {"name": "Bad", "accuracy": 0.8, "epochs": 0, "learning_rate": 0.01, "batch_size": 32}
    },
    {
        "name": "Negative learning rate",
        "data": {"name": "Bad", "accuracy": 0.8, "epochs": 10, "learning_rate": -0.01, "batch_size": 32}
    },
    {
        "name": "Zero batch size",
        "data": {"name": "Bad", "accuracy": 0.8, "epochs": 10, "learning_rate": 0.01, "batch_size": 0}
    }
]

for case in test_cases:
    try:
        ValidatedExperiment(**case["data"])
        print(f"❌ {case['name']}: Ошибка не поймана!")
    except ValidationError as e:
        print(f"✓ {case['name']}: Ошибка валидации поймана")
        print(f"  Детали: {e.errors()[0]['msg']}")


# %% [markdown]
# ### Вложенные модели
#
# Pydantic поддерживает вложенные модели для сложных структур данных:

# %%
class DatasetConfig(BaseModel):
    """Конфигурация датасета."""
    name: str
    train_size: float = Field(ge=0.0, le=1.0)
    test_size: float = Field(ge=0.0, le=1.0)
    random_state: int = Field(ge=0)

class FullExperiment(BaseModel):
    """Полная конфигурация эксперимента."""
    name: str
    dataset: DatasetConfig  # Вложенная модель
    accuracy: float = Field(ge=0.0, le=1.0)
    epochs: int = Field(ge=1)

# Создаем экземпляр со вложенной моделью
full_exp = FullExperiment(
    name="Full Pipeline",
    dataset={
        "name": "Titanic",
        "train_size": 0.8,
        "test_size": 0.2,
        "random_state": 42
    },
    accuracy=0.82,
    epochs=100
)

print(f"Эксперимент: {full_exp.name}")
print(f"Датасет: {full_exp.dataset.name}")
print(f"Train size: {full_exp.dataset.train_size}")
print(f"Random state: {full_exp.dataset.random_state}")


# %% [markdown]
# ### 🎯 Задание 1: Создать модель MLExperiment с валидацией
#
# Создайте Pydantic модель `MLExperiment` со следующими полями:
#
# 1. **model_name** (`str`): название модели
# 2. **accuracy** (`float`): точность от 0 до 1 (используйте `Field` с ограничениями)
# 3. **epochs** (`int`): количество эпох, минимум 1
# 4. **hyperparameters** (`dict[str, float]`): словарь с гиперпараметрами
# 5. **metrics** (`list[str]`): список названий метрик
#
# **Требования:**
# - Добавьте валидацию для всех числовых полей через `Field()`
# - Создайте 2-3 валидных примера
# - Попробуйте создать невалидный пример и обработайте ошибку

# %%
#TODO

class MLExperiment(BaseModel):
    """Ваша модель ML-эксперимента."""
    pass  # Уберите pass и реализуйте модель

# Тестовые примеры
# experiment1 = MLExperiment(...)
# experiment2 = MLExperiment(...)
# ... 


# %% [markdown]
# ## Секция 3: JSON и конфигурация ML-модели (45 мин)
#
# ### Сериализация и десериализация
#
# Pydantic предоставляет удобные методы для работы с JSON:

# %%
class ExperimentConfig(BaseModel):
    """Конфигурация эксперимента."""
    model_name: str
    learning_rate: float = Field(gt=0)
    batch_size: int = Field(ge=1)
    epochs: int = Field(ge=1)

# Создаем конфигурацию
config = ExperimentConfig(
    model_name="LogisticRegression",
    learning_rate=0.01,
    batch_size=32,
    epochs=100
)

print("=== Исходная конфигурация ===")
print(f"Модель: {config.model_name}")
print(f"Learning rate: {config.learning_rate}")

# %% [markdown]
# ### model_dump() и model_dump_json()

# %%
# Преобразование в словарь
config_dict = config.model_dump()
print("\n=== model_dump() - словарь ===")
print(config_dict)
print(f"Тип: {type(config_dict)}")

# Преобразование в JSON строку
config_json = config.model_dump_json()
print("\n=== model_dump_json() - JSON строка ===")
print(config_json)
print(f"Тип: {type(config_json)}")

# %% [markdown]
# ### model_validate() - восстановление из словаря

# %%
# Восстановление из словаря
config_dict = {
    "model_name": "RandomForest",
    "learning_rate": 0.001,
    "batch_size": 64,
    "epochs": 200
}

restored_config = ExperimentConfig.model_validate(config_dict)
print("=== Восстановленная конфигурация ===")
print(f"Модель: {restored_config.model_name}")
print(f"Learning rate: {restored_config.learning_rate}")
print(f"Batch size: {restored_config.batch_size}")
print(f"Эпохи: {restored_config.epochs}")

# %% [markdown]
# ### Сохранение и загрузка конфигурации в файл

# %%
import json
from pathlib import Path

# Создаем конфигурацию
config = ExperimentConfig(
    model_name="SVM",
    learning_rate=0.1,
    batch_size=16,
    epochs=150
)

# Сохраняем в файл
config_path = Path("experiment_config.json")
config_json = config.model_dump_json()
config_path.write_text(config_json)

print("=== Конфигурация сохранена в файл ===")
print(f"Содержимое файла:\n{config_path.read_text()}")

# %%
# Загружаем из файла
loaded_json = config_path.read_text()
loaded_config = ExperimentConfig.model_validate_json(loaded_json)

print("=== Конфигурация загружена из файла ===")
print(f"Модель: {loaded_config.model_name}")
print(f"Learning rate: {loaded_config.learning_rate}")
print(f"Batch size: {loaded_config.batch_size}")
print(f"Эпохи: {loaded_config.epochs}")


# %% [markdown]
# ### Полная система конфигурации ML-модели
#
# Теперь создадим полную систему конфигурации с вложенными моделями:

# %%
class ModelConfig(BaseModel):
    """Конфигурация модели."""
    model_type: str = Field(description="Тип модели (logistic_regression, random_forest, etc.)")
    penalty: str | None = Field(default=None, description="Тип регуляризации (l1, l2, etc.)")
    C: float = Field(default=1.0, gt=0, description="Параметр регуляризации")

class TrainingConfig(BaseModel):
    """Конфигурация обучения."""
    max_iter: int = Field(default=100, ge=1, description="Максимальное количество итераций")
    learning_rate: float = Field(default=0.001, gt=0, description="Learning rate")
    batch_size: int | None = Field(default=None, ge=1, description="Размер батча (None для полного градиента)")

class FullConfig(BaseModel):
    """Полная конфигурация эксперимента."""
    model: ModelConfig
    training: TrainingConfig
    experiment_name: str
    random_state: int = Field(default=42, ge=0)

# Создаем полную конфигурацию
full_config = FullConfig(
    experiment_name="Titanic Classification",
    model={
        "model_type": "logistic_regression",
        "penalty": "l2",
        "C": 0.5
    },
    training={
        "max_iter": 200,
        "learning_rate": 0.01,
        "batch_size": 32
    }
)

print("=== Полная конфигурация ===")
print(f"Эксперимент: {full_config.experiment_name}")
print(f"Модель: {full_config.model.model_type}")
print(f"Регуляризация: {full_config.model.penalty}")
print(f"C: {full_config.model.C}")
print(f"Макс. итераций: {full_config.training.max_iter}")
print(f"Learning rate: {full_config.training.learning_rate}")
print(f"Batch size: {full_config.training.batch_size}")

# %% [markdown]
# ### Сохранение и загрузка полной конфигурации

# %%
# Сохраняем полную конфигурацию
full_config_path = Path("full_config.json")
full_config_path.write_text(full_config.model_dump_json(indent=2))

print("=== Полная конфигурация сохранена ===")
print(full_config_path.read_text())

# %%
# Загружаем полную конфигурацию
loaded_full_config = FullConfig.model_validate_json(full_config_path.read_text())

print("=== Полная конфигурация загружена ===")
print(f"Эксперимент: {loaded_full_config.experiment_name}")
print(f"Тип модели: {loaded_full_config.model.model_type}")
print(f"Параметры модели: penalty={loaded_full_config.model.penalty}, C={loaded_full_config.model.C}")
print(f"Параметры обучения: max_iter={loaded_full_config.training.max_iter}, lr={loaded_full_config.training.learning_rate}")

# %% [markdown]
# ### 🎯 Финальное задание: Конфигурация для логистической регрессии
#
# Создайте полную систему конфигурации для обучения логистической регрессии:
#
# 1. **ModelConfig**:
#    - `model_type: str` - тип модели (всегда "logistic_regression")
#    - `penalty: str | None` - тип регуляризации ("l1", "l2", "elasticnet" или None)
#    - `C: float` - параметр регуляризации (должен быть > 0)
#    - `l1_ratio: float | None` - параметр для elasticnet (от 0 до 1, если используется elasticnet)
#
# 2. **TrainingConfig**:
#    - `max_iter: int` - максимальное количество итераций (минимум 1)
#    - `learning_rate: float` - learning rate (должен быть > 0)
#    - `batch_size: int | None` - размер батча (минимум 1, или None для полного градиента)
#    - `early_stopping: bool` - использовать ли early stopping
#
# 3. **FullConfig**:
#    - `model: ModelConfig` - конфигурация модели
#    - `training: TrainingConfig` - конфигурация обучения
#    - `experiment_name: str` - название эксперимента
#    - `random_state: int` - random state (для воспроизводимости)
#
# **Требования:**
# 1. Добавьте валидацию для всех полей через `Field()`
# 2. Создайте 2 разные конфигурации:
#    - С L2 регуляризацией
#    - С elasticnet регуляризацией
# 3. Сохраните обе конфигурации в JSON файлы
# 4. Загрузите их обратно и убедитесь, что данные совпадают
# 5. Попробуйте создать невалидную конфигурацию и обработайте ошибку

# %%
#TODO

from pathlib import Path

# 1. Определите модели ModelConfig, TrainingConfig, FullConfig

# 2. Создайте конфигурацию с L2 регуляризацией
config_l2 = None  #TODO

# 3. Создайте конфигурацию с elasticnet регуляризацией
config_elasticnet = None  #TODO

# 4. Сохраните конфигурации в файлы
# Path("config_l2.json").write_text(...)
# Path("config_elasticnet.json").write_text(...)

# 5. Загрузите конфигурации из файлов
# loaded_l2 = ...
# loaded_elasticnet = ...

# 6. Проверьте, что данные совпадают
# assert ...

print("Ваша реализация:")
print(f"Config L2: {config_l2}")
print(f"Config ElasticNet: {config_elasticnet}")

# %% [markdown]
# ## Резюме
#
# Вы познакомились с основами Pydantic v2:
#
# ✅ **Секция 1**: Базовые модели и автоматическая валидация
# - Создание моделей через `BaseModel`
# - Автоматическое приведение типов
# - Обработка ошибок валидации
#
# ✅ **Секция 2**: Валидация и Field
# - Использование `Field()` для ограничений
# - Вложенные модели
# - Сложные типы (list, dict)
#
# ✅ **Секция 3**: JSON и конфигурации
# - `model_dump()` и `model_dump_json()`
# - `model_validate()` для восстановления
# - Сохранение и загрузка конфигураций
#
# ### Где это пригодится:
# - **Lab 2-d (Titanic)**: Валидация параметров модели
# - **Lab 3-6**: Конфигурация ML-экспериментов
# - **Production**: FastAPI для деплоя моделей
# - **MLOps**: MLflow, LangChain и другие инструменты

# %% [markdown]
# ## Дополнительные ресурсы
#
# - [Документация Pydantic v2](https://docs.pydantic.dev/latest/)
# - [Pydantic FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/body-fields/)
# - [Pydantic vs Dataclasses](https://docs.pydantic.dev/latest/concepts/dataclasses/)
#
# **Следующие шаги:**
# - Изучить Validators для кастомной валидации
# - GenericModels для параметризованных типов
# - JSON Schema для генерации документации
