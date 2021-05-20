import typing as t
from dataclasses import dataclass


@dataclass
class Harper:
    rank: int
    name: str
    chat_id: int


all_harpers: t.List[Harper] = list()


def is_present(id: int) -> bool:
    all_with_id = list(filter(lambda x: x.chat_id == id, all_harpers))
    return len(all_with_id) > 0


def get_name(id: int) -> t.Optional[str]:
    if harper := get_harper(id):
        return harper.name
    return None


def change_harper_name(id: int, name: str) -> None:
    for harper in all_harpers:
        if harper.chat_id == id:
            harper.name = name


def remove_harper(id: int) -> None:
    for harper in all_harpers:
        if harper.chat_id == id:
            all_harpers.remove(harper)
            return


def add_harper(harper: Harper) -> None:
    all_harpers.append(harper)


def all_harper_ids() -> t.List[int]:
    return [harper.chat_id for harper in all_harpers]


def get_harper(id: int) -> t.Optional[Harper]:
    for harper in all_harpers:
        if harper.chat_id == id:
            return harper
    return None
