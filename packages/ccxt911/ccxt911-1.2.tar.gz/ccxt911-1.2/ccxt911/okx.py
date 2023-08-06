import ccxt

class Okx(ccxt.okx):

    def _fetch_account_positions(self,parameter = {}):
        """
        获取账户仓位
        :param parameter:
        :return:
        """
        data = self.private_get_account_positions(parameter)

        return data
    def _fetch_account_balance(self,parameter = {}):
        """
         获取账户余额
        :param parameter:
        :return:
        https://www.okx.com/docs-v5/zh/#rest-api-account-get-balance
        """
        data = self.private_get_account_balance(parameter)
        return data['data'][0]

    def _fetch_account_account(self,parameter = {}):
        """
        instType:产品类型
                    MARGIN：币币杠杆
                    SWAP：永续合约
                    FUTURES：交割合约
                    OPTION：期权
                    instType和instId同时传入的时候会校验instId与instType是否一致，结果返回instId的持仓信息

        :param parameter:
        :return:
        """
        return self.private_get_account_positions(parameter)['data']


    def _fetch_asset_balance(self,parameter = {}):
        """
        获取资金账户余额信息
        :return:
        """
        data = self.privateGetAssetBalances(parameter)['data']

        return data
    def _fetch_asset_total_valuation(self,parameter = {'ccy': 'USDT'}):
        """
        获取资产总估值
        :return:
        {
            "details": {                各个账户的资产估值
                "classic": "124.6",     经典账户
                "earn": "1122.73",      金融账户
                "funding": "0.09",      资金账户
                "trading": "2544.28"    交易账户
            },
            "totalBal": "3790.09",      账户总资产估值
            "ts": "1637566660769"       数据更新时间
        }

        """

        _dict = self.privateGetAssetAssetValuation(parameter)

        return _dict


