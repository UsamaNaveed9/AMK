from __future__ import unicode_literals
import frappe
from frappe.utils import today
import calendar
from datetime import datetime
from datetime import timedelta
__version__ = '0.0.1'

@frappe.whitelist()
def make_journal_entry(doc,action):
	not_cash = 0
	for i in doc.payments:
		frappe.errprint(i.mode_of_payment)
		if(i.mode_of_payment != "Cash"):
			not_cash = 1
			break
	if(not_cash):
		new_doc = frappe.new_doc("Journal Entry")
		new_doc.voucher_type = "Journal Entry"
		new_doc.posting_date = today()
		new_doc.reference_invoice = doc.name
		new_doc.company = doc.company
		for i in doc.payments:
			
			if(i.mode_of_payment != "Cash"):
				mop = frappe.get_doc("Mode of Payment",i.mode_of_payment)
				if(mop.extra_cost or mop.extra_cost_percentage):
					bank_account = mop.accounts[0].default_account
					expense_account = mop.expense_account
					row = new_doc.append("accounts",{})
					row.reference_invoice = doc.name
					row.account = bank_account
					# row.party_type = "Customer"
					# row.party = doc.customer
					# row.reference_type = "Sales Invoice"
					# row.reference_name = doc.name
					if(mop.extra_cost):
						row.credit_in_account_currency = mop.extra_cost
					else:
						row.credit_in_account_currency = (mop.extra_cost_percentage/100)*i.amount
					row = new_doc.append("accounts",{})
					row.account = expense_account
					# row.party_type = "Customer"
					# row.party = doc.customer
					# row.reference_type = "Sales Invoice"
					# row.reference_name = doc.name
					if(mop.extra_cost):
						row.debit_in_account_currency = mop.extra_cost
					else:
						row.debit_in_account_currency = (mop.extra_cost_percentage/100)*i.amount
		new_doc.save()
		new_doc.submit()