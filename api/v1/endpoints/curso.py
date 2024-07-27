from http import HTTPStatus
from typing import List

from fastapi import APIRouter, status, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.curso_model import CursoModel
from core.deps import get_session

# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass

router = APIRouter()


# Post Course

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CursoModel)
async def post_curso(curso: CursoModel, db: AsyncSession = Depends(get_session)):
    new_curso = CursoModel(titulo=curso.titulo, aulas=curso.aulas, horas=curso.horas)

    db.add(new_curso)
    await db.commit()

    return new_curso


@router.get('/', response_model=List[CursoModel], status_code=status.HTTP_200_OK)
async def get_cursos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel)
        result = await session.execute(query)
        cursos = result.scalars().all()

        return cursos


@router.get('/{curso_id}', response_model=CursoModel, status_code=status.HTTP_200_OK)
async def get_curso(curso_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso = result.scalar_one_or_none()
        if curso:
            return curso
        else:
            raise HTTPException(detail="Curso não encontrado", status_code=HTTPStatus.NOT_FOUND)


@router.put('/{curso_id}', response_model=CursoModel, status_code=status.HTTP_202_ACCEPTED)
async def update_course(curso_id: int, data: CursoModel, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso_up = result.scalar_one_or_none()
        if curso_up:
            curso_up.titulo = data.titulo
            curso_up.aulas = data.aulas
            curso_up.horas = data.horas
            await session.commit()
            return curso_up
        else:
            raise HTTPException(detail="Curso não encontrado", status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{curso_id}',response_model=CursoModel, status_code=status.HTTP_202_ACCEPTED)
async def delete_course(curso_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso_deleted = result.scalar_one_or_none()
        if curso_deleted:
            await session.delete(curso_deleted)
            await session.commit()
            return HTTPStatus.NO_CONTENT
        else:
            raise HTTPException(detail="Curso não encontrado para deletar", status_code=HTTPStatus.NOT_FOUND)
