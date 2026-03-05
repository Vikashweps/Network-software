# saga.py
import requests
from states import next_state

class PizzaSaga:
    def __init__(self, order_id: int, product_id: int, quantity: int, app_url: str):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.app_url = app_url.rstrip('/')
        self.headers = {"X-Order-Id": str(order_id)}

    def _call(self, method: str, path: str, json: dict = None) -> dict:
        url = f"{self.app_url}{path}"
        try:
            resp = requests.request(
                method, 
                url, 
                json=json, 
                headers=self.headers, 
                timeout=5
            )
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def execute(self, orders_db: list) -> dict:
        order = next((o for o in orders_db if o["order_id"] == self.order_id), None)
        if not order:
            order = {"order_id": self.order_id, "product_id": self.product_id, "quantity": self.quantity, "status": "NEW"}
            orders_db.append(order)

        while order["status"] not in ["DONE", "CANCELLED"]:
            state = order["status"]
            
            if state == "NEW":
                res = self._call("POST", f"/products/{self.product_id}/reserve", {"quantity": self.quantity})
                
                if "error" in res:
                    order["status"] = next_state(state, "PAY_FAIL")
                    continue 
        
                import random
                if random.random() < 0.8:
                    order["status"] = next_state(state, "PAY_OK")
                else:
                    order["status"] = next_state(state, "PAY_FAIL")
            
            elif state == "PAID":
                order["status"] = next_state(state, "COMPLETE")
            
            elif state == "CANCELLED":
                self.compensate(orders_db)
                break
        
        return order

    def compensate(self, orders_db: list):
        if getattr(self, '_compensated', False):
            return
        self._compensated = True
        
        order = next((o for o in orders_db if o["order_id"] == self.order_id), None)
        if not order or order["status"] != "CANCELLED":
            return
        
        self._call("POST", f"/products/{self.product_id}/restore", {"quantity": self.quantity})