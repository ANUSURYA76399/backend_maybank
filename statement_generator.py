import sqlite3
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime, timedelta  # Added timedelta import

class CreditCardStatement:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def get_customer_details(self, customer_id):
        query = """
        SELECT c.name, c.address, cc.card_number, cc.previous_balance
        FROM customers c
        JOIN credit_cards cc ON c.id = cc.customer_id
        WHERE c.id = ?
        """
        return self.cursor.execute(query, (customer_id,)).fetchone()

    def get_transactions(self, credit_card_id):
        query = """
        SELECT transaction_date, description, amount
        FROM transactions
        WHERE credit_card_id = ?
        ORDER BY transaction_date
        """
        return self.cursor.execute(query, (credit_card_id,)).fetchall()

    def get_rewards(self, credit_card_id):
        query = """
        SELECT opening_balance, earned_points, redeemed_points, closing_balance
        FROM rewards
        WHERE credit_card_id = ?
        """
        return self.cursor.execute(query, (credit_card_id,)).fetchone()

    def generate_statement_pdf(self, customer_id, credit_card_id, output_path):
        # Get data
        customer_data = self.get_customer_details(customer_id)
        transactions = self.get_transactions(credit_card_id)
        rewards = self.get_rewards(credit_card_id)

        # Create PDF
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        # Header
        elements.append(Paragraph("Maybank Credit Card Statement", styles['Heading1']))
        elements.append(Spacer(1, 20))

        # Customer Details
        customer_info = [
            [customer_data[0]],
            [customer_data[1]]
        ]
        customer_table = Table(customer_info)
        elements.append(customer_table)
        elements.append(Spacer(1, 20))

        # Add table style for customer info
        customer_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))

        # Account Summary
        previous_balance = customer_data[3]
        total_payments = sum(-amount for _, _, amount in transactions if amount < 0)
        total_purchases = sum(amount for _, _, amount in transactions if amount > 0)
        finance_charges = 30.00  # Example fixed charge
        new_balance = previous_balance - total_payments + total_purchases + finance_charges

        summary_data = [
            ['Account Summary'],
            ['Previous Balance', f'RM {previous_balance:.2f}'],
            ['Payments', f'RM {total_payments:.2f}'],
            ['Purchases', f'RM {total_purchases:.2f}'],
            ['Finance Charges', f'RM {finance_charges:.2f}'],
            ['New Balance', f'RM {new_balance:.2f}'],
            ['Minimum Payment', f'RM {(new_balance * 0.05):.2f}'],
            ['Due Date', (datetime.now().replace(day=25) + timedelta(days=31)).strftime('%Y-%m-%d')]
        ]
        summary_table = Table(summary_data, colWidths=[200, 100])
        elements.append(summary_table)
        elements.append(Spacer(1, 20))

        # Add table style for summary
        summary_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Transactions
        trans_data = [['Date', 'Description', 'Amount']]
        for date, desc, amount in transactions:
            trans_data.append([date, desc, f'RM {amount:.2f}'])
        
        elements.append(Paragraph("Transactions", styles['Heading2']))
        trans_table = Table(trans_data, colWidths=[100, 300, 100])
        elements.append(trans_table)
        elements.append(Spacer(1, 20))

        # Add table style for transactions
        trans_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (-1, 1), (-1, -1), 'RIGHT'),  # Right align amounts
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Rewards Summary
        if rewards:
            rewards_data = [
                ['Rewards Summary'],
                ['Opening Balance', str(rewards[0])],
                ['Earned Points', str(rewards[1])],
                ['Redeemed Points', str(rewards[2])],
                ['Closing Balance', str(rewards[3])]
            ]
            rewards_table = Table(rewards_data, colWidths=[200, 100])
            rewards_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(rewards_table)

        # Generate PDF
        doc.build(elements)

    def __del__(self):
        self.conn.close()