"""Base Agent Environment Class."""
import logging
from abc import ABC, abstractmethod
from decimal import Decimal
import numpy as np
import pandas as pd
# from bancorml.environments.observation_space import observation_space
# from evalml.utils.logger import get_logger, log_title, log_subtitle
from bancorml.environments.tokenomics.ledgers import VaultLedger, PoolTokenSupplyLedger, ExternalProtectionWalletLedger, \
    StakingLedger, AvailableLiquidityLedger, VortexLedger
from bancorml.utils import FixedPointUnstakeTKN, FloatingPointUnstakeTKN, FixedPointGeneral, FloatingPointGeneral
from bancorml.environments.tokenomics.floating_point_tokenomics import FloatingPointTokenomics
from bancorml.environments.tokenomics.fixed_point_tokenomics import FixedPointTokenomics
from fxpmath import Fxp

# logger = logging.getLogger(__name__)
from bancorml.utils.schemas import FixedPoint


class EnvBase(ABC):
    """Environment base for multi-agent-oriented system.

    Args:
        observation_space (obj): Gym.Spaces class instance which defines respective agent-oriented observation spaces
        random_seed (int): Seed for the random number generator. Defaults to 0.
    """
    metadata = {'render.modes': []}


    def __init__(
        self,
        # observation_space=observation_space,
    ):
        # self.observation_space = observation_space
        # self._external_price_feed = external_price_feed
        # self.logger = get_logger(f"{__name__}")

        # create a vault
        self.vault_ledger = VaultLedger().ledger

        # create a staking ledger
        self.staking_ledger = StakingLedger().ledger

        # create a single liquidity pool for the model
        self.pool_token_supply_ledger = PoolTokenSupplyLedger().ledger

        # create a external protection wallet for the model
        self.external_protection_wallet_ledger = ExternalProtectionWalletLedger().ledger

        # create a ledger to track available liquidity
        self.available_liquidity_ledger = AvailableLiquidityLedger().ledger

        self.vortex_ledger = VortexLedger().ledger
        self.actions = 0

    @property
    def min_liquidity_threshold(self) -> int or float:
        """Minimum pool liquidity threshold before the DAOmsig can initiate."""
        return self._min_liquidity_threshold

    @min_liquidity_threshold.setter
    def min_liquidity_threshold(self, updated_min_liquidity_threshold: int or float):
        self._min_liquidity_threshold = updated_min_liquidity_threshold

    @property
    def warning_only(self) -> bool:
        """If True then will cause exception and break whenever a negative balance is found."""
        return self._warning_only

    @warning_only.setter
    def warning_only(self, updated_warning_only: bool):
        self._warning_only = updated_warning_only

    @property
    def bnt_funding_limit(self) -> int or float:
        """The BancorDAO determines the available liquidity for trading, through adjustment of the “BNT funding limit” parameter."""
        return self._bnt_funding_limit

    @bnt_funding_limit.setter
    def bnt_funding_limit(self, updated_bnt_funding_limit: int or float):
        self._bnt_funding_limit = updated_bnt_funding_limit

    @property
    def alpha(self) -> float:
        """EMA calculation alpha setting"""
        return self._alpha

    @alpha.setter
    def alpha(self, updated_alpha: float):
        self._alpha = updated_alpha

    @property
    def verbose(self) -> bool:
        """Whether to print system state during processing"""
        return self._verbose

    @verbose.setter
    def verbose(self, updated_verbose: bool):
        self._verbose = updated_verbose

    @property
    def whitelisted_tokens(self) -> list:
        """List of approved tokens allowed on Bancor v3"""
        return self._whitelisted_tokens

    @whitelisted_tokens.setter
    def whitelisted_tokens(self, updated_whitelist: list):
        self._whitelisted_tokens = updated_whitelist

    @property
    def dao_msig_initialized_pools(self) -> list:
        """List of DAOmsig initialized pools on Bancor v3"""
        return self._dao_msig_initialized_pools

    @dao_msig_initialized_pools.setter
    def dao_msig_initialized_pools(self, updated_dao_msig_initialized_pools: list):
        self._dao_msig_initialized_pools = updated_dao_msig_initialized_pools

    @property
    def external_price_feed(self) -> dict:
        """List of approved tokens allowed on Bancor v3"""
        return self._external_price_feed

    @external_price_feed.setter
    def external_price_feed(self, updated_external_price_feed: dict):
        self._external_price_feed = updated_external_price_feed

    @property
    def bootstrapped_tokens(self) -> list:
        """List of whitelisted tkn pools on Bancor v3 which meet the minimum pool liquidity threshold"""
        return self._bootstrapped_tokens

    @bootstrapped_tokens.setter
    def bootstrapped_tokens(self, updated_bootstrapped_tokens: list):
        self._bootstrapped_tokens = updated_bootstrapped_tokens

    @property
    def vortex_rates(self) -> dict:
        """The Bancor Vortex accrues value from its share of the revenues is used to buy and burn vBNT to provide IL protection."""
        return self._vortex_rates

    @vortex_rates.setter
    def vortex_rates(self, updated_vortex_rates: dict):
        self._vortex_rates = updated_vortex_rates

    @property
    def pool_fees(self) -> dict:
        """Protocol revenue (i.e. the pool fees, or the commissions paid by traders) is distributed to users by increasing the balance of the staking ledger, equal to the value captured."""
        return self._pool_fees

    @pool_fees.setter
    def pool_fees(self, updated_pool_fees: dict):
        self._pool_fees = updated_pool_fees

    @property
    def exit_fee(self) -> Decimal:
        """
        As a final circumspection against bad behavior,
        exit fees are introduced into the Bancor ecosystem for the first time.
        The exit fee is designed to temper the profit motive of the imagined exploit vector.
        """
        return self._exit_fee

    @exit_fee.setter
    def exit_fee(self, updated_exit_fee: Decimal):
        self._exit_fee = updated_exit_fee

    @property
    def exchange_rates(self) -> dict:
        """BNT to TKN exchange rate, effectively swapping out an equal quantity of BNT value for TKN value, until there is no TKN remaining."""
        return self._exchange_rates

    @exchange_rates.setter
    def exchange_rates(self, updated_exchange_rates: dict):
        self._exchange_rates = updated_exchange_rates

    @property
    def ema(self) -> dict:
        """Exponential Moving Average (EMA) used to test spot price tolerance."""
        return self._ema

    @ema.setter
    def ema(self, updated_ema: dict):
        self._ema = updated_ema

    @property
    def spot_prices(self) -> dict:
        """Current system state spot prices. Setting these will cause an auto-update"""
        return self._spot_prices

    @spot_prices.setter
    def spot_prices(self, updated_spot_prices: dict):
        self._spot_prices = updated_spot_prices

    @property
    def custom_name(self):
        """Custom name of the env."""
        return self._custom_name

    @property
    def name(self):
        """Name of the env."""
        return self.custom_name or self.summary

    def set_param(self, is_solidity=None,
                        block_num=None,
                        min_liquidity_threshold=None,
                        bnt_funding_limit=None,
                        alpha=None,
                        pool_fees=None,
                        cooldown_period=None,
                        exit_fee=None,
                        spot_prices=None,
                        whitelisted_tokens=None,
                        bootstrapped_tokens=None,
                        exchange_rates=None,
                        external_price_feed=None,
                        vortex_rates=None,
                        dao_msig_initialized_pools=None,
                        warning_only=None,
                        verbose=None
                  ):
        """Allows user to set the specified system parameters.

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

        Returns:
            self
        """
        if block_num is not None:
            self.block_num = block_num
        if is_solidity is not None:
            self.is_solidity = is_solidity
            self.tokenomics = FixedPointTokenomics() if is_solidity else FloatingPointTokenomics()
        if verbose is not None:
            self.verbose = verbose
        if exchange_rates is not None:
            self.exchange_rates = exchange_rates
        if min_liquidity_threshold is not None:
            self.min_liquidity_threshold = min_liquidity_threshold
        if bnt_funding_limit is not None:
            self.bnt_funding_limit = bnt_funding_limit
        if alpha is not None:
            self.alpha = alpha
        if warning_only is not None:
            self.warning_only = warning_only
        if cooldown_period is not None:
            self.cooldown_period = cooldown_period
        if pool_fees is not None:
            self.pool_fees = pool_fees
        if exit_fee is not None:
            self.exit_fee = exit_fee
        if whitelisted_tokens is not None:
            self.set_whitelisted_tokens(whitelisted_tokens)
        if vortex_rates is not None:
            self.vortex_rates = vortex_rates
        if external_price_feed is not None:
            self.external_price_feed = external_price_feed
        if bootstrapped_tokens is not None:
            self.bootstrapped_tokens = bootstrapped_tokens
        if dao_msig_initialized_pools is not None:
            self.dao_msig_initialized_pools = dao_msig_initialized_pools
        if spot_prices is not None:
            self.spot_prices = spot_prices

        self.update_exchange_rates()
        self.init_ema()

    def init_tokens(self, add_tkns=[]):
        whitelisted_tokens = self.whitelisted_tokens
        external_price_feed = self.external_price_feed
        pool_fees = self.pool_fees
        vortex_rates = self.vortex_rates
        spot_prices = self.spot_prices
        ema = self.ema

        for tkn in add_tkns:
            if tkn not in whitelisted_tokens:
                whitelisted_tokens.append(tkn)

        for tkn in whitelisted_tokens:
            if tkn not in external_price_feed:
                if self.verbose:
                    print(f'WARNING: {tkn} was added to external_price_feed at 1.00 USD \n'
                          f'You can update this with the .update_external_price(tkn, external_price) method. \n')
                external_price_feed[tkn] =  {'block_num': [self.block_num],
                                             'price_usd': [1.00]}
            if tkn not in pool_fees:
                if self.verbose:
                    print(f'WARNING: {tkn} was added to pool_fees at 0.01 \n'
                          f'You can update this with the .update_pool_fee(tkn, pool_fee) method. \n')
                pool_fees[tkn] = 0.01

            if tkn not in vortex_rates:
                if self.verbose:
                    print(f'WARNING: {tkn} was added to vortex_rates at 0.2 \n'
                          f'You can update this with the .update_vortex_rate(tkn, vortex_rate) method. \n')
                vortex_rates[tkn] = 0.2

            if tkn not in spot_prices:
                if self.verbose:
                    print(f'WARNING: {tkn} was added to spot_prices at $1 USD \n'
                          f'You can update this with the .update_spot_price(tkn, price_usd) method. \n')
                spot_prices[tkn] = {'block_num': [self.block_num],
                                    'price_usd': [1.00]}

            if tkn not in self.vault_ledger:
                self.vault_ledger[tkn] = [0]
            if f"bn{tkn}_ERC20_contract" not in self.pool_token_supply_ledger:
                self.pool_token_supply_ledger[f"bn{tkn}_ERC20_contract"] = {'block_num': [0], 'supply': [0]}
            if tkn not in self.staking_ledger:
                self.staking_ledger[tkn] = [0]
            if tkn not in self.external_protection_wallet_ledger:
                self.external_protection_wallet_ledger[tkn] = [0]
            if tkn not in self.available_liquidity_ledger:
                self.available_liquidity_ledger[tkn] = {
                    'block_num': [self.block_num],
                    'funding_limit': [self.bnt_funding_limit],
                    'BNT': [0],
                    tkn: [0]
                }

            self.update_exchange_rates()
            if tkn not in ema:
                if self.verbose:
                    print(
                        f'WARNING: {tkn} was added to ema at the current exchange rate of {self.exchange_rates[tkn]} \n'
                        f'You can update this with the .update_ema(tkn, ema_value) method. \n')
                ema[tkn] = {'block_num': [self.block_num],
                            'ema': [self.exchange_rates[tkn]]}


        self.ema = ema
        self.whitelisted_tokens = whitelisted_tokens
        self.spot_prices = spot_prices
        self.external_price_feed = external_price_feed
        self.vortex_rates = vortex_rates
        self.pool_fees = pool_fees


    def init_ema(self):
        ema = self.ema
        for tkn in self.spot_prices:
            if tkn in ema:
                ema[tkn]['block_num'] = [self.block_num]
                ema[tkn]['ema'] = [self.exchange_rates[tkn]]
        self.ema = ema

    def get_available_liquidity_ledger(self, tkn):
        """Gets the available trading liquidity ledger.

        Args:
            tkn (str): Tickername of the token of interest.
        Returns:
            (pd.DataFrame): DataFrame of available_liquidity_ledger logging.
        """
        return pd.DataFrame.from_dict(self.available_liquidity_ledger[tkn])

    def get_vortex_ledger(self):
        """Gets the vortex ledger.

        Returns:
            (pd.DataFrame): DataFrame of vortex logging.
        """
        return pd.DataFrame.from_dict(self.vortex_ledger)

    def get_vault_ledger(self):
        """Gets the vault ledger.

        Returns:
            (pd.DataFrame): DataFrame of vault ledger logging.
        """
        return pd.DataFrame.from_dict(self.vault_ledger)

    def get_staking_ledger(self):
        """Gets the staking ledger.

        Returns:
            (pd.DataFrame): DataFrame of staking ledger logging.
        """
        return pd.DataFrame.from_dict(self.staking_ledger)

    def get_pool_token_supply_ledger(self, tkn):
        """Gets the pool token supply ledger.

        Args:
            tkn (str): Tickername of the token of interest.
        Returns:
            (pd.DataFrame): DataFrame of pool token supply ledger logging.
        """
        return pd.DataFrame.from_dict(self.pool_token_supply_ledger[f'bn{tkn}_ERC20_contract'])

    def update_spot_prices(self, tkn):
        """Updates the internal spot price as determined by the trading liquidity balances of the pool

        Args:
            tkn (str): The value of BNT to add to the vortex
        Returns:
            self
        """
        spot_rate = self.get_spot_rate(tkn)
        spot_prices = self.spot_prices
        spot_prices[tkn]['block_num'].append(self.block_num)
        spot_prices[tkn]['price_usd'].append(spot_rate)
        self.spot_prices = spot_prices
        # self.update_exchange_rates()

    def set_whitelisted_tokens(self, whitelisted_tokens, bootstrap_tokens=True):
        """Check if the spot rate is outside of the EMA tolerance. No changes are made to the pool depth if outside limits.

        Args:
            whitelisted_tokens (list): The tickername of the token.
            bootstrap_tokens (bool): If true, automatically initializes all whitelisted tokens and adds them to the bootstrapped_tokens list.
        Returns:
            bnTKN_value (int or float or decimal): value of a single bnTKN pool token.
        """
        self.whitelisted_tokens = whitelisted_tokens
        if bootstrap_tokens:
            self.init_pool(self.whitelisted_tokens)

    def init_pool(self, tkns):
        """Initializes a new pool in the respective ledgers but does not perform the DAOmsig initialization which allows trading.

        Args:
            tkns (list): List of tickernames of the tokens to be initialized.
        Returns:
            self
        """
        for tkn in tkns:
            self.vault_ledger[tkn] = [0]
            self.pool_token_supply_ledger[f"bn{tkn}_ERC20_contract"] = {'block_num': [0], 'supply': [0]}
            self.staking_ledger[tkn] = [0]
            self.external_protection_wallet_ledger[tkn] = [0]

    def validate_type(self, val):
        """Validates input data types using pydantic type setting. See utils/schema.py for details

        Args:
            val (int or float or decimal): The numerical value to be type checked

        Returns:
            val (int or float or decimal): the validated type-checked value
        """
        if self.is_solidity:
            val = Fxp(val, signed=True, n_int=256, n_frac=18)
        else:
            data_validator = FloatingPointGeneral
            input_params = dict(
                val=val
            )
            validated_params = data_validator(**input_params)
            val = validated_params.val
        return val

    def mint_bntkn(self, tkn, x=None, bnt=None):
        """Adds TKN to the available liquidity ledger.

        Args:
            tkn (str): The tickername of the token.
            x (int or float or decimal): The value of liquidity to add. (default=None)
            bnt (int or float or decimal): The value of bnt liquidity to add. (default=None)

        Returns:
            y (int): The number of pool tokens issued to the user.
        """

        pool_token_value = self.validate_type(self.get_pool_token_value(tkn))
        if bnt is None:
            x = self.validate_type(x)
            y = self.tokenomics.handle_multiplication(x, pool_token_value)
        else:
            y = self.validate_type(bnt)

        for contract in self.pool_token_supply_ledger:
            self.pool_token_supply_ledger[contract]['block_num'].append(self.block_num)
            if contract == f'bn{tkn}_ERC20_contract':
                new_val = self.tokenomics.handle_addition(self.pool_token_supply_ledger[contract]['supply'][-1], y)
                self.pool_token_supply_ledger[contract]['supply'].append(new_val)
            else:
                self.pool_token_supply_ledger[contract]['supply'].append(self.pool_token_supply_ledger[contract]['supply'][-1])
        return (y)

    def check_pool_shutdown(self, warning_only=True):
        """Checks if any whitelisted tokens meet the pool-shutdown criterea, and resets the DOAmsig state if yes.

        Returns:
            self
        """
        for TKN in self.whitelisted_tokens:
            BNTperTKN = self.get_bnt_rate(TKN)
            try:
                if self.vault_ledger[TKN][-1] < 0 or self.available_liquidity_ledger[TKN][-1] < 0 or self.staking_ledger[TKN][-1] < 0 or self.external_protection_wallet_ledger[TKN][-1] < 0:
                    if not warning_only:
                        raise UserWarning(f'Error. {TKN} balance cannot be less than zero. {self.vault_ledger[TKN][-1]}')
            except:
                pass

            vault_tkn = self.validate_type(self.vault_ledger[TKN][-1])
            BNTperTKN = self.validate_type(BNTperTKN)
            vault_bnt = self.tokenomics.handle_multiplication(vault_tkn, BNTperTKN)
            if vault_bnt < self.min_liquidity_threshold and (TKN in self.dao_msig_initialized_pools):
                if self.verbose:
                    print(
                        f"WARNING POOL SHUTDOWN!!! \n",
                        f"warning_only={warning_only} \n",
                        f"pool={TKN} \n",
                        f"TKN Liquidity <= Minimum Pool Liquidity, if not warning_only then will reset pool to pre-DAOmsig state"
                    )

    def check_bootstrapped_tokens(self):
        """Checks if new tokens have been whitelisted and whether or not those token meet the min_liquidity_threshold,
        ensures token are added to the bootstrapped_tokens list if any whitelisted tokens meet this criterea

        Returns:
            self
        """

        bootstrapped_tokens = self.bootstrapped_tokens
        for tkn in self.whitelisted_tokens:
            if tkn != 'BNT':
                tkn_vault = self.validate_type(self.vault_ledger[tkn][-1])
                exchange_rate = self.validate_type(self.exchange_rates[tkn])
                tkn_val = self.tokenomics.handle_multiplication(tkn_vault, exchange_rate)
                if (tkn_val >= self.min_liquidity_threshold) & (tkn not in bootstrapped_tokens) & (tkn in self.dao_msig_initialized_pools):
                    bootstrapped_tokens.append(tkn)
        self.bootstrapped_tokens = bootstrapped_tokens

    def check_case(self,
                   is_surplus,
                   is_deficit,
                   satisfies_hlim,
                   satisfies_hmax,
                   reduce_trading_liquidity,
                   a, b, c, e, w):
        """Defines which BIP15 logical case applies to the current action.

        Args:
            is_surplus (bool): Whether the system is in a surplus state.
            is_deficit (bool): Whether the system is in a deficit state.
            satisfies_hlim (bool): Whether the system passes the hlim test.
            satisfies_hmax (bool): Whether the system passes the hmax test.
            reduce_trading_liquidity (bool): Whether the system needs to reduce the available trading liquidity.
            a (int or float or decimal): the BNT balance of the trading liquidity, as judged from the spot rate.
            b (int or float or decimal): the TKN balance of the trading liquidity, as judged from the spot rate.
            c (int or float or decimal): the difference between the TKN balance of the vault, and the TKN trading liquidity.
            e (int or float or decimal): the TKN balance of the staking ledger.
            w (int or float or decimal): the TKN balance of the external protection wallet.

        Returns:
            case (str): the human readable logical-case name
        """
        if is_surplus & (a == 0 and b == 0):
            case = 'bootstrap surplus (special case)'

        elif is_deficit & (a == 0 and b == 0):
            case = 'bootstrap deficit (special case)'

        elif is_surplus & (satisfies_hlim and satisfies_hmax) & ((b + c) > e):
            case = 'arbitrage surplus'

        elif is_surplus & (not satisfies_hlim or not satisfies_hmax) & (not reduce_trading_liquidity):
            case = 'default surplus'

        elif is_surplus & (not satisfies_hlim or not satisfies_hmax) & reduce_trading_liquidity:
            case = 'bootstrap surplus'

        elif is_deficit & (satisfies_hlim and satisfies_hmax):
            case = 'arbitrage deficit'

        elif is_deficit & (not satisfies_hlim or not satisfies_hmax) & (
                not reduce_trading_liquidity):
            case = 'default deficit'

        elif is_deficit & (not satisfies_hlim or not satisfies_hmax) & reduce_trading_liquidity:
            case = 'bootstrap deficit'

        return case

    def validate_input_types(self, tkn, x):
        """Validates input data types using pydantic type setting. See utils/schema.py for details

        Args:
            tkn (str): The tickername of the token.
            x (int or float or decimal): The value of liquidity to add. (default=None)

        Returns:
            a (int or float or decimal): the BNT balance of the trading liquidity, as judged from the spot rate.
            b (int or float or decimal): the TKN balance of the trading liquidity, as judged from the spot rate.
            c (int or float or decimal): the difference between the TKN balance of the vault, and the TKN trading liquidity.
            e (int or float or decimal): the TKN balance of the staking ledger.
            w (int or float or decimal): the TKN balance of the external protection wallet.
            m (float or decimal): the global system exit fee
            n (float or decimal): the per pool trading fee
            x (int or float or decimal): the TKN or BNT amount involved in the current action
        """
        a = self.available_liquidity_ledger[tkn]['BNT'][-1]
        b = self.available_liquidity_ledger[tkn][tkn][-1]
        e = self.staking_ledger[tkn][-1]
        staked_bnt = self.staking_ledger['BNT'][-1]
        bnbnt_supply = self.pool_token_supply_ledger['bnBNT_ERC20_contract']['supply'][-1]
        w = self.external_protection_wallet_ledger[tkn][-1]
        c = self.vault_ledger[tkn][-1] - b
        n = self.exit_fee
        m = self.pool_fees[tkn]
        data_validator = FixedPointUnstakeTKN if self.is_solidity else FloatingPointUnstakeTKN
        input_params = dict(
            a=a,
            b=b,
            e=e,
            w=w,
            c=c,
            n=n,
            m=m,
            x=x,
            staked_bnt=staked_bnt,
            bnbnt_supply=bnbnt_supply
        )
        self.validated_params = data_validator(**input_params)
        self.params_set = True
        return self.validated_params.a, self.validated_params.b, self.validated_params.c, self.validated_params.e, self.validated_params.m, self.validated_params.n, self.validated_params.x, self.validated_params.w, self.validated_params.staked_bnt, self.validated_params.bnbnt_supply

    def update_available_liquidity_ledger(self, tkn, bnt_trading_liquidity, tkn_trading_liquidity):
        """Updates available liquidity for swaps

        Args:
            tkn (str): The tickername of the token.
            bnt_trading_liquidity (int or float or decimal): The value of liquidity to add to bnt.
            tkn_trading_liquidity (int or float or decimal): The value of liquidity to add to tkn.

        Returns:
            self
        """
        self.available_liquidity_ledger[tkn]['BNT'].append(bnt_trading_liquidity)
        self.available_liquidity_ledger[tkn][tkn].append(tkn_trading_liquidity)
        self.available_liquidity_ledger[tkn]['funding_limit'].append(
            self.available_liquidity_ledger[tkn]['funding_limit'][-1])
        self.available_liquidity_ledger[tkn]['block_num'].append(
            self.available_liquidity_ledger[tkn]['block_num'][-1])
        for key in self.available_liquidity_ledger:
            if key != tkn:
                self.available_liquidity_ledger[key]['funding_limit'].append(
                    self.available_liquidity_ledger[key]['funding_limit'][-1])
                self.available_liquidity_ledger[key]['block_num'].append(
                    self.available_liquidity_ledger[key]['block_num'][-1])
                self.available_liquidity_ledger[key]['BNT'].append(self.available_liquidity_ledger[key]['BNT'][-1])
                self.available_liquidity_ledger[key][key].append(self.available_liquidity_ledger[key][key][-1])

    def update_ledger_balances(self, tkn, p, q, r, s, t, u, a, b, c, e, m, n, x, w, case, event_type='unstake_tkn'):
        """Updates the ledger balances for withdraw actions

        Args:
            tkn (str): The tickername of the token.
            x (int or float or decimal): The value of liquidity to add. (default=None)
            a (int or float or decimal): the BNT balance of the trading liquidity, as judged from the spot rate.
            b (int or float or decimal): the TKN balance of the trading liquidity, as judged from the spot rate.
            c (int or float or decimal): the difference between the TKN balance of the vault, and the TKN trading liquidity.
            e (int or float or decimal): the TKN balance of the staking ledger.
            w (int or float or decimal): the TKN balance of the external protection wallet.

        Returns:
            self
        """
        p = self.validate_type(p)
        r = self.validate_type(r)
        s = self.validate_type(s)
        x = self.validate_type(x)
        q = self.validate_type(q)
        u = self.validate_type(u)
        tkn_bnt_liquidity = self.available_liquidity_ledger[tkn]['BNT'][-1]
        tkn_bnt_liquidity = self.validate_type(tkn_bnt_liquidity)

        tkn_tkn_liquidity = self.available_liquidity_ledger[tkn][tkn][-1]
        tkn_tkn_liquidity = self.validate_type(tkn_tkn_liquidity)

        bnt_staking = self.staking_ledger['BNT'][-1]
        bnt_staking = self.validate_type(bnt_staking)

        tkn_staking = self.staking_ledger[tkn][-1]
        tkn_staking = self.validate_type(tkn_staking)

        tkn_vault = self.vault_ledger[tkn][-1]
        tkn_vault = self.validate_type(tkn_vault)

        tkn_external_protection = self.external_protection_wallet_ledger[tkn][-1]
        tkn_external_protection = self.validate_type(tkn_external_protection)

        if event_type == 'unstake_tkn':

            # handle surplus signs
            if (case != 'default surplus') & self.tokenomics.surplus:
                tknbnt = self.tokenomics.handle_subtraction(tkn_bnt_liquidity, p)
                tkntkn = self.tokenomics.handle_addition(tkn_tkn_liquidity, r)
                self.available_liquidity_ledger[tkn]['BNT'][-1] = tknbnt
                self.available_liquidity_ledger[tkn][tkn][-1] = tkntkn

            elif self.tokenomics.surplus:
                tknbnt = self.tokenomics.handle_subtraction(tkn_bnt_liquidity, p)
                tkntkn = self.tokenomics.handle_subtraction(tkn_tkn_liquidity, r)
                self.available_liquidity_ledger[tkn]['BNT'][-1] = tknbnt
                self.available_liquidity_ledger[tkn][tkn][-1] = tkntkn

            # handle deficit signs
            elif (self.tokenomics.deficit) & ('ep2' in case):
                tknbnt = self.tokenomics.handle_subtraction(tkn_bnt_liquidity, p)
                tkntkn = self.tokenomics.handle_subtraction(tkn_tkn_liquidity, r)
                self.available_liquidity_ledger[tkn]['BNT'][-1] = tknbnt
                self.available_liquidity_ledger[tkn][tkn][-1] = tkntkn

            elif self.tokenomics.deficit:
                tknbnt = self.tokenomics.handle_addition(tkn_bnt_liquidity, p)
                tkntkn = self.tokenomics.handle_subtraction(tkn_tkn_liquidity, r)
                self.available_liquidity_ledger[tkn]['BNT'][-1] = tknbnt
                self.available_liquidity_ledger[tkn][tkn][-1] = tkntkn

            staking_bnt = self.tokenomics.handle_subtraction(bnt_staking, q)
            self.staking_ledger['BNT'][-1] = staking_bnt

            staking_tkn = self.tokenomics.handle_subtraction(tkn_staking, x)
            self.staking_ledger[tkn][-1] = staking_tkn

            vault_tkn = self.tokenomics.handle_subtraction(tkn_vault, s)
            self.vault_ledger[tkn][-1] = vault_tkn

            self.mint_bntkn(tkn, bnt=t)

            external_protection_wallet_tkn = self.tokenomics.handle_subtraction(tkn_external_protection, u)
            self.external_protection_wallet_ledger[tkn][-1] = external_protection_wallet_tkn

        eq_case = self.tokenomics.reduce_trading_liquidity
        if self.tokenomics.surplus: eq = 'x(1-n) <= c'
        else: eq = 'x(1-n)(b+c)/e <= c'
        if self.tokenomics.satisfies_hlim and self.tokenomics.satisfies_hmax:
            eq_entry = ''
        else:
            eq_entry = f'{eq}:{eq_case}'
        self.describe_withdrawal = {
            'inputs': [
                f"a:{a}",
                f"b:{b}",
                f"c:{c}",
                f"e:{e}",
                f"m:{m}",
                f"n:{n}",
                f"x:{x}",
            ],
            'tests': [
                f'hlim:{self.tokenomics.hlim}',
                f'hmax:{self.tokenomics.hmax}',
                f'is_surplus:{self.tokenomics.surplus}',
                f'case={case}',
                f'satisfies_hlim:{self.tokenomics.satisfies_hlim}',
                f'satisfies_hmax:{self.tokenomics.satisfies_hmax}',
                eq_entry,
            ],
            'outputs': [
                f"p:{p}",
                f"q:{q}",
                f"r:{r}",
                f"s:{s}",
                f"t:{t}",
                f"u:{u}",
                '',
            ],
            'trading_liquidity': [
                f"BNT:{self.available_liquidity_ledger[tkn]['BNT'][-1]}",
                f"{tkn}:{self.available_liquidity_ledger[tkn][tkn][-1]}",
                '',
                '',
                '',
                '',
                '',
            ],
            'vault_ledger': [
                f"{tkn}:{self.vault_ledger[tkn][-1]}",
                '',
                '',
                '',
                '',
                '',
                '',
            ],
            'staking_ledger': [
                f"{tkn}:{self.staking_ledger[tkn][-1]}",
                '',
                '',
                '',
                '',
                '',
                '',
            ],
            'external_protection_ledger': [
                f"{tkn}:{self.external_protection_wallet_ledger[tkn][-1]}",
                '',
                '',
                '',
                '',
                '',
                '',
            ]
        }
        return self

    def describe(self, withdraw=False):
        """Outputs details of the system state, including ledgers & parameters, or the case of withdrawal, inputs, outputs, &etc.
        Args:
            return_dict (bool): If True, return dictionary of information about system state. Defaults to False.
        Returns:
            pd.DataFrame: DataFrame of system state
        """
        if withdraw:
            logger = self.describe_withdrawal
        else:
            # try:
            logger = {'trading_liquidity':[],
                      'vault_ledger': [],
                      'staking_ledger': [],
                      'pool_token_supply_ledger': [],
                      'vortex_ledger': []
                      }
            for tkn in self.available_liquidity_ledger:
                if tkn != 'BNT':
                    logger['trading_liquidity'].append(f"{tkn}:{self.available_liquidity_ledger[tkn][tkn][-1]} - BNT:{self.available_liquidity_ledger[tkn]['BNT'][-1]}")
            for tkn in self.available_liquidity_ledger:
                logger['vault_ledger'].append(
                    f"{tkn}:{self.vault_ledger[tkn][-1]}")
            for tkn in self.staking_ledger:
                if tkn != 'block_num':
                    logger['staking_ledger'].append(
                    f"{tkn}:{self.staking_ledger[tkn][-1]}")
            for tkn in self.pool_token_supply_ledger:
                logger['pool_token_supply_ledger'].append(
                    f"{tkn.replace('_ERC20_contract','')}:{self.pool_token_supply_ledger[tkn]['supply'][-1]}")

            logger['vortex_ledger'].append(f"Balance:{self.vortex_ledger['BNT'][-1]}")

            max_rows = max([len(logger['pool_token_supply_ledger']),
                            len(logger['staking_ledger']),
                            len(logger['vault_ledger']),
                            len(logger['trading_liquidity'])])

            for key in logger:
                for row in range(max_rows - len(logger[key])):
                    logger[key].append('')

            for ledger in logger:
                logger[ledger].sort()

        return pd.DataFrame(logger)



    ######################################
    # move everything below here to tokenomics
    ######################################


    def update_exchange_rates(self):
        exchange_rates = self.exchange_rates
        bnt_price = self.spot_prices['BNT']['price_usd'][-1]
        for tkn in self.spot_prices:
            tkn_price = self.spot_prices[tkn]['price_usd'][-1]
            exchange_rates[tkn] = self.tokenomics.handle_division(tkn_price, bnt_price)
        self.exchange_rates = exchange_rates

    def get_pool_token_value(self, tkn):
        """Get pool token value in bnTKN/TKN. If this is the first issuance, the pool token value is forced to 1.

        Args:
            x (int or float or decimal): The value of BNT to add to the vortex
        Returns:
            bnTKN_value (int or float or decimal): value of a single bnTKN pool token.
        """
        staked_amount = self.staking_ledger[tkn][-1]
        bnTKN_supply = self.pool_token_supply_ledger[f'bn{tkn}_ERC20_contract']['supply'][-1]
        if staked_amount > 0 and bnTKN_supply > 0:
            bnTKN_value = self.tokenomics.handle_division(bnTKN_supply, staked_amount)
        else:
            bnTKN_value = 1
        return bnTKN_value

    def get_spot_rate(self, tkn):
        """Gets the spot rate in units of BNT/TKN as determined by the trading liquidity balances of the pool

        Args:
            tkn (str): The value of BNT to add to the vortex
        Returns:
            spot_rate (int or float or decimal): spot rate in units of BNT/TKN
        """
        if tkn == 'BNT':
            spot_rate = self.exchange_rates[tkn]
        else:
            TKN_amt = self.available_liquidity_ledger[tkn][tkn][-1]
            BNT_amt = self.available_liquidity_ledger[tkn]['BNT'][-1]
            if TKN_amt > 0 and BNT_amt > 0:
                spot_rate = self.tokenomics.handle_division(BNT_amt, TKN_amt)
            else:
                spot_rate = self.exchange_rates[tkn]

        return spot_rate

    def get_bnt_rate(self, tkn) -> float:
        """Gets the rate in units of TKN/BNT as determined by the external price feed

        Args:
            tkn (str): The token tickername.
        Returns:
            bnt_rate (int or float or decimal): bnt rate in units of TKN/BNT
        """
        bnt_price = self.external_price_feed['BNT']['price_usd'][-1]
        tkn_price = self.external_price_feed[tkn]['price_usd'][-1]
        bnt_price = self.validate_type(bnt_price)
        tkn_price = self.validate_type(tkn_price)
        bnt_rate = self.tokenomics.handle_division(tkn_price, bnt_price)
        return bnt_rate

    def dao_msig_initialize_pools(self, force=False):
        """Command to initialize the pools in simulation of DAOmsig actions.

        Returns:
            self
        """
        dao_msig_initialized_pools = self.dao_msig_initialized_pools
        for TKN in self.whitelisted_tokens:
            BNTperTKN = self.get_bnt_rate(TKN)
            BNTperTKN = self.validate_type(BNTperTKN)

            tkn_tkn_liquidity = self.available_liquidity_ledger[TKN][TKN][-1]
            tkn_tkn_liquidity = self.validate_type(tkn_tkn_liquidity)

            tkn_bnt_liquidity = self.available_liquidity_ledger[TKN]['BNT'][-1]
            tkn_bnt_liquidity = self.validate_type(tkn_bnt_liquidity)

            tkn_vault = self.vault_ledger[TKN][-1]
            tkn_vault = self.validate_type(tkn_vault)

            bnt_vault = self.vault_ledger['BNT'][-1]
            bnt_vault = self.validate_type(bnt_vault)

            bnt_staking = self.staking_ledger['BNT'][-1]
            bnt_staking = self.validate_type(bnt_staking)

            bnbnt_pool = self.pool_token_supply_ledger[f"bnBNT_ERC20_contract"]["supply"][-1]
            bnbnt_pool = self.validate_type(bnbnt_pool)

            funding_limit = self.available_liquidity_ledger[TKN]['funding_limit'][-1]
            funding_limit = self.validate_type(funding_limit)

            tkn_vault_times_bntpertkn = self.tokenomics.handle_multiplication(tkn_vault, BNTperTKN)

            zero = self.validate_type(0)
            min_liquidity_threshold = self.validate_type(self.min_liquidity_threshold)

            if (tkn_tkn_liquidity == zero and tkn_bnt_liquidity == zero and tkn_vault_times_bntpertkn > min_liquidity_threshold and (TKN not in self.dao_msig_initialized_pools)) or force:

                self.available_liquidity_ledger[TKN]['block_num'].append(self.available_liquidity_ledger[TKN]['block_num'][-1])
                self.available_liquidity_ledger[TKN][TKN].append(self.tokenomics.handle_division(min_liquidity_threshold, BNTperTKN))
                self.available_liquidity_ledger[TKN]['BNT'].append(self.min_liquidity_threshold)

                self.vault_ledger['BNT'].append(self.tokenomics.handle_addition(bnt_vault, min_liquidity_threshold))
                self.staking_ledger['BNT'].append(self.tokenomics.handle_addition(bnt_staking, min_liquidity_threshold))
                self.pool_token_supply_ledger[f"bnBNT_ERC20_contract"]["supply"].append(self.tokenomics.handle_addition(bnbnt_pool, min_liquidity_threshold))

                self.update_ema(TKN)
                self.available_liquidity_ledger[TKN]['funding_limit'].append(self.tokenomics.handle_subtraction(funding_limit, min_liquidity_threshold))
                dao_msig_initialized_pools.append(TKN)

        self.dao_msig_initialized_pools = dao_msig_initialized_pools
        self.check_bootstrapped_tokens()

    def update_ema(self, tkn):
        """Updates the EMA (Exponential Moving Average) based on current spot rates.

        Args:
            tkn (str): The tickername of the token.
        Returns:
            self
        """
        alpha = self.validate_type(self.alpha)
        spot_rate = self.validate_type(self.get_spot_rate(tkn))
        current_ema = self.validate_type(self.ema[tkn]['ema'][-1])
        if tkn in self.ema:
            if ema[tkn]['block_num'][-1] < self.block_num:
                ema[tkn]['block_num'].append(self.block_num)
                new_ema = self.tokenomics.handle_ema(alpha, spot_rate, current_ema)
                ema[tkn]['ema'].append(new_ema)
        else:
            ema[tkn]['block_num'].append(self.block_num)
            ema[tkn]['ema'].append(self.exchange_rates[tkn])
        self.ema = ema

    def is_within_ema_tolerance(self, tkn, lower_limit=.99, upper_limit=1.01):
        """Check if the spot rate is outside of the EMA tolerance. No changes are made to the pool depth if outside limits.

        Args:
            tkn (str): The tickername of the token.
        Returns:
            bnTKN_value (int or float or decimal): value of a single bnTKN pool token.
        """
        spot_rate = self.get_spot_rate(tkn)
        ema = self.ema[tkn]['ema'][-1]
        lower_bound = self.tokenomics.handle_multiplication(lower_limit, ema)
        upper_bound = self.tokenomics.handle_multiplication(upper_limit, ema)
        result = lower_bound <= spot_rate <= upper_bound
        if self.verbose:
            print(
                f"spot_rate={spot_rate} \n",
                f"ema={ema} \n",
                f"EMA Test = {result}, ({lower_limit} * {ema}) <= {spot_rate} <= ({upper_limit} * {ema}), tkn={tkn}"
            )
        return result

    def add_tkn_to_vault(self, tkn, x):
        """Adds x tkn to the self.vault_ledger dictionary with the same block_num number.

        Args:
            tkn (str): The tickername of the token.
            x (int or float or decimal): The amount of tkn.
        Returns:
            self
        """
        for key in self.vault_ledger:
            if key == tkn:
                new_val = self.tokenomics.handle_addition(self.vault_ledger[key][-1], x)
                self.vault_ledger[key].append(new_val)
            else:
                self.vault_ledger[key].append(self.vault_ledger[key][-1])
            self.vault_ledger['block_num'][-1] = self.block_num

    def add_tkn_to_staking_ledger(self, tkn, x):
        """Adds x tkn to the self.staking_ledger dictionary with the same block_num number.

        Args:
            tkn (str): The tickername of the token.
            x (int or float or decimal): The amount of tkn.
        Returns:
            self
        """
        for key in self.staking_ledger:
            if key == tkn:
                new_val = self.tokenomics.handle_addition(self.staking_ledger[key][-1], x)
                self.staking_ledger[key].append(new_val)
            else:
                self.staking_ledger[key].append(self.staking_ledger[key][-1])
            self.staking_ledger['block_num'][-1] = self.block_num

    def add_tkn_to_vortex_ledger(self, x):
        """Adds TKN to the vortex ledger.

        Args:
            x (int or float or decimal): The value of BNT to add to the vortex.

        Returns:
            self
        """
        new_val = self.tokenomics.handle_addition(self.vortex_ledger['BNT'][-1], x)
        self.vortex_ledger['BNT'].append(new_val)
        self.vortex_ledger['block_num'].append(self.block_num)

    def add_tkn_to_pool_token_supply_ledger(self, tkn, x):
        self.pool_token_supply_ledger[tkn]['block_num'].append(self.block_num)
        for key in self.pool_token_supply_ledger:
            if key == tkn:
                new_val = self.tokenomics.handle_addition(self.pool_token_supply_ledger[tkn]['supply'][-1], x)
                self.pool_token_supply_ledger[tkn]['supply'].append(new_val)
            else:
                self.pool_token_supply_ledger[key]['supply'].append(self.pool_token_supply_ledger[key]['supply'][-1])

    def add_tkn_to_available_liquidity_ledger(self, tkn, x):
        """Adds TKN to the available liquidity ledger.

        Args:
            tkn (str): The tickername of the token.
            x (int or float or decimal): The value of liquidity to add.

        Returns:
            self
        """
        for key in self.available_liquidity_ledger:
            if key == tkn:

                a = self.available_liquidity_ledger[key]['BNT'][-1]
                b = self.available_liquidity_ledger[key][tkn][-1]
                c = self.tokenomics.handle_subtraction(self.vault_ledger[key][-1], b)
                spot_rate = self.get_spot_rate(tkn)
                funding_limit = self.available_liquidity_ledger[key]['funding_limit'][-1]

                print(f'a={a}, b={b}, c={c}, spot_rate={spot_rate}, funding_limit={funding_limit}')

                if (c >= b) & (a <= funding_limit):
                    print('case1')
                    new_tknbnt_liquidity = self.tokenomics.handle_multiplication(a, 2)
                    new_tkn_liquidity = self.tokenomics.handle_multiplication(b, 2)
                    new_funding_limit = self.tokenomics.handle_subtraction(funding_limit, a)

                    self.available_liquidity_ledger[key]['BNT'].append(new_tknbnt_liquidity)
                    self.available_liquidity_ledger[key][tkn].append(new_tkn_liquidity)
                    self.available_liquidity_ledger[key]['funding_limit'].append(new_funding_limit)

                elif (c >= b) & (a > funding_limit):
                    print('case2')
                    new_tknbnt_liquidity = self.tokenomics.handle_addition(a, funding_limit)
                    new_tkn_liquidity = self.tokenomics.handle_division(funding_limit, spot_rate) + b

                    self.available_liquidity_ledger[key]['BNT'].append(new_tknbnt_liquidity)
                    self.available_liquidity_ledger[key][tkn].append(new_tkn_liquidity)
                    self.available_liquidity_ledger[key]['funding_limit'].append(0)

                elif (c < b) & (a <= funding_limit):
                    print('case3')
                    b_plus_c = self.tokenomics.handle_addition(b, c)
                    new_tknbnt_liquidity = self.tokenomics.handle_multiplication(b_plus_c, spot_rate)
                    new_tkn_liquidity = b_plus_c
                    c_spot = self.tokenomics.handle_multiplication(c, spot_rate)
                    new_funding_limit = self.tokenomics.handle_subtraction(funding_limit, c_spot)

                    self.available_liquidity_ledger[key]['BNT'].append(new_tknbnt_liquidity)
                    self.available_liquidity_ledger[key][tkn].append(new_tkn_liquidity)
                    self.available_liquidity_ledger[key]['funding_limit'].append(new_funding_limit)

                else:
                    print('case4')
                    c_spot = self.tokenomics.handle_multiplication(c, spot_rate)
                    new_tknbnt_liquidity = self.tokenomics.handle_addition(a, c_spot)
                    new_tkn_liquidity = self.tokenomics.handle_addition(b, c)
                    new_funding_limit = self.tokenomics.handle_subtraction(funding_limit, c_spot)

                    self.available_liquidity_ledger[key]['BNT'].append(new_tknbnt_liquidity)
                    self.available_liquidity_ledger[key][tkn].append(new_tkn_liquidity)
                    self.available_liquidity_ledger[key]['funding_limit'].append(new_funding_limit)

                self.available_liquidity_ledger[key]['block_num'].append(self.block_num)
                final_liquidity = self.available_liquidity_ledger[key]['BNT'][-1]
                delta = self.tokenomics.handle_subtraction(final_liquidity, a)
                self.add_tkn_to_vault('BNT', delta)
                self.add_tkn_to_staking_ledger('BNT', delta)

                bnt = self.staking_ledger['BNT'][-1]
                bnt_supply = self.pool_token_supply_ledger[f"bnBNT_ERC20_contract"]["supply"][-1]
                if bnt_supply > 0 and bnt > 0:
                    bnt_bnbnt_rate = self.tokenomics.handle_division(bnt, bnt_supply)
                    update_amt = self.tokenomics.handle_division(delta, bnt_bnbnt_rate)
                    self.add_tkn_to_pool_token_supply_ledger("bnBNT_ERC20_contract", update_amt)

                if "bnBNT" not in self.protocol_agent.wallet:
                    self.protocol_agent.wallet["bnBNT"] = {'block_num': [0], "bnBNT": [0]}

                new_val = self.tokenomics.handle_addition(self.protocol_agent.wallet["bnBNT"]["bnBNT"][-1], delta)
                self.protocol_agent.wallet["bnBNT"]["bnBNT"].append(new_val)
                self.protocol_agent.wallet["bnBNT"]['block_num'].append(self.block_num)

            else:
                self.available_liquidity_ledger[key][key].append(self.available_liquidity_ledger[key][key][-1])
                self.available_liquidity_ledger[key]['BNT'].append(self.available_liquidity_ledger[key]['BNT'][-1])
                self.available_liquidity_ledger[key]['block_num'].append(self.block_num)
                self.available_liquidity_ledger[key]['funding_limit'].append(self.available_liquidity_ledger[key]['funding_limit'][-1])

