import ccxt
import pandas as pd
import time

class Binance(ccxt.binance):

    def _fetch_asset_total_valuation(self):
        """
        获取总资产估值
        :return: 返回总资产估值
        """
        pass

    def _fetch_spot_balance(self):
        """
        获取当前账户的现货资产数量
        :return:
        [
        {'asset': 'BTC', 'free': 0.0, 'locked': 0.0, 'total': 0.0}，
        {'asset': 'LTC', 'free': 0.0, 'locked': 0.0, 'total': 0.0}，
        {'asset': 'ETH', 'free': 0.0, 'locked': 0.0, 'total': 0.0}，
        ]
        """
        df = pd.DataFrame(self.fetch_balance()["info"]["balances"])
        df['free'] = df['free'].astype(float)
        df['locked'] = df['locked'].astype(float)
        df['total'] = df['free']+df['locked']
        return df.to_dict(orient='records')

    def _fetch_valuation_from_coin(self,coin):
        """
        获取币的USDT估值
        :param coin:现货币种
        :return:返回估值
        """
        if  coin =='USDT' or coin =='BUSD':
            return 1

        valuation_coin = ['USDT','BUSD','BTC','ETH']
        for i in valuation_coin:
            try:
                if i == 'USDT' or i =='BUSD':
                    symbol = coin + i
                    valuation = self._fetch_ticker({'symbol':symbol})
                    return valuation
                else:
                    symbol = coin + i
                    valuation = self._fetch_ticker({'symbol': symbol})
                    _ = i+'USDT'
                    reference_price=self._fetch_ticker({'symbol': _})
                    return valuation*reference_price
            except Exception as e:
                print(f"报错:{e}  报错函数：_fetch_valuation_from_coin")
        else:
            print(f"：没有交易对或API错误 _fetch_valuation_from_coin")
            exit()



    def _fetch_ticker(self,parameter = {}):
        """
        获取现货最新价格
        :param parameter:
        {
            symbol	: "BTCUSDT"#添加交易对 不填写交易对返回所有信息
        }
        :return:返回交易对价格
        """
        data = self.public_get_ticker_price(parameter)
        return float(data['price'])


    def _fetch_u_futures_account(self):
        """
        获取U本位合约账户
        {
            "symbol": "BTCUSDT",  // 交易对
            "initialMargin": "0",   // 当前所需起始保证金(基于最新标记价格)
            "maintMargin": "0", //维持保证金
            "unrealizedProfit": "0.00000000",  // 持仓未实现盈亏
            "positionInitialMargin": "0",  // 持仓所需起始保证金(基于最新标记价格)
            "openOrderInitialMargin": "0",  // 当前挂单所需起始保证金(基于最新标记价格)
            "leverage": "100",  // 杠杆倍率
            "isolated": true,  // 是否是逐仓模式
            "entryPrice": "0.00000",  // 持仓成本价
            "maxNotional": "250000",  // 当前杠杆下用户可用的最大名义价值
            "bidNotional": "0",  // 买单净值，忽略
            "askNotional": "0",  // 买单净值，忽略
            "positionSide": "BOTH",  // 持仓方向
            "positionAmt": "0",      // 持仓数量
            "updateTime": 0         // 更新时间
        }
        :return:
        """

        df = pd.DataFrame(self.fapiPrivateV2_get_account()["positions"], dtype=float)#获取合约仓位

        return df.to_dict(orient='records')
    
    def _fet_u_futures_balance(self,):
        """
        获取U本位资产数量
        :return:
        [
            {
            'asset': 'BUSD',
            'total': 5068.86897692,         总资产估值数量
            'balance': 5211.6747775,        所有余额
            'posBalance': -142.80580058,    仓位未实现盈亏
            'free': 3095.78097992,          最大可转出资金
            'crossWalletTotal': 5211.6747775    全仓可用余额
            },

        ]
        """
        try:
            return_data = self.fapiPrivateV2_get_balance()
        except Exception as e:
            print(e)
            exit('_fet_u_futures_balance')

        df = pd.DataFrame(return_data,dtype=float)
        del df['accountAlias']
        del df['updateTime']
        del df['marginAvailable']
        del df['availableBalance']
        df.rename(columns={'crossWalletBalance':'crossWalletTotal','crossUnPnl': 'posBalance','maxWithdrawAmount':'free'}, inplace=True)
        df['total'] = df['balance'] + df['posBalance']
        df = df[['asset','total','balance','posBalance','free','crossWalletTotal']]
        return df.to_dict(orient='records')

    def _fetch_coin_futures_balance(self):
        """
        币本位合约余额
        :return:
        """
        pass

    def _fetch_coin_futures_account(self):
        """
        获取币本位合约账户
        :return:
        """
        pass


    def _fetch_full_lever_balance(self):
        """
        sapi_get_margin_account返回值
        "borrowEnabled": true,
      "marginLevel": "11.64405625",
      "totalAssetOfBtc": "6.82728457",          总资产
      "totalLiabilityOfBtc": "0.58633215",      总欠款
      "totalNetAssetOfBtc": "6.24095242",       净资产
      "tradeEnabled": true,
      "transferEnabled": true,


      "userAssets": [
          {
              "asset": "BTC",
              "borrowed": "0.00000000",
              "free": "0.00499500",
              "interest": "0.00000000",
              "locked": "0.00000000",
              "netAsset": "0.00499500"
          },
          {

        :return:返回BTC净资产* 的USDT
        """
        margin_account = self.sapi_get_margin_account()
        return margin_account

    def _fetch_isolated_lever_balance(self):
        """
        获取逐仓杠杆余额
        :return:

            "totalAssetOfBtc": "0.00000000",
            "totalLiabilityOfBtc": "0.00000000",
            "totalNetAssetOfBtc": "0.00000000"
            ”assets“:[{
         "baseAsset": {
          "asset": "BTC",
          "borrowEnabled": true,
          "borrowed": "0.00000000",
          "free": "0.00000000",
          "interest": "0.00000000",
          "locked": "0.00000000",
          "netAsset": "0.00000000",
          "netAssetOfBtc": "0.00000000",
          "repayEnabled": true,
          "totalAsset": "0.00000000"},
          "quoteAsset":
        {
          "asset": "USDT",
          "borrowEnabled": true,
          "borrowed": "0.00000000",
          "free": "0.00000000",
          "interest": "0.00000000",
          "locked": "0.00000000",
          "netAsset": "0.00000000",
          "netAssetOfBtc": "0.00000000",
          "repayEnabled": true,
          "totalAsset": "0.00000000"
        },
        "symbol": "BTCUSDT"
        "isolatedCreated": true,
        "enabled": true, // 账户是否启用，true-启用，false-停用
        "marginLevel": "0.00000000",
        "marginLevelStatus": "EXCESSIVE", // "EXCESSIVE", "NORMAL", "MARGIN_CALL", "PRE_LIQUIDATION", "FORCE_LIQUIDATION"
        "marginRatio": "0.00000000",
        "indexPrice": "10000.00000000",
        "liquidatePrice": "1000.00000000",
        "liquidateRate": "1.00000000",
        "tradeEnabled": true,]


        """
        data = self.sapi_get_margin_isolated_account()

        return data







