
class SymmetricMatrix(object):

    def __init__(self, vector):
        """ Representation of a symmetric matrix
        :param vector: elements within upper triangle of a symmetric matrix
        """

        acum = 0
        count = 0
        vector_length = len(vector)

        # Checks if it's a square matrix and calculate the dim
        while acum < vector_length:
            count += 1
            acum += count

            if acum > vector_length:
                raise AttributeError('Not a square matrix')

        self.vector = vector
        self.dim = count

    def element_at(self, i, j):
        if i < j:
            internal_i = i
            internal_j = j
        else:
            internal_i = j
            internal_j = i

        index = self.__index_at(internal_i, internal_j)

        return self.vector[index]

    def __index_at(self, i, j):
        return int(i * self.dim) - int(i * (i + 1) / 2) + j

