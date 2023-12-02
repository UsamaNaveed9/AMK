from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import today



@frappe.whitelist()
def make_journal_entry(doc,action):
	if(doc.mode_of_payment != "Cash"):
		mop = frappe.get_doc("Mode of Payment",doc.mode_of_payment)
		if(mop.extra_cost or mop.extra_cost_percentage):
			bank_account = mop.accounts[0].default_account
			expense_account = mop.expense_account
			new_doc = frappe.new_doc("Journal Entry")
			new_doc.cheque_no = doc.name
			new_doc.company = doc.company
			row = new_doc.append("accounts",{})
			row.account = bank_account
			if(mop.extra_cost):
				row.credit_in_account_currency = mop.extra_cost
			else:
				row.credit_in_account_currency = (mop.extra_cost_percentage/100)*doc.paid_amount
			row = new_doc.append("accounts",{})
			row.account = expense_account
			if(mop.extra_cost):
				row.debit_in_account_currency = mop.extra_cost
			else:
				row.debit_in_account_currency = (mop.extra_cost_percentage/100)*doc.paid_amount
			new_doc.voucher_type = "Journal Entry"
			new_doc.posting_date = today()
			new_doc.cheque_date = today()
			new_doc.save()
			new_doc.submit()