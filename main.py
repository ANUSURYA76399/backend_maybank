from statement_generator import CreditCardStatement
import os

def main():
    try:
        # Check if directories exist, if not create them
        if not os.path.exists('database'):
            os.makedirs('database')
        if not os.path.exists('statements'):
            os.makedirs('statements')

        # Initialize the statement generator
        statement_gen = CreditCardStatement('database/credit_card.db')
        
        # Generate statement for a customer
        print("Generating PDF statement...")
        statement_gen.generate_statement_pdf(
            customer_id=1,
            credit_card_id=1,
            output_path='statements/statement.pdf'
        )
        print("PDF generated successfully!")
        print(f"PDF location: {os.path.abspath('statements/statement.pdf')}")

    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main()