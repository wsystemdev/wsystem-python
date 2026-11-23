# Generated from the W System OpenAPI 0.3.130 by growth/sdk/gen.py. Do not edit by hand.
from __future__ import annotations
from typing import Any, Optional
from ._http import RequestOptions, _seg

OPERATIONS = [
    ('billingPlans', 'GET', '/billing/plans'),
    ('billingUsage', 'GET', '/billing/usage'),
    ('billingCheckout', 'POST', '/billing/checkout'),
    ('einvoiceMandateTerms', 'GET', '/einvoice/mandate-terms'),
    ('createPeppolMandate', 'POST', '/einvoice/mandates'),
    ('getPeppolMandate', 'GET', '/einvoice/mandates/{mid}'),
    ('revokePeppolMandate', 'POST', '/einvoice/mandates/{mid}/revoke'),
    ('einvoiceInbox', 'GET', '/einvoice/inbox'),
    ('einvoiceInboxUbl', 'GET', '/einvoice/inbox/{document_id}/ubl'),
    ('einvoiceLiveStatus', 'GET', '/einvoice/live/{document_id}'),
    ('listPlatformCompanies', 'GET', '/platform/companies'),
    ('getPlatformCompany', 'GET', '/platform/companies/{mandate_id}'),
    ('setPlatformWebhook', 'POST', '/platform/webhook'),
    ('getPlatformWebhook', 'GET', '/platform/webhook'),
    ('deletePlatformWebhook', 'DELETE', '/platform/webhook'),
    ('testPlatformWebhook', 'POST', '/platform/webhook/test'),
    ('getPlatformUsage', 'GET', '/platform/usage'),
    ('setPlatformSpendCap', 'PUT', '/platform/spend-cap'),
    ('checkReceivedInvoice', 'POST', '/einvoice/check'),
    ('listInboxInvoices', 'GET', '/inbox/invoices'),
    ('getInboxInvoice', 'GET', '/inbox/invoices/{iid}'),
    ('deleteInboxInvoice', 'DELETE', '/inbox/invoices/{iid}'),
    ('getInboxAddress', 'GET', '/inbox/address'),
    ('rotateInboxAddress', 'POST', '/inbox/address/rotate'),
    ('ksefInfo', 'GET', '/einvoice/ksef'),
    ('ksefConnect', 'POST', '/einvoice/ksef/connections'),
    ('ksefConnections', 'GET', '/einvoice/ksef/connections'),
    ('ksefTestCompany', 'POST', '/einvoice/ksef/test-company'),
    ('ksefAuthChallenge', 'POST', '/einvoice/ksef/auth/challenge'),
    ('ksefAuthComplete', 'POST', '/einvoice/ksef/auth/complete'),
    ('ksefDisconnect', 'DELETE', '/einvoice/ksef/connections/{cid}'),
    ('ksefInvoiceStatus', 'GET', '/einvoice/ksef/invoices/{sid}'),
    ('ksefInvoiceUpo', 'GET', '/einvoice/ksef/invoices/{sid}/upo'),
    ('ksefInvoices', 'GET', '/einvoice/ksef/invoices'),
    ('health', 'GET', '/health'),
    ('viesStatus', 'GET', '/vies/status'),
    ('verifyVat', 'GET', '/verify'),
    ('verifyVatBatch', 'POST', '/verify/batch'),
    ('lookupCompany', 'GET', '/company'),
    ('lookupCompanyBatch', 'POST', '/company/batch'),
    ('screenSanctions', 'GET', '/sanctions/screen'),
    ('screenSanctionsBatch', 'POST', '/sanctions/screen/batch'),
    ('kybCheck', 'POST', '/kyb/check'),
    ('verifyEori', 'GET', '/eori'),
    ('verifyEoriBatch', 'POST', '/eori/batch'),
    ('validateEinvoice', 'POST', '/einvoice/validate'),
    ('parseEinvoice', 'POST', '/einvoice/parse'),
    ('createEinvoice', 'POST', '/einvoice/create'),
    ('einvoiceRoute', 'GET', '/einvoice/route'),
    ('ddReport', 'POST', '/ddreport'),
    ('frPaRegistry', 'GET', '/fr/pa-registry'),
    ('extractEinvoiceFromPdf', 'POST', '/einvoice/extract'),
    ('einvoiceSample', 'GET', '/einvoice/sample'),
    ('sendEinvoice', 'POST', '/einvoice/send'),
    ('preflightEinvoice', 'POST', '/einvoice/preflight'),
    ('einvoiceEvidenceKey', 'GET', '/einvoice/evidence-key'),
    ('einvoiceUsage', 'GET', '/einvoice/usage'),
]


class _Operations:
    """All 57 operations of the W System API (spec 0.3.130)."""

    def _request(self, method: str, path: str, *, query: Any = None, body: Any = None, options: Optional[RequestOptions] = None) -> Any:  # pragma: no cover
        raise NotImplementedError

    def billing_plans(self, *, options: Optional[RequestOptions] = None) -> Any:
        """Monthly API-key plans  (GET /billing/plans)"""
        return self._request('GET', '/billing/plans', query={}, body=None, options=options)

    def billing_usage(self, *, options: Optional[RequestOptions] = None) -> Any:
        """Your API key's plan, monthly quota, units used, and paid x402 calls attributed to this key (free; no units consumed)  (GET /billing/usage)"""
        return self._request('GET', '/billing/usage', query={}, body=None, options=options)

    def billing_checkout(self, body: Any, *, options: Optional[RequestOptions] = None) -> Any:
        """Start Stripe Checkout for a monthly plan  (POST /billing/checkout)"""
        return self._request('POST', '/billing/checkout', query={}, body=body, options=options)

    def einvoice_mandate_terms(self, *, options: Optional[RequestOptions] = None) -> Any:
        """Get the Peppol mandate terms to show the signer  (GET /einvoice/mandate-terms)"""
        return self._request('GET', '/einvoice/mandate-terms', query={}, body=None, options=options)

    def create_peppol_mandate(self, body: Any, *, options: Optional[RequestOptions] = None) -> Any:
        """Record a company's Peppol mandate (click-through acceptance)  (POST /einvoice/mandates)"""
        return self._request('POST', '/einvoice/mandates', query={}, body=body, options=options)

    def get_peppol_mandate(self, mid: Any, *, options: Optional[RequestOptions] = None) -> Any:
        """Get one of your Peppol mandate records  (GET /einvoice/mandates/{mid})"""
        return self._request('GET', '/einvoice/mandates/' + _seg(mid), query={}, body=None, options=options)

    def revoke_peppol_mandate(self, mid: Any, *, options: Optional[RequestOptions] = None) -> Any:
        """Revoke a Peppol mandate  (POST /einvoice/mandates/{mid}/revoke)"""
        return self._request('POST', '/einvoice/mandates/' + _seg(mid) + '/revoke', query={}, body=None, options=options)

    def einvoice_inbox(self, *, page: Any = None, page_size: Any = None, options: Optional[RequestOptions] = None) -> Any:
        """LIVE: documents received over Peppol for your mandated companies (X-API-Key)  (GET /einvoice/inbox)"""
        return self._request('GET', '/einvoice/inbox', query={'page': page, 'page_size': page_size}, body=None, options=options)

    def einvoice_inbox_ubl(self, document_id: Any, *, options: Optional[RequestOptions] = None) -> Any:
        """LIVE: signed download link for a received document's original UBL (valid 1 hour)  (GET /einvoice/inbox/{document_id}/ubl)"""
        return self._request('GET', '/einvoice/inbox/' + _seg(document_id) + '/ubl', query={}, body=None, options=options)

    def einvoice_live_status(self, document_id: Any, *, options: Optional[RequestOptions] = None) -> Any:
        """LIVE: delivery state of a document you sent with mode=live (TRANSIT -> SENT, or FAILED = not charged)  (GET /einvoice/live/{document_id})"""
        return self._request('GET', '/einvoice/live/' + _seg(document_id), query={}, body=None, options=options)

    def list_platform_companies(self, *, client_ref: Any = None, options: Optional[RequestOptions] = None) -> Any:
        """List the client companies under your key: onboarding stage, live readiness and per-company live document counts  (GET /platform/companies)"""
        return self._request('GET', '/platform/companies', query={'client_ref': client_ref}, body=None, options=options)

    def get_platform_company(self, mandate_id: Any, *, options: Optional[RequestOptions] = None) -> Any:
        """One client company under your key: onboarding stage, next step and live document counts  (GET /platform/companies/{mandate_id})"""
        return self._request('GET', '/platform/companies/' + _seg(mandate_id), query={}, body=None, options=options)

    def set_platform_webhook(self, body: Any, *, options: Optional[RequestOptions] = None) -> Any:
        """Set or replace your webhook URL for company.stage_changed (signing secret returned once)  (POST /platform/webhook)"""
        return self._request('POST', '/platform/webhook', query={}, body=body, options=options)

    def get_platform_webhook(self, *, options: Optional[RequestOptions] = None) -> Any:
        """Your webhook URL and its recent deliveries (the secret is never shown again)  (GET /platform/webhook)"""
        return self._request('GET', '/platform/webhook', query={}, body=None, options=options)

    def delete_platform_webhook(self, *, options: Optional[RequestOptions] = None) -> Any:
        """Remove your webhook  (DELETE /platform/webhook)"""
        return self._request('DELETE', '/platform/webhook', query={}, body=None, options=options)

    def test_platform_webhook(self, *, options: Optional[RequestOptions] = None) -> Any:
        """Send a signed webhook.test event to your URL now and return the delivery result  (POST /platform/webhook/test)"""
        return self._request('POST', '/platform/webhook/test', query={}, body=None, options=options)

    def get_platform_usage(self, *, options: Optional[RequestOptions] = None) -> Any:
        """Platform plan: this month's checked documents, Peppol documents, active companies and cost estimate (free)  (GET /platform/usage)"""
        return self._request('GET', '/platform/usage', query={}, body=None, options=options)

    def set_platform_spend_cap(self, body: Any, *, options: Optional[RequestOptions] = None) -> Any:
        """Platform plan: set or remove an optional monthly spend cap in EUR (calls that would exceed it get 429, nothing charged)  (PUT /platform/spend-cap)"""
        return self._request('PUT', '/platform/spend-cap', query={}, body=body, options=options)

    def check_received_invoice(self, body: Any, *, options: Optional[RequestOptions] = None) -> Any:
        """Check a received invoice before paying it: e-invoice rules, supplier VAT + sanctions, amounts, IBAN, duplicates, bank-detail changes -> ok / review / hold  (POST /einvoice/check)"""
        return self._request('POST', '/einvoice/check', query={}, body=body, options=options)

    def list_inbox_invoices(self, *, limit: Any = None, verdict: Any = None, options: Optional[RequestOptions] = None) -> Any:
        """Your checked received invoices, newest first (free)  (GET /inbox/invoices)"""
        return self._request('GET', '/inbox/invoices', query={'limit': limit, 'verdict': verdict}, body=None, options=options)

    def get_inbox_invoice(self, iid: Any, *, options: Optional[RequestOptions] = None) -> Any:
        """One checked invoice with its full check result (free)  (GET /inbox/invoices/{iid})"""
        return self._request('GET', '/inbox/invoices/' + _seg(iid), query={}, body=None, options=options)

    def delete_inbox_invoice(self, iid: Any, *, options: Optional[RequestOptions] = None) -> Any:
        """Delete one invoice from your inbox history (free)  (DELETE /inbox/invoices/{iid})"""
        return self._request('DELETE', '/inbox/invoices/' + _seg(iid), query={}, body=None, options=options)

    def get_inbox_address(self, *, options: Optional[RequestOptions] = None) -> Any:
        """Your own email intake address: forward supplier invoices there (free)  (GET /inbox/address)"""
        return self._request('GET', '/inbox/address', query={}, body=None, options=options)

    def rotate_inbox_address(self, *, options: Optional[RequestOptions] = None) -> Any:
        """Issue a new intake address; the old one stops working (free)  (POST /inbox/address/rotate)"""
        return self._request('POST', '/inbox/address/rotate', query={}, body=None, options=options)

    def ksef_info(self, *, options: Optional[RequestOptions] = None) -> Any:
        """Poland KSeF connector: what works, environment, how to connect (free)  (GET /einvoice/ksef)"""
        return self._request('GET', '/einvoice/ksef', query={}, body=None, options=options)

    def ksef_connect(self, body: Any, *, options: Optional[RequestOptions] = None) -> Any:
        """Connect a company's KSeF account (TEST, or DEMO if enabled): store its KSeF token encrypted after a sign-in check  (POST /einvoice/ksef/connections)"""
        return self._request('POST', '/einvoice/ksef/connections', query={}, body=body, options=options)

    def ksef_connections(self, *, options: Optional[RequestOptions] = None) -> Any:
        """List the KSeF connections (companies) under your API key  (GET /einvoice/ksef/connections)"""
        return self._request('GET', '/einvoice/ksef/connections', query={}, body=None, options=options)

    def ksef_test_company(self, body: Any = None, *, options: Optional[RequestOptions] = None) -> Any:
        """Create a fictitious company in KSeF TEST (random NIP) and connect it, to try KSeF sending end to end  (POST /einvoice/ksef/test-company)"""
        return self._request('POST', '/einvoice/ksef/test-company', query={}, body=body, options=options)

    def ksef_auth_challenge(self, body: Any, *, options: Optional[RequestOptions] = None) -> Any:
        """Start certificate sign-in: get a KSeF challenge and the unsigned AuthTokenRequest XML to sign externally  (POST /einvoice/ksef/auth/challenge)"""
        return self._request('POST', '/einvoice/ksef/auth/challenge', query={}, body=body, options=options)

    def ksef_auth_complete(self, body: Any, *, options: Optional[RequestOptions] = None) -> Any:
        """Finish certificate sign-in: accept the signed AuthTokenRequest, enroll a KSeF Authentication certificate, store it encrypted  (POST /einvoice/ksef/auth/complete)"""
        return self._request('POST', '/einvoice/ksef/auth/complete', query={}, body=body, options=options)

    def ksef_disconnect(self, cid: Any, *, options: Optional[RequestOptions] = None) -> Any:
        """Revoke a KSeF connection: the stored KSeF token is deleted at once  (DELETE /einvoice/ksef/connections/{cid})"""
        return self._request('DELETE', '/einvoice/ksef/connections/' + _seg(cid), query={}, body=None, options=options)

    def ksef_invoice_status(self, sid: Any, *, options: Optional[RequestOptions] = None) -> Any:
        """KSeF status of a sent invoice: processing / accepted (KSeF number) / rejected (code and reason) (free)  (GET /einvoice/ksef/invoices/{sid})"""
        return self._request('GET', '/einvoice/ksef/invoices/' + _seg(sid), query={}, body=None, options=options)

    def ksef_invoice_upo(self, sid: Any, *, options: Optional[RequestOptions] = None) -> Any:
        """UPO (official KSeF receipt, XML signed by the Ministry of Finance) of an accepted invoice (free)  (GET /einvoice/ksef/invoices/{sid}/upo)"""
        return self._request('GET', '/einvoice/ksef/invoices/' + _seg(sid) + '/upo', query={}, body=None, options=options)

    def ksef_invoices(self, *, nip: Any = None, limit: Any = None, options: Optional[RequestOptions] = None) -> Any:
        """List invoices sent to KSeF under your API key (newest first, free)  (GET /einvoice/ksef/invoices)"""
        return self._request('GET', '/einvoice/ksef/invoices', query={'nip': nip, 'limit': limit}, body=None, options=options)

    def health(self, *, options: Optional[RequestOptions] = None) -> Any:
        """Liveness check  (GET /health)"""
        return self._request('GET', '/health', query={}, body=None, options=options)

    def vies_status(self, *, options: Optional[RequestOptions] = None) -> Any:
        """VIES availability per member state (free, cached 5 min)  (GET /vies/status)"""
        return self._request('GET', '/vies/status', query={}, body=None, options=options)

    def verify_vat(self, vat: Any, *, requester: Any = None, nocache: Any = None, fallback: Any = None, options: Optional[RequestOptions] = None) -> Any:
        """Validate one EU VAT number (VIES)  (GET /verify)"""
        return self._request('GET', '/verify', query={'vat': vat, 'requester': requester, 'nocache': nocache, 'fallback': fallback}, body=None, options=options)

    def verify_vat_batch(self, body: Any, *, options: Optional[RequestOptions] = None) -> Any:
        """Validate up to 100 EU VAT numbers  (POST /verify/batch)"""
        return self._request('POST', '/verify/batch', query={}, body=body, options=options)

    def lookup_company(self, q: Any, *, country: Any = None, limit: Any = None, options: Optional[RequestOptions] = None) -> Any:
        """Look up a company in official EU business registers  (GET /company)"""
        return self._request('GET', '/company', query={'q': q, 'country': country, 'limit': limit}, body=None, options=options)

    def lookup_company_batch(self, body: Any, *, options: Optional[RequestOptions] = None) -> Any:
        """Batch company-registry lookup (max 25 queries)  (POST /company/batch)"""
        return self._request('POST', '/company/batch', query={}, body=body, options=options)

    def screen_sanctions(self, name: Any, *, threshold: Any = None, birth_year: Any = None, country: Any = None, lists: Any = None, options: Optional[RequestOptions] = None) -> Any:
        """Screen a name against EU, UN, OFAC and UK sanctions lists  (GET /sanctions/screen)"""
        return self._request('GET', '/sanctions/screen', query={'name': name, 'threshold': threshold, 'birth_year': birth_year, 'country': country, 'lists': lists}, body=None, options=options)

    def screen_sanctions_batch(self, body: Any, *, options: Optional[RequestOptions] = None) -> Any:
        """Batch sanctions screening (max 50 names)  (POST /sanctions/screen/batch)"""
        return self._request('POST', '/sanctions/screen/batch', query={}, body=body, options=options)

    def kyb_check(self, body: Any, *, options: Optional[RequestOptions] = None) -> Any:
        """One-call KYB: VAT + registry + sanctions -> verdict  (POST /kyb/check)"""
        return self._request('POST', '/kyb/check', query={}, body=body, options=options)

    def verify_eori(self, eori: Any, *, options: Optional[RequestOptions] = None) -> Any:
        """Validate one EU EORI number (EC EOS)  (GET /eori)"""
        return self._request('GET', '/eori', query={'eori': eori}, body=None, options=options)

    def verify_eori_batch(self, body: Any, *, options: Optional[RequestOptions] = None) -> Any:
        """Validate up to 100 EU EORI numbers  (POST /eori/batch)"""
        return self._request('POST', '/eori/batch', query={}, body=body, options=options)

    def validate_einvoice(self, body: Any, *, rules: Any = None, autofix: Any = None, allow_amount_changes: Any = None, options: Optional[RequestOptions] = None) -> Any:
        """Validate an EU e-invoice (EN 16931, XRechnung; UBL, CII, ZUGFeRD/Factur-X PDF)  (POST /einvoice/validate)"""
        return self._request('POST', '/einvoice/validate', query={'rules': rules, 'autofix': autofix, 'allow_amount_changes': allow_amount_changes}, body=body, options=options)

    def parse_einvoice(self, body: Any, *, options: Optional[RequestOptions] = None) -> Any:
        """Read an incoming EU e-invoice (UBL, CII, ZUGFeRD/Factur-X PDF) into JSON  (POST /einvoice/parse)"""
        return self._request('POST', '/einvoice/parse', query={}, body=body, options=options)

    def create_einvoice(self, body: Any, *, options: Optional[RequestOptions] = None) -> Any:
        """Create a valid EU e-invoice (UBL 2.1, CII, ZUGFeRD/Factur-X PDF) from simple JSON  (POST /einvoice/create)"""
        return self._request('POST', '/einvoice/create', query={}, body=body, options=options)

    def einvoice_route(self, id: Any, *, requester: Any = None, options: Optional[RequestOptions] = None) -> Any:
        """"Can I e-invoice this company?" VAT + Peppol + country mandate lookup  (GET /einvoice/route)"""
        return self._request('GET', '/einvoice/route', query={'id': id, 'requester': requester}, body=None, options=options)

    def dd_report(self, body: Any, *, options: Optional[RequestOptions] = None) -> Any:
        """Counterparty due-diligence report (VAT, register, sanctions, EORI, LEI, Peppol) with risk flags  (POST /ddreport)"""
        return self._request('POST', '/ddreport', query={}, body=body, options=options)

    def fr_pa_registry(self, *, name: Any = None, website: Any = None, limit: Any = None, options: Optional[RequestOptions] = None) -> Any:
        """Is this platform on France's official list of Plateformes Agréées (PA)? (free)  (GET /fr/pa-registry)"""
        return self._request('GET', '/fr/pa-registry', query={'name': name, 'website': website, 'limit': limit}, body=None, options=options)

    def extract_einvoice_from_pdf(self, body: Any = None, *, format: Any = None, options: Optional[RequestOptions] = None) -> Any:
        """AI draft from a plain PDF invoice -> EN 16931 / XRechnung (for review)  (POST /einvoice/extract)"""
        return self._request('POST', '/einvoice/extract', query={'format': format}, body=body, options=options)

    def einvoice_sample(self, *, type: Any = None, options: Optional[RequestOptions] = None) -> Any:
        """Example JSON body for POST /einvoice/create (free)  (GET /einvoice/sample)"""
        return self._request('GET', '/einvoice/sample', query={'type': type}, body=None, options=options)

    def send_einvoice(self, body: Any, *, options: Optional[RequestOptions] = None) -> Any:
        """SANDBOX: verify buyer -> create -> validate -> route -> transmit (mock or partner Peppol sandbox) -> signed evidence receipt  (POST /einvoice/send)"""
        return self._request('POST', '/einvoice/send', query={}, body=body, options=options)

    def preflight_einvoice(self, body: Any, *, options: Optional[RequestOptions] = None) -> Any:
        """Safe send: check the buyer and the invoice before sending (VAT, Peppol, sanctions, EN 16931) -> ok / warn / block  (POST /einvoice/preflight)"""
        return self._request('POST', '/einvoice/preflight', query={}, body=body, options=options)

    def einvoice_evidence_key(self, *, options: Optional[RequestOptions] = None) -> Any:
        """Public key (JWK) for verifying /einvoice/send evidence receipts (free)  (GET /einvoice/evidence-key)"""
        return self._request('GET', '/einvoice/evidence-key', query={}, body=None, options=options)

    def einvoice_usage(self, *, period: Any = None, options: Optional[RequestOptions] = None) -> Any:
        """Aggregate e-invoice usage counts for the current UTC month (free; no PII)  (GET /einvoice/usage)"""
        return self._request('GET', '/einvoice/usage', query={'period': period}, body=None, options=options)
