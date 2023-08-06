class LBRY_Account():
    def __init__(self,raw_account,LBRY_api,wallet):
        self._LBRY_api = LBRY_api
        self.raw = raw_account
        self.name = raw_account['name']
        self.id = raw_account['id']
        self.certificates = raw_account['certificates'] if 'certificates' in raw_account else 0
        self.satoshis = raw_account['satoshis'] if 'satoshis' in raw_account else 0

        self.public_key = raw_account['public_key']
        self.is_default = raw_account['is_default']
        self.wallet = wallet

    def __str__(self):
        return f"LBRY_Account({self.name})"

    def remove(self):
        self._LBRY_api.remove_account(self)

    def set_as_default(self):
        self._LBRY_api.set_default_account(self.id)

    def new_name(self, new_name):
        self._LBRY_api.request('account_set', {'account_id':self.id,
            'new_name': new_name,
            'wallet_id': self.wallet})
        self.name = new_name
