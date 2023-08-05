import pytest
from ...matrix.Matrix import Matrix

def test_checkIdentiy():
    matrix_identity = Matrix([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
    matrix_2 = Matrix([[3,6,7,8],[9,1,2,0],[5,2,1,0],[2,2,1,1]])

    new_matrix = matrix_identity + matrix_2

    assert new_matrix == matrix_2

def test_checkSum():
    matrix_identity = Matrix([[1,1,2,3],[7,8,2,0],[4,3,2,1],[1,2,3,4]])
    matrix_2 = Matrix([[3,6,7,8],[9,1,2,0],[5,2,1,0],[2,2,1,1]])

    new_matrix = matrix_identity + matrix_2

    assert new_matrix.array == [[4,7,9,11],[16,9,4,0],[9,5,3,1],[3,4,4,5]]

def test_checkCorrectShape():
    with pytest.raises(AssertionError):
        matrix_identity = Matrix([[1,1,2,3],[7,8,2,0],[4,3,2,1],[1,2,3,4]])
        matrix_2 = Matrix([[3,6,7,8],[9,1,2,0],[5,2,1,0]])
        new_matrix = matrix_identity + matrix_2
