from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# --- Modelo de dados ---
class Item(BaseModel):
    name: str

# --- Dados iniciais ---
items = [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"},
]

# --- Listar todos ---
@app.get("/items")
def get_items():
    return {"items": items}

# --- Obter um item específico ---
@app.get("/items/{item_id}")
def get_item(item_id: int):
    item = next((item for item in items if item["id"] == item_id), None)
    if item:
        return {"item": item}
    raise HTTPException(status_code=404, detail="Item not found")

# --- Criar um novo item ---
@app.post("/items")
def create_item(item: Item):
    new_item = {"id": len(items) + 1, "name": item.name}
    items.append(new_item)
    return {"item": new_item}

# --- Atualizar um item existente ---
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    existing = next((i for i in items if i["id"] == item_id), None)
    if not existing:
        raise HTTPException(status_code=404, detail="Item not found")
    existing["name"] = item.name
    return {"item": existing}

# --- Deletar um item ---
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    global items
    items = [i for i in items if i["id"] != item_id]
    return {"result": True}