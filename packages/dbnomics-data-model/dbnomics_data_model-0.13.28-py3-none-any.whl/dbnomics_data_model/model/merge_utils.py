"""Merge utils."""

from itertools import chain
from typing import Callable, Iterable, Iterator, TypeVar

from toolz import groupby

__all__ = ["iter_merged_items"]


T = TypeVar("T")
K = TypeVar("K", bound=str)


def default_merge(a: T, b: T) -> T:
    return a.merge(b)


def default_key(v: T) -> K:
    return v._get_merge_key()


def iter_merged_items(
    current: Iterable[T],
    other: Iterable[T],
    *,
    key: Callable[[T], K] = default_key,
    merge: Callable[[T, T], T] = default_merge,
    sort_by_key: bool = False,
) -> Iterator[T]:
    """Iterate over the items of current merged with `other` matched with `key`.

    If `sort_by_key` is `True`, yield items in the key order.
    Otherwise, items appearing in `current` only or both are yielded first,
    then those only in `other`.
    """
    current = list(current)
    other = list(other)

    groups = groupby(key, chain(current, other))

    def iter_group_keys() -> Iterator[K]:
        current_keys = [key(item) for item in current]
        other_keys = [key(item) for item in other]
        if sort_by_key:
            yield from sorted(set(chain(current_keys, other_keys)))
        else:
            only_other_keys = []
            for item in other:
                other_key = key(item)
                if other_key not in current_keys:
                    only_other_keys.append(other_key)
            yield from chain(current_keys, only_other_keys)

    for group_key in iter_group_keys():
        group = groups[group_key]
        if len(group) == 2:
            item, other_item = group
            yield merge(item, other_item)
        else:
            yield group[0]
