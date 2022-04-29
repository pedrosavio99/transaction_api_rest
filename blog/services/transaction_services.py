from rest_framework.response import Response
from blog.models import Account, Transaction, Wallet, Status


def send_transaction(user_update, account_model, value, walletUpdate, total_balance):
    transaction_model = Transaction(
            user_payer=user_update,
            account_id=account_model,
            value=float(value),
            status=1)
    
    transaction_model.save()
    walletUpdate.balance = float(total_balance) - float(value)
    walletUpdate.save(update_fields=['balance'])
    return transaction_model.transaction_id 


def make_transaction_services(request):
    try:
        user_id = request.logged_user
        wallet = Wallet.objects.get(user_payer=user_id)

        account = request.data['account']
        bank = request.data['bank']
        branch = request.data['branch']
        value = request.data['value']

        if account == "" or len(account) != 9:
            response = {'message': 'Account number must be 9 digits'}
            return Response(response, status=400)
        
        if bank == "" or len(bank) != 3:
            response = {'message': 'Bank number must be 3 digits'}
            return Response(response, status=400)

        if branch == "" or len(branch) != 3:
            response = {'message': 'Branch number must be 3 digits'}
            return Response(response, status=400)
        
        if float(value) > float(wallet.balance):
            response = {'message': 'You dont have enough money'}
            return Response(response, status=400)
            
        if float(value) < 0:
            response = {'message': 'Use positive values'}
            return Response(response, status=400)
        
        filter_accounts = Account.objects.filter(account_number=float(account)).first()

        if filter_accounts:
            response = {'message': f'Transaction done, account found in our database', 'transaction_id':
                        f'{send_transaction(user_id, filter_accounts, value, wallet, wallet.balance)}'}
            return Response(response, status=200)
            
        else:
            
            account_model = Account(
                account_number=float(account),
                bank=float(bank),
                branch=float(branch),
                )
            account_model.save()
            response = {'message': f'transaction done, New account saved', 'transaction_id':
                        f'{send_transaction(user_id, account_model, value, wallet, wallet.balance)}'}
            return Response(response, status=200)
    except Exception as error:
        response = {"Error": str(error)}
        return Response(response, status=400)


def status_transaction_services(request):
    try:
        transaction_id = request.data['transaction_id']
        new_status = request.data['status']
        transaction = Transaction.objects.filter(transaction_id=transaction_id).first()

        if transaction is None:
            response = {'message': 'Transaction not found'}
            return Response(response, status=400)

        wallet_update = Wallet.objects.get(user_payer=transaction.user_payer)
        old_status = int(transaction.status)

        if transaction_id == "" or new_status == "":
            response = {'message': 'Complete the fields'}
            return Response(response, status=400)
        if int(new_status) > 3 or int(new_status) < 0:
            response = {'message': 'Status nos found'}
            return Response(response, status=400)

        if not transaction:
            response = {'message': 'Transaction not found'}
            return Response(response, status=400)

        if old_status == Status.REJECTED:
            response = {'message': 'Transaction already REJECTED'}
            return Response(response, status=400)
        if old_status == Status.FINISHED:
            response = {'message': 'Transaction already FINISHED'}
            return Response(response, status=400)
        elif int(new_status) == Status.REJECTED:
            wallet_update.balance = float(wallet_update.balance) + float(transaction.value)
            wallet_update.save(update_fields=['balance'])
            transaction.status = int(new_status)
            transaction.save()
            response = {'message': 'Transaction and balance update - REJECTED'}
            return Response(response, status=400)
        elif int(new_status) == Status.FINISHED:
            wallet_update.balance = float(wallet_update.balance)
            wallet_update.save(update_fields=['balance'])
            transaction.status = int(new_status)
            transaction.save()
            response = {'message': 'Transaction and balance update - FINISHED'}
            return Response(response, status=200)
        else:
            transaction.status = int(new_status)
            transaction.save()
            response = {'message': 'Transaction is already - PENDING'}
            return Response(response, status=200)
    except Exception as error:
        response = {"Error": str(error)}
        return Response(response, status=400)

