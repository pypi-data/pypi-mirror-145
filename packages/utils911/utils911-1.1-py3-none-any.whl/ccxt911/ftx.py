import ccxt

class Ftx(ccxt.ftx):

    def _fetch_asset_total_valuation(self,parameter = {}):
        """
        获取资产总市值
        :param parameter:
        :return:
        """
        return

    def _fetch_funding_rate(self,parameter = {}):
        """
        获取当前的资金费率，因为FTX是按1小时结算的，所以我们按当前获取的资金费率*8进行计算
        :param parameter:
        {
            'future'：'BTC-PERP'，
        }
        :return:
        {
            "symbol":"BTC-PERP",
            "fundingrate":”0.0025“*8，
        }
        """
        #rate = self.publicGetFundingRates({'future':"BTC-PERP"})
        symbol = parameter['future']
        try:
            rate = self.fetch_funding_rate(symbol=symbol)

            fundingRate = {
                'symbol': symbol,
                'fundingRate': str(float(rate['info']['nextFundingRate']) * 8),
            }
            return fundingRate
        except Exception as e:
            print(e)
            exit('_fetch_funding_rate')

