#Chat.gpt was used as a resource to help create this code
import math
"""Imports Python's Math Library"""
def t_distribution_c_value(degrees_of_freedom, confidence_level):
    # Function to compute the c value from the t-distribution table
    m = degrees_of_freedom
    y = confidence_level
    half_y = 0.5 * (1 + y)

    # Initial guess for c using a normal distribution
    c_guess = math.sqrt(2 * math.log(1 / half_y))

    """Defines a function called t distribution c value with parameters degrees of freedom and confidence level.
    State variables m, y, and half_y.
    Calculates a value c using our new half_y value."""
    def equation_to_solve(c):
        return 0.5 * (1 + math.erf(c / math.sqrt(2))) - half_y

    # Use Newton's method to find the root
    tolerance = 1e-10
    max_iterations = 1000
    for _ in range(max_iterations):
        f_c = equation_to_solve(c_guess)
        if abs(f_c) < tolerance:
            break
        f_prime_c = math.exp(-0.5 * c_guess ** 2) / math.sqrt(2 * math.pi)
        c_guess -= f_c / f_prime_c
    """This implements Newton's method to find the root of the equation.
    It continues till the solution is accurate enough within the tolerance
    (or until the max iterations is reached).  The final computed c_guess is returned."""
    return c_guess


def confidence_interval_t_distribution(degrees_of_freedom, z_value, confidence_level):
    # Step 2: Determine c from the t-distribution table
    c = t_distribution_c_value(degrees_of_freedom, confidence_level)

    # Step 3: Compute the probability
    probability = 0.5 * (1 + math.erf(z_value / math.sqrt(2)))

    # Display the results
    print(
        f"\nResults for {degrees_of_freedom} degrees of freedom, z = {z_value}, and {confidence_level * 100}% confidence level:")
    print(f"Computed probability: {probability}")
    """This function calculates the value of c using the t distribution.
    Then it compute the probability using the normal distribution (CDF).
    Then the results are displayed, the user inputted degrees of freedom, 
    the three user inputted z values,
    the user inputted confidence level, and
    the probability for each z value."""

if __name__ == "__main__":
    # Now we have to write code for the user to be able to put in these different values.
    degrees_of_freedom = int(input("Enter the degrees of freedom (n-1): "))
    z_values = [float(input(f"Enter z value {i + 1}: ")) for i in range(3)]  # Input three z values

    # User input for confidence level (e.g., 0.95, 0.99)
    confidence_level = float(input("Enter the confidence level (e.g., 0.95 for 95% confidence): "))
    """This allows the user to put in the different needed values.
    I also specified how each number needed to be put in to help avoid user-error."""
    # Call the function to compute and display the results for each z value
    for z_value in z_values:
        confidence_interval_t_distribution(degrees_of_freedom, z_value, confidence_level)
        """This creates a for loop so that the function won't just output one of the z value probabilities.
        This allows the function to run through the three different z-values and comput the results."""