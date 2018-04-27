__author__ = 'Fadi Mhanna'


#Represent each 1 in the matrix A as a data object x with five fields L[x], R[x], U[x], D[x], C[x]
class data_object:

    #Create links as data_object type attributes
    def __init__(self, L=None, R=None, U=None, D=None, C=None):
        self.L = L
        self.R = R
        self.U = U
        self.D = D
        self.C = C

#Each column object y contains the fields L[y], R[y], U[y], D[y], and C[y] of a data object and two additional fields, S[y] (“size”) and N[y] (“name”)
class column_object:

    #Create links as column_object type attributes
    def __init__(self, L=None, R=None, U=None, D=None, C=None, S=None, N=None):
        self.L = L
        self.R = R
        self.U = U
        self.D = D
        self.C = C
        self.S = S
        self.N = N

def create_column_object_links(matrix_A, column_object_list):

    #Create special column object called root, h
    previous = root = column_object()
    column_object_list.append(root)

    #Create L and R links for column objects
    for column in range(len(matrix_A[0])):
        current_column = column_object()
        column_object_list.append(current_column)
        current_column.L = previous
        previous.R = current_column
        previous = current_column
    current_column.R = root
    root.L = current_column

def create_data_object_links(matrix_A, data_object_list, column_object_list):
    
    #Populate data_object_list matrix and create L and R links
    for row in range(len(matrix_A)):
        first_time_in_row = 1
        temp_row = []
        for column in range(len(matrix_A[row])):
            if matrix_A[row][column] == 1:
                if first_time_in_row:
                    first_time_in_row = 0
                    previous = first = data_object()
                    temp_row.append(first)
                else:
                    current = data_object(previous) #Create Left link to previous data_object
                    temp_row.append(current)
                    previous.R = current
                    previous = current
            else:
                temp_row.append(None)
        #Create wraparound links
        first.L = previous
        previous.R = first
        data_object_list.append(temp_row)

    #Create U and D links within data_object_list and column_object_list matrices
    for column in range(len(data_object_list[0])):
        first_time_in_column = 1
        for row in range(len(data_object_list)):
            if data_object_list[row][column]:
                if first_time_in_column:
                    first_time_in_column = 0
                    data_object_list[row][column].U = column_object_list[column+1]
                    column_object_list[column+1].D = data_object_list[row][column]
                    previous = data_object_list[row][column]
                else:
                    data_object_list[row][column].U = previous
                    previous.D = data_object_list[row][column]
                    previous = data_object_list[row][column]
        previous.D = column_object_list[column+1]
        column_object_list[column+1].U = previous



def main():

    data_object_list = []
    column_object_list = []

    matrix_A = [
        [0,0,1,0,1,1,0],
        [1,0,0,1,0,0,1],
        [0,1,1,0,0,1,0],
        [1,0,0,1,0,0,0],
        [0,1,0,0,0,0,1],
        [0,0,0,1,1,0,1]
    ]

    create_column_object_links(matrix_A, column_object_list)
    create_data_object_links(matrix_A, data_object_list, column_object_list)

if __name__ == "__main__":
    main()