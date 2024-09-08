from typing import Literal

allowed_voucher_types = Literal['salesinvoice', 'salescreditnote', 'purchaseinvoice', 'purchasecreditnote', 'invoice', 'creditnote', 'orderconfirmation', 'quotation', 'downpaymentinvoice', 'deliverynote']
allowed_voucher_status = Literal['open', 'draft', 'overdue', 'paid', 'paidoff', 'voided', 'transferred',
                'sepadebit', 'accepted', 'rejected', 'unchecked']