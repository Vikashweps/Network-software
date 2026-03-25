import json
from typing import Any, Dict, Optional, Tuple
import requests

# GraphQL эндпоинт согласно варианту
GRAPHQL_URL = "http://localhost:8246/graphql"


def build_payload(query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Формирует стандартный GraphQL запрос в формате JSON.
    """
    payload = {
        "query": query,
        "variables": variables if variables is not None else {}
    }
    return payload


def execute_query(query: str, variables: Optional[Dict[str, Any]] = None) -> Tuple[Optional[Dict], Optional[list]]:
    """
    Выполняет GraphQL запрос и возвращает данные или ошибки.
    """
    payload = build_payload(query, variables)
    
    try:
        response = requests.post(
            GRAPHQL_URL,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        result = response.json()
        
        # Обработка ошибок
        if "errors" in result and result["errors"]:
            return None, result["errors"]
        
        # Возврат данных
        if "data" in result:
            return result["data"], None
        
        return None, [{"message": "Неизвестный формат ответа"}]
        
    except requests.exceptions.RequestException as e:
        return None, [{"message": f"Ошибка подключения: {str(e)}"}]
    except json.JSONDecodeError as e:
        return None, [{"message": f"Ошибка парсинга JSON: {str(e)}"}]


# GraphQL запросы
QUERY_GET_ALL_DEVICES = """
query {
  devices {
    id
    name
    serial
  }
}
"""

QUERY_GET_DEVICE_BY_ID = """
query GetDevice($id: ID!) {
  device(id: $id) {
    id
    name
    serial
  }
}
"""

MUTATION_CREATE_DEVICE = """
mutation CreateDevice($input: CreateDeviceInput!) {
  createDevice(input: $input) {
    id
    name
    serial
  }
}
"""



# Блок запуска
if __name__ == "__main__":
    print("🚀 GraphQL Клиент — Devices (Week 06)")
    print(f"📍 Эндпоинт: {GRAPHQL_URL}\n")
    
    # 1. Создание устройства (Mutation)
    print(" 1. Создаём устройство...")
    data, errors = execute_query(
        MUTATION_CREATE_DEVICE,
        variables={
            "input": {
                "name": "Router Cisco",
                "serial": "SN-2024-001"
            }
        }
    )
    
    if errors:
        print(" ОШИБКИ:", errors)
    elif data:
        print(" Успешно:", data)
        device_id = data.get('createDevice', {}).get('id')
        
        # 2. Получение списка устройств
        print("\n2. Получаем список устройств...")
        data, errors = execute_query(QUERY_GET_ALL_DEVICES)
        if errors:
            print("ОШИБКИ:", errors)
        elif data:
            print("Успешно:", data)
        
        # 3. Получение по ID
        if device_id:
            print(f"\n 3. Получаем устройство по ID={device_id}...")
            data, errors = execute_query(
                QUERY_GET_DEVICE_BY_ID,
                variables={"id": device_id}
            )
            if errors:
                print(" ОШИБКИ:", errors)
            elif data:
                print(" Успешно:", data)