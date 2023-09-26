const { deploymentWithGovernanceProposal } = require("../utils/deploy");
const addresses = require("../utils/addresses");
const { balancer_rETH_WETH_PID } = require("../utils/constants");

const platformAddress = addresses.mainnet.rETH_WETH_BPT;

module.exports = deploymentWithGovernanceProposal(
  {
    deployName: "071_balancer_rETH_WETH",
    forceDeploy: false,
    //forceSkip: true,
    deployerIsProposer: true,
    //proposalId: ,
  },
  async ({ deployWithConfirmation, ethers, getTxOpts, withConfirmation }) => {
    const { deployerAddr } = await getNamedAccounts();
    const sDeployer = await ethers.provider.getSigner(deployerAddr);

    // Current contracts
    const cOETHVaultProxy = await ethers.getContract("OETHVaultProxy");
    const cOETHVaultAdmin = await ethers.getContractAt(
      "OETHVaultAdmin",
      cOETHVaultProxy.address
    );

    // Deployer Actions
    // ----------------

    // 1. Deploy new proxy for the Balancer strategy
    // New strategy will be living at a clean address
    const dOETHBalancerMetaPoolStrategyProxy = await deployWithConfirmation(
      "OETHBalancerMetaPoolrEthStrategyProxy"
    );
    const cOETHBalancerMetaPoolStrategyProxy = await ethers.getContractAt(
      "OETHBalancerMetaPoolrEthStrategyProxy",
      dOETHBalancerMetaPoolStrategyProxy.address
    );

    // 2. Deploy new Balancer strategy implementation
    const dOETHBalancerMetaPoolStrategyImpl = await deployWithConfirmation(
      "BalancerMetaPoolStrategy",
      [
        [platformAddress, cOETHVaultProxy.address],
        [
          addresses.mainnet.rETH,
          addresses.mainnet.stETH,
          addresses.mainnet.wstETH,
          addresses.mainnet.frxETH,
          addresses.mainnet.sfrxETH,
          addresses.mainnet.balancerVault, // Address of the Balancer vault
          balancer_rETH_WETH_PID, // Pool ID of the Balancer pool
        ],
        addresses.mainnet.rETH_WETH_AuraRewards, // Address of the Aura rewards contract
      ]
    );
    const cOETHBalancerMetaPoolStrategy = await ethers.getContractAt(
      "BalancerMetaPoolStrategy",
      dOETHBalancerMetaPoolStrategyProxy.address
    );

    const cOETHHarvesterProxy = await ethers.getContract("OETHHarvesterProxy");
    const cOETHHarvester = await ethers.getContractAt(
      "OETHHarvester",
      cOETHHarvesterProxy.address
    );

    // 3. Encode the init data
    // TODO change back
    const initFunction =
      "initialize(address[],address[],address[],uint256,uint256)";
    const initData = cOETHBalancerMetaPoolStrategy.interface.encodeFunctionData(
      initFunction,
      [
        [addresses.mainnet.BAL, addresses.mainnet.AURA],
        [addresses.mainnet.rETH, addresses.mainnet.WETH],
        [platformAddress, platformAddress],
        //TODO: delete this:
        2, // WeightedPoolExitKind.BPT_IN_FOR_EXACT_TOKENS_OUT
        1, // WeightedPoolExitKind.EXACT_BPT_IN_FOR_TOKENS_OUT
      ]
    );

    // 4. Init the proxy to point at the implementation
    // prettier-ignore
    await withConfirmation(
      cOETHBalancerMetaPoolStrategyProxy
        .connect(sDeployer)["initialize(address,address,bytes)"](
          dOETHBalancerMetaPoolStrategyImpl.address,
          addresses.mainnet.Timelock,
          initData,
          await getTxOpts()
        )
    );

    console.log(
      "Balancer strategy address:",
      dOETHBalancerMetaPoolStrategyProxy.address
    );

    // Governance Actions
    // ----------------
    return {
      name: "Deploy new Balancer MetaPool strategy",
      actions: [
        // 1. Add new strategy to the vault
        {
          contract: cOETHVaultAdmin,
          signature: "approveStrategy(address)",
          args: [cOETHBalancerMetaPoolStrategy.address],
        },
        // 2. Set supported strategy on Harvester
        {
          contract: cOETHHarvester,
          signature: "setSupportedStrategy(address,bool)",
          args: [cOETHBalancerMetaPoolStrategy.address, true],
        },
        // 3. Set harvester address
        {
          contract: cOETHBalancerMetaPoolStrategy,
          signature: "setHarvesterAddress(address)",
          args: [cOETHHarvesterProxy.address],
        },
      ],
    };
  }
);
