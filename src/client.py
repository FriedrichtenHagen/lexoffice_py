import os
from urllib.parse import urljoin
import requests
from datetime import datetime, timedelta, date
import time
from typing import Any, Dict, List, Union, Literal
import logging 
from .errors import handle_response
"""
Implementation of the Lexoffice API functions

Docs: https://developers.lexoffice.io/docs/#lexoffice-api-documentation
"""

class Lexoffice:
    def __init__(self, 
                 client_secret:str,
                 max_retries:int = 3,
                 default_retry_wait = 60) -> None:
        
        self.BASE_URL = "https://api.lexoffice.io"
        self.client_secret = client_secret or os.getenv('CLIENT_SECRET')
        
        self.headers = {
            "Authorization": f"Bearer {self.client_secret}",
            "Accept": "application/json"
        }
        self.max_retries = max_retries
        self.default_retry_wait = default_retry_wait

    def _request(self, 
                 path: str,
                 params: dict = None,
                 id: str = None,
                 method = 'GET',
                 ) -> List[Dict[str, Any]]:
        """
            Make a request against the Lexoffice API.
            Returns the HTTP response, which might be successful or not.

            :param path: the URL path for this request (relative to the Lexoffice API base URL)
            :param params: dictionary of URL parameters (optional)
            :param id: id of object
            :param method: the HTTP request method (default: GET)
            :return: the parsed json response, when the request was successful, or a LexofficeApiError
            """
        # make the request
        url = urljoin(self.BASE_URL, path)
        retries = 0
        
        while retries <= self.max_retries:
            response = requests.request(method, url, headers=self.headers, params=params)

            if response.status_code == 429:
                # A client can make up to 2 requests per second to the lexoffice API.
                # Recommended: Use the token bucket algorithm on your side. 
                # Librarys for all major programming languages exist.







                time.wait(60)
                retries += 1
                logging.warning(f"Rate limit exceeded. Retrying in {self.default_retry_wait} seconds...")
                time.sleep(self.default_retry_wait)            
            else:
                return handle_response(response)
    
    def _paginated_requests(self,
                            path:str,
                            params: dict = None,
                            method = 'GET') -> List[Dict[str, Any]]:
        if params is None:
            params = {}
        # add page=0 to the initial request
        params['page'] = 0
        # set page size to maximum (250)
        params['size'] = 250

        initial_request = self._request(
            path,
            params,
        )

        results = initial_request['content']
        num_of_total_pages = initial_request['totalPages']
        num_of_current_page = initial_request['number']
        num_of_total_elements = initial_request['totalElements']
        logging.info(f'Number of total elements: {num_of_total_elements}')
        print(num_of_total_pages)
        while num_of_current_page < num_of_total_pages - 1:
            params['page'] += 1
            next_page_request = self._request(path, params)
            results.extend(next_page_request['content'])
            num_of_current_page = next_page_request['number']
            logging.info(num_of_current_page)
            print(num_of_current_page)
        return results
        
    allowed_voucher_types = Literal['salesinvoice', 'salescreditnote', 'purchaseinvoice', 'purchasecreditnote', 'invoice', 'creditnote', 'orderconfirmation', 'quotation', 'downpaymentinvoice', 'deliverynote']
    allowed_voucher_status = Literal['open', 'draft', 'overdue', 'paid', 'paidoff', 'voided', 'transferred',
                'sepadebit', 'accepted', 'rejected', 'unchecked']
    def get_voucherlist(
            self, 
            voucher_type: Union[Literal['any'], List[allowed_voucher_types]], 
            voucher_status: Union[Literal['any'], List[allowed_voucher_status]],
            archived: bool = None,
            contact_id: str = None,
            voucher_date_from: str = None,
            voucher_date_to: str = None,
            created_date_from: str = None,
            created_date_to: str = None,
            updated_date_from: str = None,
            updated_date_to: str = None, 
            voucher_number: str = None,
        ):
        # https://api.lexoffice.io/v1/voucherlist?voucherType=invoice&voucherStatus=open,paid,paidoff,voided,transferred
        """
        Retrieve and Filter Voucherlist
        Vouchers can be filtered by various attributes, such as voucherType, voucherStatus, the archived flag, various relevant dates, and the voucher number.
        docs: https://developers.lexoffice.io/docs/?shell#voucherlist-endpoint-voucherlist-properties

        :param voucher_type: A comma-separated list of voucher types to be returned, or the value "any".
            salesinvoice	            Vouchers Endpoint
            salescreditnote	            Vouchers Endpoint
            purchaseinvoice	            Vouchers Endpoint
            purchasecreditnote	        Vouchers Endpoint
            invoice	                    Invoices endpoint
            creditnote	                Credit Notes endpoint
            orderconfirmation	        Order Confirmations Endpoint
            quotation	                Quotations Endpoint
            downpaymentinvoice	        Down Payment Invoice Endpoint
            deliverynote                Delivery Notes Endpoint
        :param voucher_status: A comma-separated list of voucher status, or the value "any". Some status only apply to specific voucher types. 
            draft	    Voucher is created but not yet final. It is still editable in lexoffice.
            open	    Voucher is finalized in lexoffice and no longer editable but yet unpaid or only partially paid.
            overdue	    Voucher is open/sepadebit and dueDate is in the past.
            paid	    Voucher is marked as fully paid in lexoffice.
            paidoff	    Voucher is a credit note and paid in full.
            voided	    Voucher is cancelled.
            transferred	Voucher is transferred via the lexoffice online banking connector. When the payment is handled by the bank this status changes to paid.
            sepadebit	The payment has already been authorized or the amount will be collected by direct debit (direct withdrawal). When the payment is handled by the bank this status changes to paid.
            accepted	Only used for quotations. This status is set when a quotation was marked as accepted in lexoffice.
            rejected	Only used for quotations. This status is set when a quotation was marked as rejected in lexoffice.
            unchecked	Only used for bookkeeping vouchers. The voucher has been created in lexoffice using a file upload, but lacks mandatory information and cannot yet be booked
        :param archived:            If the voucher is marked as archived or not.
        :param contact_id:          The id of an existing lexoffice contact.
        :param voucher_date_from:   The date of the voucher in format yyyy-MM-dd(e.g. 2023-06-01). References a full day in CET/CEST 0:00-23:59:59
        :param voucher_date_to:     The date of the voucher in format yyyy-MM-dd(e.g. 2023-06-30). References a full day in CET/CEST 0:00-23:59:59
        :param created_date_from:   The date the voucher was created in format yyyy-MM-dd(e.g. 2023-06-01). References a full day in CET/CEST 0:00-23:59:59
        :param createdDateTo:       The date the voucher was created in format yyyy-MM-dd(e.g. 2023-06-30). References a full day in CET/CEST 0:00-23:59:59
        :param updated_date_from:   The date the voucher was lastly modified in format yyyy-MM-dd(e.g. 2023-06-01). References a full day in CET/CEST 0:00-23:59:59
        :param updated_date_to:     The date the voucher was lastly modified in format yyyy-MM-dd(e.g. 2023-06-30). References a full day in CET/CEST 0:00-23:59:59
        :param voucherNumber:       The voucher's voucher number
        """
        
        # parse voucher types and vouchter stati into comma seperated list
        if voucher_type != 'any':
            voucher_type = ', '.join(voucher_type)
        if voucher_status != 'any':
            voucher_status = ', '.join(voucher_status)

        params = {
            'voucherType': voucher_type,
            'voucherStatus': voucher_status,
            'archived': archived,
            'contactId': contact_id,
            'voucherDateFrom': voucher_date_from,
            'voucherDateTo': voucher_date_to,
            'createdDateFrom': created_date_from,
            'createdDateTo': created_date_to,
            'updatedDateFrom': updated_date_from,
            'updatedDateTo': updated_date_to,
            'voucherNumber': voucher_number,

        }
        voucherlist = self._paginated_requests('/v1/voucherlist/', params)
        return voucherlist
  
    
    def get_articles(self) -> List[Dict[str, Any]]:
        """
        GET Articles
        The articles endpoint provides read and write access to articles in lexoffice. 
        These articles can be used in line items of sales vouchers such as invoices or quotations.

        https://developers.lexoffice.io/docs/?shell#articles-endpoint
        """
        articles = self._paginated_requests('/v1/articles/')
        return articles
    
    def get_contacts(self) -> List[Dict[str, Any]]:
        """
        GET Contacts
        This endpoint provides read access to contacts (e.g. customers, vendors). 
        A contact can hold addresses, contact information (e.g. phone numbers, email addresses) 
        and contact persons for company related contacts.

        https://developers.lexoffice.io/docs/?shell#contacts-endpoint-purpose        
        """

        contacts = self._paginated_requests('/v1/contacts/')
        return contacts

    def get_invoices(self, list_of_invoice_ids):
        # https://api.lexoffice.io/v1/invoices/e9066f04-8cc7-4616-93f8-ac9ecc8479c8

        """
        GET invoices
        This endpoint provides read and write access to invoices.

        https://developers.lexoffice.io/docs/?shell#contacts-endpoint-purpose        
        """
        all_invoices = []
        for invoice_id in list_of_invoice_ids:
            invoice = self._request(f'v1/invoices/{invoice_id}')
            all_invoices.append(invoice)
        return all_invoices
    
    get_