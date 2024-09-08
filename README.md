# lexoffice_py

**lexoffice_py** is a python wrapper around the [Lexoffice API](https://developers.lexoffice.io/docs/).
The goals is to provide an easy to use interface for all Lexoffice API endpoints.
It handles pagination, rate limiting, errors. Most information needed is available via docstrings, for further details please refer to the [Lexoffice API docs](https://developers.lexoffice.io/docs/).

```python
>>> from client import Lexoffice
>>> Lex = Lexoffice(client_secret='***')
>>> voucherlist = Lexoffice.get_voucherlist(voucher_type='invoice', voucher_status='open', voucher_date_from='2024-01-01')
>>> len(voucherlist)
1204
>>> voucherlist[0]
{
  "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "voucherType": "invoice",
  "voucherStatus": "open",
  "voucherNumber": "INV1234",
  "voucherDate": "2024-09-05T00:00:00.000+02:00",
  "createdDate": "2024-09-05T09:20:09.000+02:00",
  "updatedDate": "2024-09-05T09:32:59.000+02:00",
  "dueDate": "2024-09-15T00:00:00.000+02:00",
  "contactName": "COMPANY NAME",
  "totalAmount": 10000.0,
  "openAmount": 10000.0,
  "currency": "EUR",
  "archived": false
}
```

If something appears to be broken, please have a look at the [open issues](https://github.com/FriedrichtenHagen/lexoffice_py/issues) and vote for an existing issue or create a new one, if you can't find an issue that describes your problem.

## Features

* Aims to cover all functions of the Lexoffice API (work in progress)
* Allows you to get detailed information for all of your invoices (including line item information) at once. If you have you have a very large amount of invoices, you made want to solve this differently since each invoice results in one api call.
* Python function wrappers for all API endpoints as part of the Lexoffice class
* Support for type hints

## API Functions

lexoffice_py currently only implements a subset of all available API features. This section gives an overview over which API endpoints are accessible through lexoffice_py.

### Available
- GET Voucherlist
- GET Articles
- GET Contacts
- GET Invoices

### Not yet (fully) implemented

- Contacts
- Countries 
- Credit Notes 
- Delivery Notes 
- Dunnings 
- Down Payment Invoices 
- Event Subscriptions 
- Files 
- Invoices 
- Order Confirmations 
- Payments 
- Payment Conditions 
- Posting Categories 
- Print Layouts 
- Profile 
- Quotations 
- Recurring Templates 
- Voucherlist 
- Vouchers 

- POST Endpoints in general



