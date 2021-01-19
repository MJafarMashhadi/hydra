import pytest
from hydra.utils import reflection

def test_find_subclasses():
    class Base(object):
        pass

    class A(Base):
        pass
    class B(Base):
        pass

    class C(B):
        pass
    class D(B):
        pass

    class E(D):
        pass

    assert len(reflection.get_all_subclasses(Base, include_self=True)) == 6
    assert len(reflection.get_all_subclasses(E, include_self=True)) == 1
    assert len(reflection.get_all_subclasses(A, include_self=True)) == 1
    assert len(reflection.get_all_subclasses(B, include_self=True)) == 4

    assert len(reflection.get_all_subclasses(Base)) == 5
    assert len(reflection.get_all_subclasses(E)) == 0
    assert len(reflection.get_all_subclasses(A)) == 0
    assert len(reflection.get_all_subclasses(B)) == 3
