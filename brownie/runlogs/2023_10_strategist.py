# -------------------------------------
# Oct 03, 2023 - Swap USDT to USDC & DAI
# -------------------------------------
from collateralSwap import *

def main():
  txs = []
  with TemporaryFork():
    txs.append(vault_core.rebase({'from':STRATEGIST}))
    txs.append(vault_value_checker.takeSnapshot({'from':STRATEGIST}))

    txs.append(
      vault_admin.withdrawFromStrategy(
        MORPHO_AAVE_STRAT, 
        [USDT], 
        [(1_992_665 + 2_413_401) * 10**6], 
        {'from': STRATEGIST}
      )
    )

    txs.append(
      build_swap_tx(
        USDT,
        DAI,
        1_992_665 * 10**6,
        0.5,
        False,
        dry_run=False
      )
    )
    txs.append(
      build_swap_tx(
        USDT,
        USDC,
        2_413_401 * 10**6,
        0.5,
        False,
        dry_run=False
      )
    )

    vault_change = vault_core.totalValue() - vault_value_checker.snapshots(STRATEGIST)[0]
    supply_change = ousd.totalSupply() - vault_value_checker.snapshots(STRATEGIST)[1]
    profit = vault_change - supply_change
    txs.append(vault_value_checker.checkDelta(profit, (500 * 10**18), vault_change, (500 * 10**18), {'from': STRATEGIST}))

    txs.append(vault_core.allocate({'from': STRATEGIST}))

  print(to_gnosis_json(txs))

# -------------------------------------
# Oct 03, 2023 - Swap USDT to USDC
# -------------------------------------
from collateralSwap import *

def main():
  txs = []
  with TemporaryFork():
    txs.append(vault_core.rebase({'from':STRATEGIST}))
    txs.append(vault_value_checker.takeSnapshot({'from':STRATEGIST}))

    txs.append(
      vault_admin.withdrawFromStrategy(
        MORPHO_AAVE_STRAT, 
        [USDT], 
        [(2_413_401) * 10**6], 
        {'from': STRATEGIST}
      )
    )

    txs.append(
      build_swap_tx(
        USDT,
        USDC,
        2_413_401 * 10**6,
        0.5,
        False,
        dry_run=False
      )
    )

    vault_change = vault_core.totalValue() - vault_value_checker.snapshots(STRATEGIST)[0]
    supply_change = ousd.totalSupply() - vault_value_checker.snapshots(STRATEGIST)[1]
    profit = vault_change - supply_change
    txs.append(vault_value_checker.checkDelta(profit, (500 * 10**18), vault_change, (500 * 10**18), {'from': STRATEGIST}))

    txs.append(vault_core.allocate({'from': STRATEGIST}))

  print(to_gnosis_json(txs))

# -------------------------------------
# Oct 03, 2023 - OETH Allocation
# -------------------------------------
from world import *

def main():
  with TemporaryForkForReallocations() as txs:
    # Before
    txs.append(vault_oeth_core.rebase({'from': STRATEGIST}))
    txs.append(oeth_vault_value_checker.takeSnapshot({'from': STRATEGIST}))

    # Remove 2330.46 WETH from strategy
    txs.append(
      vault_oeth_admin.withdrawFromStrategy(
        OETH_CONVEX_OETH_ETH_STRAT, 
        [weth], 
        [2330.46 * 10**18],
        {'from': STRATEGIST}
      )
    )
    
    # Deposit 2971.64 WETH to FraxETHStrategy
    txs.append(
      vault_oeth_admin.depositToStrategy(
        FRAX_ETH_STRATEGY, 
        [weth], 
        [2971.64 * 10**18], 
        {'from': STRATEGIST}
      )
    )

    # After
    vault_change = vault_oeth_core.totalValue() - oeth_vault_value_checker.snapshots(STRATEGIST)[0]
    supply_change = oeth.totalSupply() - oeth_vault_value_checker.snapshots(STRATEGIST)[1]
    profit = vault_change - supply_change
    txs.append(oeth_vault_value_checker.checkDelta(profit, (0.1 * 10**18), vault_change, (0.1 * 10**18), {'from': STRATEGIST}))
    print("-----")
    print("Profit", "{:.6f}".format(profit / 10**18), profit)
    print("Vault Change", "{:.6f}".format(vault_change / 10**18), vault_change)
    print("-----")


# -------------------------------------
# Oct 03, 2023 - OETH Balancer rETH allocation
# -------------------------------------
from world import *

with TemporaryForkForReallocations() as txs:
  # Before
  txs.append(vault_oeth_core.rebase({'from': STRATEGIST}))
  txs.append(oeth_vault_value_checker.takeSnapshot({'from': STRATEGIST}))

  # Deposit 32 rETH to BalancerRethStrategy
  txs.append(
    vault_oeth_admin.depositToStrategy(
      BALANCER_RETH_STRATEGY, 
      [reth], 
      [32 * 10**18], 
      {'from': STRATEGIST}
    )
  )

  # After
  vault_change = vault_oeth_core.totalValue() - oeth_vault_value_checker.snapshots(STRATEGIST)[0]
  supply_change = oeth.totalSupply() - oeth_vault_value_checker.snapshots(STRATEGIST)[1]
  profit = vault_change - supply_change
  txs.append(oeth_vault_value_checker.checkDelta(profit, (0.1 * 10**18), vault_change, (0.1 * 10**18), {'from': STRATEGIST}))
  print("-----")
  print("Profit", "{:.6f}".format(profit / 10**18), profit)
  print("Vault Change", "{:.6f}".format(vault_change / 10**18), vault_change)
  print("-----")

# -------------------------------------
# Oct 03, 2023 - OETH Balancer rETH allocation
# -------------------------------------
from world import *

with TemporaryForkForReallocations() as txs:
  # Before
  txs.append(vault_oeth_core.rebase({'from': STRATEGIST}))
  txs.append(oeth_vault_value_checker.takeSnapshot({'from': STRATEGIST}))

  # Deposit 32 rETH to BalancerRethStrategy
  txs.append(
    vault_oeth_admin.depositToStrategy(
      BALANCER_RETH_STRATEGY, 
      [reth], 
      [32 * 10**18], 
      {'from': STRATEGIST}
    )
  )

  # After
  vault_change = vault_oeth_core.totalValue() - oeth_vault_value_checker.snapshots(STRATEGIST)[0]
  supply_change = oeth.totalSupply() - oeth_vault_value_checker.snapshots(STRATEGIST)[1]
  profit = vault_change - supply_change
  txs.append(oeth_vault_value_checker.checkDelta(profit, (0.1 * 10**18), vault_change, (0.1 * 10**18), {'from': STRATEGIST}))
  print("-----")
  print("Profit", "{:.6f}".format(profit / 10**18), profit)
  print("Vault Change", "{:.6f}".format(vault_change / 10**18), vault_change)
  print("-----")

# -------------------------------------
# Oct 05, 2023 - OETH Balancer rETH allocation
# -------------------------------------
from world import *

with TemporaryForkForReallocations() as txs:
  # Before
  txs.append(vault_oeth_core.rebase({'from': STRATEGIST}))
  txs.append(oeth_vault_value_checker.takeSnapshot({'from': STRATEGIST}))

  # Deposit 32 rETH to BalancerRethStrategy
  txs.append(
    vault_oeth_admin.depositToStrategy(
      BALANCER_RETH_STRATEGY, 
      [reth, weth], 
      [32 * 10**18, 36.57 * 10**18], 
      {'from': STRATEGIST}
    )
  )

  # After
  vault_change = vault_oeth_core.totalValue() - oeth_vault_value_checker.snapshots(STRATEGIST)[0]
  supply_change = oeth.totalSupply() - oeth_vault_value_checker.snapshots(STRATEGIST)[1]
  profit = vault_change - supply_change
  txs.append(oeth_vault_value_checker.checkDelta(profit, (0.1 * 10**18), vault_change, (0.1 * 10**18), {'from': STRATEGIST}))
  print("-----")
  print("Profit", "{:.6f}".format(profit / 10**18), profit)
  print("Vault Change", "{:.6f}".format(vault_change / 10**18), vault_change)
  print("-----")

# -------------------------------------
# Oct 09, 2023 - FraxETH allocation
# -------------------------------------
from world import *

with TemporaryForkForReallocations() as txs:
  # Before
  txs.append(vault_oeth_core.rebase({'from': STRATEGIST}))
  txs.append(oeth_vault_value_checker.takeSnapshot({'from': STRATEGIST}))

  # Remove 3356.52 WETH from strategy
  txs.append(
    vault_oeth_admin.withdrawFromStrategy(
      OETH_CONVEX_OETH_ETH_STRAT, 
      [weth], 
      [3356.52 * 10**18],
      {'from': STRATEGIST}
    )
  )
  
  # Deposit 3937.88 WETH to FraxETHStrategy
  txs.append(
    vault_oeth_admin.depositToStrategy(
      FRAX_ETH_STRATEGY, 
      [weth], 
      [3937.88 * 10**18], 
      {'from': STRATEGIST}
    )
  )

  # After
  vault_change = vault_oeth_core.totalValue() - oeth_vault_value_checker.snapshots(STRATEGIST)[0]
  supply_change = oeth.totalSupply() - oeth_vault_value_checker.snapshots(STRATEGIST)[1]
  profit = vault_change - supply_change
  txs.append(oeth_vault_value_checker.checkDelta(profit, (0.1 * 10**18), vault_change, (0.1 * 10**18), {'from': STRATEGIST}))
  print("-----")
  print("Profit", "{:.6f}".format(profit / 10**18), profit)
  print("Vault Change", "{:.6f}".format(vault_change / 10**18), vault_change)
  print("-----")

# -------------------------------------
# Oct 11, 2023 - OGV Buyback
# ------------------------------------
from buyback import *

def main():
  build_buyback_tx(max_dollars=10000, max_slippage=1)

# -------------------------------------
# Oct 11, 2023 - Buy CVX
# ------------------------------------
from convex import *

def main():
  build_cvx_buyback_tx(slippage=1)

# -------------------------------------
# Oct 11, 2023 - Lock CVX
# ------------------------------------
from convex import *

def main():
  lock_cvx()

# -------------------------------------
# Oct 16, 2023 - FraxETH allocation
# -------------------------------------
from world import *

with TemporaryForkForReallocations() as txs:
  # Before
  txs.append(vault_oeth_core.rebase({'from': STRATEGIST}))
  txs.append(oeth_vault_value_checker.takeSnapshot({'from': STRATEGIST}))

  # Deposit 725.71 WETH to FraxETHStrategy
  txs.append(
    vault_oeth_admin.depositToStrategy(
      FRAX_ETH_STRATEGY, 
      [weth], 
      [725.71 * 10**18], 
      {'from': STRATEGIST}
    )
  )

  # After
  vault_change = vault_oeth_core.totalValue() - oeth_vault_value_checker.snapshots(STRATEGIST)[0]
  supply_change = oeth.totalSupply() - oeth_vault_value_checker.snapshots(STRATEGIST)[1]
  profit = vault_change - supply_change
  txs.append(oeth_vault_value_checker.checkDelta(profit, (0.1 * 10**18), vault_change, (0.1 * 10**18), {'from': STRATEGIST}))
  print("-----")
  print("Profit", "{:.6f}".format(profit / 10**18), profit)
  print("Vault Change", "{:.6f}".format(vault_change / 10**18), vault_change)
  print("-----")
