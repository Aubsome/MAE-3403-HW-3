#Chat.gpt was used as a resource to help create this code
def cholesky_decomposition(A):
    n = len(A)
    L = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1):
            if i == j:
                L[i][j] = (A[i][j] - sum(L[i][k] ** 2 for k in range(j))) ** 0.5
            else:
                L[i][j] = (A[i][j] - sum(L[i][k] * L[j][k] for k in range(j))) / L[j][j]

    return L
"""First we get the size of the matrix using n=len(A).
Next, we define a matrix 'L' that is filled with zeroes, so we can get the lower triangle part
of the Cholesky decomp. 
Then the function iterates each row, and also looks at the diagonals of the matrix.
For Diagonal elements it subtracts the sum of squared elements from the lower triangle matrix
then square roots the results.
For the non Diagonal elements it uses a different formula involving the lower triangle part, 'L'."""

def is_symmetric_positive_definite(matrix):
    # Check if the matrix is symmetric
    for i in range(len(matrix)):
        if len(matrix[i]) != len(matrix):
            return False
        for j in range(i + 1, len(matrix[i])):
            if matrix[i][j] != matrix[j][i]:
                return False
    """The for loop here checks to see if the matrix is symmetric.
    It iterates each row of the matrix using the first loop.
    This means for each row it checks the length og the row and sees if it is equal to the total number of rows.
    If it is not equal it gives the feedback, 'false'.
    The second loop looks at the diagonal's of the matrix and compares the elements below
    the diagonal with the connecting element above. If the connecting elements are not equal"""

    # Check if the matrix is positive definite
    try:
        cholesky_decomposition(matrix)
        return True
    except ValueError:
        return False

"""This 'try' function then runs the cholesky decomposition function we just made.
If the function runs successfully then the matrix is symmetric and positive definite. 
If the function does not run right then the matrix gives a valueerror of false letting the
system know that the cholesky decomposition is not possible."""

def forward_substitution(L, b):
    n = len(L)
    y = [0] * n

    for i in range(n):
        y[i] = (b[i] - sum(L[i][j] * y[j] for j in range(i))) / L[i][i]

    return y
"""We are creating a function that will perform forward substitution for the Cholesky Matrix.
We first get the matrix's size. 'L'
Then we state that a vector named 'y' with length 'n' will be all zeroes.
Next we iterate over the rows of the matrix 'L'
The function then performs the calculation for forward substitution.
The final solution vector is given back as 'y'
(This function is for the lower triangle part of the matrix)"""
def backward_substitution(L, b):
    n = len(L)
    x = [0] * n

    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(L[j][i] * x[j] for j in range(i + 1, n))) / L[i][i]

    return x
"""We are creating a function that will perform backward substitution for the Cholesky Matrix.
We first get the matrix's size. 'L'
Then we state that a vector named 'x' with length 'n' will be all zeroes.
Next we iterate over the rows of the matrix 'L' in reverse.
The function then performs the calculation for backward substitution.
The final solution vector is given back as 'x'
(This function is for the upper triangle part of the matrix)"""
def cholesky_solve(A, b):
    L = cholesky_decomposition(A)
    y = forward_substitution(L, b)
    x = backward_substitution(L, y)
    return x
"""Defines a function names cholesky solve with variables A and b.
The Cholesky decomposition function runs using matrix 'A' 
The forward substitution function runs using 'L' from the Cholesky decomp and variable b.
The backward substitution function runs using 'L' from Cholesky decomp (transposes it) and variable y.
The solution returns with x from the eqn. Ax=b"""
def little_decomposition(A):
    n = len(A)
    L = [[0] * n for _ in range(n)]
    U = [[0] * n for _ in range(n)]

    for i in range(n):
        L[i][i] = 1

    for i in range(n):
        for j in range(i, n):
            U[i][j] = A[i][j] - sum(L[i][k] * U[k][j] for k in range(i))
        for j in range(i + 1, n):
            L[j][i] = (A[j][i] - sum(L[j][k] * U[k][i] for k in range(i))) / U[i][i]

    return L, U
"""This is a function for the Doolittle Decomposition.
First we find the size of Matrix A
Then we create a matrix 'L' of size 'n' that will be all zeroes. (For Lower Triangle)
Then we create a matrix 'U' of size 'n' that will be all zeroes. (For upper Triangle)
Then we set the diagonal elements in 'L' to 1.
Then we calculate the upper triangle matrix using U.
Then we calculate the lower triangle matrix using L.
It returns the new calculated matrices L and U."""
def doolittle_solve(A, b):
    L, U = little_decomposition(A)

    n = len(A)
    y = [0] * n
    x = [0] * n

    # Solve Ly = b using forward substitution
    for i in range(n):
        y[i] = b[i] - sum(L[i][j] * y[j] for j in range(i))

    # Solve Ux = y using backward substitution
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]

    return x
"""This is a function to solve the Doolittle matrix.
Using the little decomposition function we created above we get L and U.
We get the size of the matrix A
A vector named y will be the size of n filled with zeroes.
A vector named x will be the size of n filled with zeroes.
Performs the calculations for forward substitution to solve for y in Ly=b.
Performs the calculations for backward substitution to solve for x in Ux=y.
Gives back 'x' which is the solution vector for the Doolittle eqn."""
def solve_linear_system(A, b):
    if is_symmetric_positive_definite(A):
        print("Using Cholesky method:")
        x = cholesky_solve(A, b)
    else:
        print("Using Doolittle method:")
        x = doolittle_solve(A, b)

    return x
"""This function makes an if statement saying, if the function to determine if the
matrix was both positive and definite gave the output true print that we are using
the Cholesky method and that its solved x vector is correct.  If not, print that we
are using the Doolittle method and use its solved x from now on."""
def main():
    # Problem 1
    A1 = [[1, -1, 3, 2],
          [-1, 5, -5, -2],
          [3, -5, 19, 3],
          [2, -2, 3, 21]]

    b1 = [15, -35, 94, 1]

    # Problem 2
    A2 = [[4, 2, 4, 0],
          [2, 2, 3, 2],
          [4, 3, 6, 3],
          [0, 2, 3, 9]]

    b2 = [20, 36, 60, 122]

    # Solve problems
    x1 = solve_linear_system(A1, b1)
    print(f"Solution for Problem 1: {x1}")
    x2 = solve_linear_system(A2, b2)
    print(f"Solution for Problem 2: {x2}")
"""This is where we run our main function.
We first set up the first matrix (A1) and its solution matrix (b1).
Then we set up the second matrix (A2) and its solution matrix (b2).
Then we solve the problems.
We state that the solution vector for the first problem, 'x1', will be found using
the solve linear system function we have created. Once solve it will print our 
solution vector (x1).  
The second matrix's solution vector, 'x2', will be found using the solve linear 
system function we have created.  Once solve it will print our solution vector (x2)."""

if __name__ == "__main__":
    """This checks that the script is running as the main program."""
    main()
    """This calls the main function."""