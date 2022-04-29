from django.http import request
from django.test import Client, TestCase
from blog.models import UserPayer, Wallet
from blog.tests.utils import TestTransactionsUtils


class TestTransactions(TestCase):
    client = Client()

    def setUp(self):
        payload_create_user = {"document": "11111111112111",
                               "name": "pedro",
                               "email": "p@gamil.comm",
                               "password": "123456789"}
        response = self.client.post('/register/', payload_create_user, content_type='application/json')

    def test_created_user(self):
        user = UserPayer.objects.filter(email='p@gamil.comm').first()
        print(user)
        wallet_user = Wallet.objects.filter(user_payer=user).first()

        self.assertEqual(user.email, "p@gamil.comm")
        self.assertEqual(int(wallet_user.balance), 9000000)

    def test_creating_user_repeat(self):
        payload_create_user_same_document = {"document": "11111111112111",
                                             "name": "pedro",
                                             "email": "pedro@gmail.commmm",
                                             "password": "12345678"}
        response_same_doc_error = self.client.post('/register/', payload_create_user_same_document,
                                                   content_type='application/json')

        payload_create_user_same_email = {"document": "11111111111112",
                                          "name": "pedro",
                                          "email": "p@gamil.comm",
                                          "password": "12345678"}
        response_same_email_error = self.client.post('/register/', payload_create_user_same_email,
                                                     content_type='application/json')

        self.assertEqual(response_same_doc_error.data['message'], 'user with the same document already registered')
        self.assertEqual(response_same_email_error.data['message'], 'user with the same email already registered')

    def test_router_login(self):
        payload_login_correct = {"email": "p@gamil.comm", "password": "123456789"}
        response_correct = self.client.post('/login/',
                                            payload_login_correct, content_type='application/json')

        payload_login_wrong_email = {"email": "pedro@gmail.commm", "password": "123456789"}
        response_wrong_email = self.client.post('/login/',
                                                payload_login_wrong_email, content_type='application/json')

        payload_login_wrong_password = {"email": "p@gamil.comm", "password": "12345679324"}
        response_wrong_password = self.client.post('/login/',
                                                   payload_login_wrong_password, content_type='application/json')

        self.assertEqual(response_correct.status_code, 200)
        self.assertEqual(response_correct.data['message'], 'welcome')

        self.assertEqual(response_wrong_email.status_code, 400)
        self.assertEqual(response_wrong_email.data['message'], 'Incorrect email or password')

        self.assertEqual(response_wrong_password.status_code, 400)
        self.assertEqual(response_wrong_password.data['message'], 'Incorrect email or password')

    def test_autenticated_router_make_transaction(self):
        token = TestTransactionsUtils.get_token(self, 'p@gamil.comm', '123456789')

        payload_transaction = {
            "account": "911111212",
            "bank": "111",
            "branch": "111",
            "value": "10.35"}

        self.client = Client(HTTP_AUTHORIZATION=token)
        response_transaction = self.client.post('/transaction/', payload_transaction, content_type='application/json')

        self.assertEqual(response_transaction.data['message'], 'transaction done, New account saved')
        self.assertEqual(response_transaction.status_code, 200)

    def test_transaction_done(self):
        token = TestTransactionsUtils.get_token(self, 'p@gamil.comm', '123456789')
        self.client = Client(HTTP_AUTHORIZATION=token)

        payload_correct = {
            "account": "911111212",
            "bank": "111",
            "branch": "111",
            "value": "10000"}

        response_payload_correct = self.client.post('/transaction/', payload_correct)

        payload_account_few_numbers = {
            "account": "9111112",
            "bank": "111",
            "branch": "111",
            "value": "10000"}

        response_wrong_account = self.client.post('/transaction/', payload_account_few_numbers)

        payload_account_many_numbers = {
            "account": "91111121444444444444444444444442",
            "bank": "111",
            "branch": "111",
            "value": "10000"}

        response_account_many_numbers = self.client.post('/transaction/', payload_account_many_numbers)

        payload_bank_many_numbers = {
            "account": "911111212",
            "bank": "1111111111111111111111111111111111111111111111111",
            "branch": "111",
            "value": "10000"}

        response_bank_many_numbers = self.client.post('/transaction/', payload_bank_many_numbers)

        payload_bank_few_numbers = {
            "account": "911111212",
            "bank": "1",
            "branch": "111",
            "value": "10000"}

        response_bank_few_numbers = self.client.post('/transaction/', payload_bank_few_numbers)

        payload_branch_few_numbers = {
            "account": "911111212",
            "bank": "111",
            "branch": "1",
            "value": "10000"}

        response_branch_few_numbers = self.client.post('/transaction/', payload_branch_few_numbers)

        payload_branch_many_numbers = {
            "account": "911111212",
            "bank": "111",
            "branch": "1111111111111111111111111111111111111111111111111111",
            "value": "10000"}

        response_branch_many_numbers = self.client.post('/transaction/', payload_branch_many_numbers)

        payload_negative_value = {
            "account": "911111212",
            "bank": "111",
            "branch": "111",
            "value": "-1000000"}

        response_negative_value = self.client.post('/transaction/', payload_negative_value)

        payload_high_transaction_value = {
            "account": "911111212",
            "bank": "111",
            "branch": "111",
            "value": "1000000000000000000000000"}

        response_high_transaction_value = self.client.post('/transaction/', payload_high_transaction_value)

        user = UserPayer.objects.filter(document=int('11111111112111')).first()
        filter_wallet = Wallet.objects.get(user_payer=user)

        self.assertEqual(response_payload_correct.data['message'], 'transaction done, New account saved')
        self.assertEqual(response_payload_correct.status_code, 200)

        self.assertEqual(response_wrong_account.data['message'], 'Account number must be 9 digits')
        self.assertEqual(response_wrong_account.status_code, 400)
        self.assertEqual(response_account_many_numbers.data['message'], 'Account number must be 9 digits')
        self.assertEqual(response_wrong_account.status_code, 400)
        self.assertEqual(response_bank_many_numbers.data['message'], 'Bank number must be 3 digits')
        self.assertEqual(response_bank_many_numbers.status_code, 400)
        self.assertEqual(response_bank_few_numbers.data['message'], 'Bank number must be 3 digits')
        self.assertEqual(response_bank_few_numbers.status_code, 400)
        self.assertEqual(response_branch_few_numbers.data['message'], 'Branch number must be 3 digits')
        self.assertEqual(response_branch_few_numbers.status_code, 400)
        self.assertEqual(response_branch_many_numbers.data['message'], 'Branch number must be 3 digits')
        self.assertEqual(response_branch_many_numbers.status_code, 400)
        self.assertEqual(response_negative_value.data['message'], 'Use positive values')
        self.assertEqual(response_negative_value.status_code, 400)
        self.assertEqual(response_high_transaction_value.data['message'], 'You dont have enough money')
        self.assertEqual(response_high_transaction_value.status_code, 400)

        self.assertEqual(float(filter_wallet.balance), 8990000.0)

    def test_auth_status_transaction(self):
        token = TestTransactionsUtils.get_token(self, 'p@gamil.comm', '123456789')
        self.client = Client(HTTP_AUTHORIZATION=token)

        payload_trans_01 = {
            "account": "911111212",
            "bank": "111",
            "branch": "111",
            "value": "10.35"}

        payload_trans_02 = {
            "account": "911111212",
            "bank": "111",
            "branch": "111",
            "value": "10.35"}

        payload_trans_03 = {
            "account": "911111212",
            "bank": "111",
            "branch": "111",
            "value": "10.35"}

        self.client = Client(HTTP_AUTHORIZATION=token)
        response_pending = self.client.post('/transaction/', payload_trans_01, content_type='application/json')
        response_finished = self.client.post('/transaction/', payload_trans_02, content_type='application/json')
        response_rejected = self.client.post('/transaction/', payload_trans_03, content_type='application/json')

        payload_finished = {
                            "transaction_id": "1",
                            "status": "2"}

        payload_finished_again = {
                                  "transaction_id": "1",
                                  "status": "2"}

        payload_rejected = {
                            "transaction_id": "2",
                            "status": "3"}

        payload_rejected_again = {
                                  "transaction_id": "2",
                                  "status": "3"}

        self.client = Client(HTTP_AUTHORIZATION=token)
        response_change_status = self.client.post('/transaction_auth/', payload_finished)
        response_change_status_finished2 = self.client.post('/transaction_auth/', payload_finished_again)
        response_change_status_rejected = self.client.post('/transaction_auth/', payload_rejected)
        response_change_status_rejected2 = self.client.post('/transaction_auth/', payload_rejected_again)

        self.assertEqual(response_change_status.data['message'], 'Transaction and balance update - FINISHED')
        self.assertEqual(response_change_status_finished2.data['message'], 'Transaction already FINISHED')
        self.assertEqual(response_change_status_rejected.data['message'], 'Transaction and balance update - REJECTED')
        self.assertEqual(response_change_status_rejected2.data['message'], 'Transaction already REJECTED')
