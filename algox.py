import sys

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
class column_object (data_object):
    #Create links as column_object type attributes
    def __init__(self, S=None, N=None):
        data_object.__init__(self, L=None, R=None, U=None, D=None, C=None)
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
        current_column.N = column + 1
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
                previous.C = column_object_list[column+1]
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

def count_ones(matrix_A, column_object_list):
    for column in range(len(matrix_A[0])):
        column_count = 0
        for row in range(len(matrix_A)):
            if matrix_A[row][column] == 1:
                column_count += 1
                column_object_list[column+1].S = column_count

def choose_column(column_object_list):
    temp_column = column_object_list[1]
    s = sys.maxsize
    while (temp_column != column_object_list[0]):
        if(temp_column.S < s):
            s = temp_column.S
            return_column = temp_column
        temp_column = temp_column.R
    return return_column

def cover_column(selected_column):
    selected_column.R.L = selected_column.L
    selected_column.L.R = selected_column.R
    temp_row = selected_column.D
    while (temp_row != selected_column):
        temp_column = temp_row.R
        while(temp_column != temp_row):
            temp_column.D.U = temp_column.U
            temp_column.U.D = temp_column.D
            temp_column.C.S = temp_column.C.S - 1
            temp_column = temp_column.R
        temp_row = temp_row.D

def uncover_column(selected_column):
    temp_row = selected_column.U
    while(temp_row != selected_column):
        temp_column = temp_row.L
        while(temp_column != temp_row):
            temp_column.C.S = temp_column.C.S + 1
            temp_column.D.U = temp_column
            temp_column.U.D = temp_column
            temp_column = temp_column.L
        temp_row = temp_row.U
    selected_column.R.L = selected_column
    selected_column.L.R = selected_column

def search(k, data_object_list, column_object_list, solution_list):

    if(column_object_list[0].R == column_object_list[0]):
        temp_solution_row = []
        solution_matrix = []
        print('Solution found:')
        for s in solution_list:
            if s:
                temp_column = s.R
                temp_solution_row.append(s.C.N)
                while(temp_column != s):
                    temp_solution_row.append(temp_column.C.N)
                    temp_column = temp_column.R
            solution_matrix.append(temp_solution_row)
            temp_solution_row = []

        for i in range(len(solution_matrix)):
            count = 0
            for j in range(len(solution_matrix[i])):
                count += solution_matrix[i][j]
            if (count):
                for z in range(len(data_object_list[0])):
                    if ((z+1) in solution_matrix[i]):
                        print(1, end="")
                    else:
                        print(0, end="")
                print('\r')
        return True 
    else:
        selected_column = choose_column(column_object_list)
        cover_column(selected_column)
        temp_row = selected_column.D
        while (temp_row != selected_column):
            solution_list[k] = temp_row
            temp_column = temp_row.R
            while(temp_column != temp_row):
                cover_column(temp_column.C)
                temp_column = temp_column.R
            solution_found = search(k+1, data_object_list, column_object_list, solution_list)
            if solution_found:
                return solution_found
            temp_row = solution_list[k]
            selected_column = temp_row.C
            temp_column = temp_row.L
            while(temp_column != temp_row):
                uncover_column(temp_column.C)
                temp_column = temp_column.L
            temp_row = temp_row.D
        uncover_column(selected_column)

def main():
    k = 0

    matrix_A = [
        [0,0,1,0,1,1,0],
        [1,0,0,1,0,0,1],
        [0,1,1,0,0,1,0],
        [1,0,0,1,0,0,0],
        [0,1,0,0,0,0,1],
        [0,0,0,1,1,0,1]
    ]

    data_object_list = []
    column_object_list = []
    solution_list = [None] * len(matrix_A)

    create_column_object_links(matrix_A, column_object_list)
    create_data_object_links(matrix_A, data_object_list, column_object_list)
    count_ones(matrix_A, column_object_list)

    if not(search(k, data_object_list, column_object_list, solution_list)):
        print ('No solution found')

if __name__ == "__main__":
    main()