from bancorml.environments.env_base import EnvBase
from bancorml.agents import LiquidityProviderAgent


class Bancor3(EnvBase):
    """Bancor3 Environment.

        Args:
            is_solidity (bool): Toggles between floating-point-signed and fixed-point-unsigned
            min_liquidity_threshold (float): The BancorDAO prescribes a liquidity threshold, denominated in BNT, that represents the minimum available liquidity that must be present before the protocol bootstraps the pool with BNT.
            bnt_funding_limit (int): The BancorDAO determines the available liquidity for trading, through adjustment of the “BNT funding limit” parameter.
            alpha (float): Alpha value in the EMA equation.
            pool_fees (dict): Dictionary of tkn:fee (str:float) key-values per pool.
            cooldown_period (int): The cooldown period in days.
            exit_fee (float): The global exit fee.
            spot_prices (dict): Dictionary of tkn:price (str:float) key-values per tkn.
            whitelisted_tokens (list): List of token tickernames indicating whitelist status approval.
            bootstrapped_tokens (list): List of DAOmsig initiated pools/tokens.
            vortex_rates (dict): Dictionary of tkn:rate (str:float) key-values per TKN.
        """

    name = "Bancor3 Environment"
    block_num = 0
    ema = {
        'TKN': {'block_num': [0], 'ema': [0]},
        'BNT': {'block_num': [0], 'ema': [0]},
        'wBTC': {'block_num': [0], 'ema': [0]},
        'ETH': {'block_num': [0], 'ema': [0]},
        'LINK': {'block_num': [0], 'ema': [0]}
    }

    def __init__(
            self,
            block_num=0,
            alpha=0.2,
            is_solidity=False,
            min_liquidity_threshold=1000,
            exit_fee=.0025,
            cooldown_period=7,
            bnt_funding_limit=100000,
            external_price_feed={
                        "TKN": {'block_num': [0, 1, 2, 3],
                                'price_usd': [2.50, 2.49, 2.51, 2.50]},
                        "BNT": {'block_num': [0, 1, 2, 3],
                                'price_usd': [2.50, 2.49, 2.51, 2.50]},
                        "LINK": {'block_num': [0, 1, 2, 3],
                                'price_usd': [15.35, 15.20, 15.11, 15.00]},
                        "ETH": {'block_num': [0, 1, 2, 3],
                                'price_usd': [2550.00, 2400.00, 2450.00, 2500.00]},
                        "wBTC": {'block_num': [0, 1, 2, 3],
                                'price_usd': [40123.23, 40312.21, 40111.11, 40000.00]}
            },
            pool_fees={
                "TKN": 0.01,
                "BNT": 0.01,
                "LINK": 0.01,
                "ETH": 0.01,
                "wBTC": 0.01
            },
            whitelisted_tokens=[],
            bootstrapped_tokens=[],
            exchange_rates={},
            spot_prices={
                "TKN": {'block_num': [0],
                        'price_usd': [2.50]},
                "BNT": {'block_num':[0],
                        'price_usd':[2.50]},
                "LINK": {'block_num':[0],
                        'price_usd':[15.00]},
                "ETH": {'block_num':[0],
                        'price_usd':[2500.00]},
                "wBTC": {'block_num':[0],
                        'price_usd':[40000.00]}
            },
            vortex_rates={
                "TKN": 0.2,
                "BNT": 0.2,
                "LINK": 0.2,
                "ETH": 0.2,
                "wBTC": 0.2
            },
            dao_msig_initialized_pools=[],
            verbose=True,
            **kwargs
    ):

        super().__init__()

        self.set_param(alpha=alpha,
                       spot_prices=spot_prices,
                       vortex_rates=vortex_rates,
                       block_num=block_num,
                       exchange_rates=exchange_rates,
                       min_liquidity_threshold=min_liquidity_threshold,
                       bnt_funding_limit=bnt_funding_limit,
                       exit_fee=exit_fee,
                       cooldown_period=cooldown_period,
                       pool_fees=pool_fees,
                       bootstrapped_tokens=bootstrapped_tokens,
                       whitelisted_tokens=whitelisted_tokens,
                       external_price_feed=external_price_feed,
                       is_solidity=is_solidity,
                       dao_msig_initialized_pools=dao_msig_initialized_pools,
                       verbose=verbose)

        for tkn in self.available_liquidity_ledger:
            self.available_liquidity_ledger[tkn]['funding_limit'][-1] = bnt_funding_limit

        self.protocol_agent = LiquidityProviderAgent(env=self, unique_id="Bancor Protocol")
        self._ema = Bancor3.ema

    def unstake(self, tkn, x, p=0, q=0, r=0, s=0, t=0, u=0):
        """Bancor3 Unstake protocol logic

        Args:
            x (int or float): The precise TKN value of the bnTKN tokens being withdrawn.
            uid (str or int): The agent user id (default=0)
            tkn (str): The abbreviated token name (default=BNT, valid options are as listed on CoinGecko)

        Returns:
            tkn_out (int or float or decimal): The x of TKN to return to the user
            bnt_out (int or float or decimal): The x of BNT to return to the user
        """
        if tkn == 'BNT':
            exchange_rate =  self.staking_ledger['BNT'][-1] / self.pool_token_supply_ledger['bnBNT_ERC20_contract']['supply'][-1]
            bnt = exchange_rate * x
            exit_fee = self.exit_fee * bnt
            tkn_out = 0
            bnt_out = bnt - exit_fee
        else:
            a, b, c, e, m, n, x, w = self.validate_input_types(tkn, x)

            # check surplus
            self.tokenomics.check_surplus(b, c, e, n)

            # check hlim
            self.tokenomics.check_hlim(b, c, e, x)

            # check hmax
            self.tokenomics.check_hmax(b, c, e, m, n, x, self.tokenomics.surplus)

            # check if trading liquidity needs reduced
            self.tokenomics.check_reduce_trading_liquidity(x, b, c, e, n,
                                                           self.tokenomics.surplus,
                                                           self.tokenomics.satisfies_hmax,
                                                           self.tokenomics.satisfies_hlim)

            # check case (e.g. "default surplus", "arbitrage deficit", etc...)
            case = self.check_case(self.tokenomics.surplus,
                                   self.tokenomics.deficit,
                                   self.tokenomics.satisfies_hlim,
                                   self.tokenomics.satisfies_hmax,
                                   self.tokenomics.reduce_trading_liquidity,
                                   a, b, c, e, w)

            if case in ['bootstrap surplus', 'bootstrap surplus (special case)']:
                s = self.tokenomics.handle_bootstrap_surplus(x, n)

            elif case == 'bootstrap deficit (special case)':
                s = self.tokenomics.handle_bootstrap_deficit_special_case(c, e, n, x)

            elif case == 'arbitrage surplus':
                p, r, s = self.tokenomics.handle_arbitrage_surplus(x, n, a, b, c, e, m)

            elif case == 'default surplus':
                p, q, r, s = self.tokenomics.handle_default_surplus(x, n, c, a, b)

            elif case == 'arbitrage deficit':
                p, r, s = self.tokenomics.handle_arbitrage_deficit(x, n, a, m, e, b, c)

            elif case == 'bootstrap deficit':
                s, t = self.tokenomics.handle_bootstrap_deficit(x, n, b, c, e, a)

            elif case == 'default deficit':
                p, q, r, s, t = self.tokenomics.handle_default_deficit(a, b, c, e, n, x)

            if tkn in self.external_protection_wallet_ledger:
                external_wallet_case = self.tokenomics.check_external_wallet_adjustment(a, b, w, t, self.tokenomics.satisfies_hlim, self.tokenomics.satisfies_hmax)

                if external_wallet_case == 'external wallet adjustment (1)':
                    t, u = self.tokenomics.handle_external_wallet_adjustment_1(t, b, a)
                    case = case + ' ep1'

                elif external_wallet_case == 'external wallet adjustment (2)':
                    t, u = self.tokenomics.handle_external_wallet_adjustment_2(w, t, b, a)
                    case = case + ' ep2'

            # update ledger balances based on the current state
            self.update_ledger_balances(tkn, p, q, r, s, t, u, a, b, c, e, m, n, x, w, case)
            tkn_out = s + u
            bnt_out = t

        self.check_pool_shutdown()
        return tkn_out, bnt_out

    def stake(self, tkn, x, block_num):
        """Main protocol logic to perform staking functionality

        Args:
            tkn (str): The abbreviated token name (default=BNT, valid options are as listed on CoinGecko)
            x (int or float): The precise TKN value of the bnTKN tokens being withdrawn.

        Returns:
            y (int or float or decimal): the number of pool tokens issued to the user.
        """
        if block_num != self.block_num:
            self.update_ema(tkn)
            self.block_num = block_num

        assert tkn in self.whitelisted_tokens, 'The token is not supported'
        if tkn == 'BNT':
            exchange_rate =   self.pool_token_supply_ledger['bnBNT_ERC20_contract']['supply'][-1] / self.staking_ledger['BNT'][-1]
            y = exchange_rate * x
        else:
            y = self.mint_bntkn(tkn, x)
            self.add_tkn_to_vault(tkn, x)
            self.add_tkn_to_staking_ledger(tkn, x)
            if self.is_within_ema_tolerance(tkn) and (tkn in self.dao_msig_initialized_pools):
                self.add_tkn_to_available_liquidity_ledger(tkn, x)
            self.check_bootstrapped_tokens()

        self.check_pool_shutdown()
        return (y)

    def trade(self, tkn1, x, tkn2, block_num, update_liquidity=False):
        """Main protocol logic to perform trading functionality.

        Args:
            tkn1 (str): The abbreviated token name being traded-in
            x (int or float): The precise TKN value of tkn1 being traded.
            tkn2 (str): The abbreviated token name being traded-for (i.e., sent back to the user)

        Returns:
            tkn_out (int or float or decimal): the number of pool tokens issued to the user.
        """
        if block_num != self.block_num:
            self.update_ema(tkn1)
            self.update_ema(tkn2)
            self.block_num = block_num

        if (tkn1=='BNT') or (tkn2=='BNT'):

            if tkn1=='BNT':
                tkn_a = tkn2
                operation = self.tokenomics.handle_trade_bnt_to_tkn

            elif tkn2=='BNT':
                tkn_a = tkn1
                operation = self.tokenomics.handle_trade_tkn_to_bnt

            a = self.available_liquidity_ledger[tkn_a]['BNT'][-1]
            b = self.available_liquidity_ledger[tkn_a][tkn_a][-1]
            d = self.pool_fees[tkn_a]
            e = self.vortex_rates[tkn_a]
            bnt_trading_liquidity, tkn_trading_liquidity, tkn_out, tkn_fee, vortex_fee = operation(
                a, d, b, x, e)

            if self.is_within_ema_tolerance(tkn_a) or update_liquidity:
                self.update_available_liquidity_ledger(tkn_a, bnt_trading_liquidity, tkn_trading_liquidity)

            self.add_tkn_to_vault(tkn1, x)
            self.add_tkn_to_vault(tkn2, -tkn_out)
            self.add_tkn_to_staking_ledger(tkn2, tkn_fee)
            self.add_tkn_to_vortex_ledger(vortex_fee)

            print(f'bnt_trading_liquidity={bnt_trading_liquidity}, \n'
                  f'tkn_trading_liquidity={tkn_trading_liquidity}, \n'
                  f'tkn_out={tkn_out}, \n'
                  f'tkn_fee={tkn_fee}, \n'
                  f'vortex_fee={vortex_fee} \n\n')

        else:

            a1 = self.available_liquidity_ledger[tkn1]['BNT'][-1]
            b1 = self.available_liquidity_ledger[tkn1][tkn1][-1]
            d1 = self.pool_fees[tkn1]

            a2 = self.available_liquidity_ledger[tkn2]['BNT'][-1]
            b2 = self.available_liquidity_ledger[tkn2][tkn2][-1]
            d2 = self.pool_fees[tkn2]

            e = self.vortex_rates[tkn1]

            bnt_source_trading_liquidity, tkn_source_trading_liquidity, bnt_destination_trading_liquidity, tkn_destination_trading_liquidity, tkn_out, bnt_fee, tkn_fee, vortex_fee = self.tokenomics.handle_trade_tkn_to_tkn(
                a1, d1, b1, a2, d2, b2, x, e)

            if self.is_within_ema_tolerance(tkn1):
                self.update_available_liquidity_ledger(tkn1, bnt_source_trading_liquidity, tkn_source_trading_liquidity)

            if self.is_within_ema_tolerance(tkn2):
                self.update_available_liquidity_ledger(tkn2, bnt_destination_trading_liquidity, tkn_destination_trading_liquidity)

            self.add_tkn_to_vault(tkn1, x)
            self.add_tkn_to_vault(tkn2, -tkn_out)
            self.add_tkn_to_staking_ledger(tkn2, tkn_fee)
            self.add_tkn_to_staking_ledger('BNT', bnt_fee)
            self.add_tkn_to_vortex_ledger(vortex_fee)

            print(f'bnt_source_trading_liquidity={bnt_source_trading_liquidity}, \n',
                  f'tkn_source_trading_liquidity={tkn_source_trading_liquidity}, \n',
                  f'bnt_destination_trading_liquidity={bnt_destination_trading_liquidity}, \n',
                  f'tkn_destination_trading_liquidity={tkn_destination_trading_liquidity}, \n',
                  f'tkn_out={tkn_out}, \n',
                  f'bnt_fee={bnt_fee}, \n',
                  f'tkn_fee={tkn_fee}, \n',
                  f'vortex_fee={vortex_fee} \n')

        self.check_pool_shutdown()

        for token in [tkn1, tkn2]:
            self.update_spot_prices(token)

        return tkn_out

