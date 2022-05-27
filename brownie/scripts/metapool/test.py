from metastrategy import *
harvest_all_strategies()
vault_core.rebase(OPTS)

# do a lot of mints/redeems on the strategy.
# OUSD vs 3CVR minted for metapool is 50%/50% result: 
# balanced pool - vault & OUSD balances go up for 1 mio mainly because of redeem fees. 
#                 caller is down 630k on stablecoins. 277k OUSD that has been minted for
#                 strategy "stays in the wild" Metapool continues to be relatively balanced (0.5mio diff)
#                 Average user gained 1.2% of OUSD balance increase
# 3CRV pool tilt- vault & OUSD balances go up for 11.2 mio. 10.4 OUSD that has been minted by strategy
#                 caller is down 630k on stablecoins. 277k OUSD that has been minted for
#                 strategy "stays in the wild" Metapool continues to be relatively balanced (0.5mio diff)
#                 Average user gained 1.1% of OUSD balance increase
# OUSD pool tilt- vault & OUSD balances go down for 2.4 mio. 3.2 OUSD has been burned for strategy
#                 caller is down 672k on stablecoins.Metapool continues to be relatively balanced (0.5mio diff)
#                 Average user gained 1.3% of OUSD balance increase
# NOTE: users gaining OUSD is mainly because of redeem fees
#
#
# OUSD vs 3CVR minted for metapool is 66%/33% result (have multiplied threePoolLpDollarValue in ConvexMetaStrat
# by 2 to run this test):
# balanced pool - nothing special happens comparing to 50%/50% test, `me` account is down 600k
# 3CRV pool tilt- nothing special happens comparing to 50%/50% test, `me` account is down 490k
# OUSD pool tilt- nothing special happens comparing to 50%/50% test, `me` account is down 640k
# importantly in all cases the vault and OUSD total supply are ok and have not diverged
with TemporaryFork():
    # Option 1
    balance_metapool()
    # Option 2
    # tiltMetapoolTo3CRV()
    # Option 3
    # tiltMetapoolToOUSD(5*1e6*1e18)
    with AccountOUSDBalance(OPTS):
        with SupplyChanges(OPTS):
            with ObserveMeBalances(OPTS):
                with MetapoolBalances(OPTS):
                    with Crv3Balances(OPTS):
                        for x in range(30):
                            mint(10e6)
                            withdrawAllFromMeta()
                            redeem(10e6)
                        show_vault_holdings()
                        balance_metapool()



# tilt pools between the mints and redeems
# OUSD vs 3CVR minted for metapool is 50%/50% result: 
# balanced pool  - vault & OUSD balances go up for 2 mio mainly mainly because of extra 1.67 mio OUSD minted
#                  for strategy. 'me' account is down 300k. General user balance goes up by 0.6%. 
# 3CRV pool tilt - vault & OUSD balances go up for 24 mio mainly mainly because of extra 23.6 mio OUSD minted
#                  for strategy. 'me' account is down 320k. General user balance goes up by 0.58%. 
# OUSD pool tilt - some transactions fail but overall vault & OUSD are up by 0.7 mio. `me` account is at a loss
#                  of 350k. General user balance goes up by 0.67%. 
# NOTE: users gaining OUSD is mainly because of redeem fees
#
#
# OUSD vs 3CVR minted for metapool is 66%/33% result (have multiplied threePoolLpDollarValue in ConvexMetaStrat
# by 2 to run this test):
# balanced pool - nothing special happens comparing to 50%/50% test, `me` account is down 188k
# 3CRV pool tilt- nothing special happens comparing to 50%/50% test, `me` account is down 190k
# OUSD pool tilt- nothing special happens comparing to 50%/50% test, `me` account is down 400k
# importantly in all cases the vault and OUSD total supply are ok and have not diverged
with TemporaryFork():
    balance_metapool()
    with AccountOUSDBalance(OPTS):
        with SupplyChanges(OPTS):
            with ObserveMeBalances(OPTS):
                with MetapoolBalances(OPTS):
                    with Crv3Balances(OPTS):
                        for x in range(15):
                            mint(10e6)
                            # Option 1
                            balance_metapool()
                            # Option 2
                            # tiltMetapoolTo3CRV(5*1e6*1e18)
                            # Option 3
                            # tiltMetapoolToOUSD(5*1e6*1e18)
                            withdrawAllFromMeta()
                            redeem(10e6)
                            balance_metapool()
                        show_vault_holdings()


with TemporaryFork():
    with ObserveMeBalances(OPTS):
        usdt.approve(threepool_swap.address, int(1e50), OPTS)
        threepool_swap.exchange(2,1,200*1e12, 0, OPTS)


