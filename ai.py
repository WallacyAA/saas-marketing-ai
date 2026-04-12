from fastapi import APIRouter
from pydantic import BaseModel
from database import SessionLocal
from models import Post

router = APIRouter()

class PostRequest(BaseModel):
    topic: str

@router.post("/generate-post")
def generate_post(data: PostRequest):
    
    db = SessionLocal()

    post_content = f"""
🦷 Dica do dia sobre {data.topic}!

Manter bons hábitos é essencial para sua saúde.

✅ Escove os dentes após as refeições  
✅ Use fio dental diariamente  
✅ Visite seu dentista regularmente  

Cuide do seu sorriso 😁✨
"""

    new_post = Post(content=post_content, clinic_id=1)

    db.add(new_post)
    db.commit()
    db.close()

    return {"post": post_content}