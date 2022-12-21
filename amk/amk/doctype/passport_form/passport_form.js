// Copyright (c) 2022, smg and contributors
// For license information, please see license.txt

frappe.ui.form.on('Passport Form', {
	form_type(frm) {
		if(frm.doc.form_type == "Receipt"){
		    frm.set_value("naming_series", "RF-.YY.-");
		}
		if(frm.doc.form_type == "Issue"){
		    frm.set_value("naming_series", "IT-.YY.-");
		}
	}
});
