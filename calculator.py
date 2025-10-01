# calculator_basic.py

def basic_calculator():
    """
    A simple calculator that performs basic arithmetic operations
    """
    print("🧮 Simple Calculator")
    print("=" * 30)
    
    try:
        # Get user input
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        
        print("\nAvailable operations:")
        print("+ : Addition")
        print("- : Subtraction")
        print("* : Multiplication")
        print("/ : Division")
        print("% : Modulus (Remainder)")
        print("** : Exponentiation")
        
        operation = input("\nEnter the operation symbol: ").strip()
        
        # Perform calculation based on operation
        result = None
        operation_name = ""
        
        if operation == '+':
            result = num1 + num2
            operation_name = "Addition"
        elif operation == '-':
            result = num1 - num2
            operation_name = "Subtraction"
        elif operation == '*':
            result = num1 * num2
            operation_name = "Multiplication"
        elif operation == '/':
            if num2 == 0:
                print("❌ Error: Division by zero is not allowed!")
                return
            result = num1 / num2
            operation_name = "Division"
        elif operation == '%':
            if num2 == 0:
                print("❌ Error: Modulus by zero is not allowed!")
                return
            result = num1 % num2
            operation_name = "Modulus"
        elif operation == '**':
            result = num1 ** num2
            operation_name = "Exponentiation"
        else:
            print("❌ Invalid operation! Please use one of: +, -, *, /, %, **")
            return
        
        # Display result
        print("\n" + "=" * 30)
        print(f"📊 Calculation Result:")
        print(f"{operation_name}: {num1} {operation} {num2} = {result}")
        
    except ValueError:
        print("❌ Error: Please enter valid numbers!")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

# Run the calculator
if __name__ == "__main__":
    basic_calculator()