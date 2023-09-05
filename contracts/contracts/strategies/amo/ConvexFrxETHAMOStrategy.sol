// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title Convex Automated Market Maker (AMO) Strategy
 * @notice AMO strategy for the Curve OETH/frxETH pool
 * @author Origin Protocol Inc
 */
import { IERC20 } from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

import { BaseConvexAMOStrategy } from "./BaseConvexAMOStrategy.sol";

contract ConvexFrxETHAMOStrategy is BaseConvexAMOStrategy {
    constructor(
        BaseStrategyConfig memory _baseConfig,
        AMOConfig memory _amoConfig,
        ConvexConfig memory _convexConfig
    ) BaseConvexAMOStrategy(_baseConfig, _amoConfig, _convexConfig) {}

    /***************************************
        Vault to Pool Asset Conversions
    ****************************************/

    /// @dev frxETH is the Vault asset and the Curve pool asset so
    /// nothing to except return the vault asset amount
    function _toPoolAsset(address, uint256 assets)
        internal
        pure
        override
        returns (uint256 poolAssets)
    {
        poolAssets = assets;
    }

    function _calcPoolAsset(address, uint256 vaultAssetAmount)
        internal
        pure
        override
        returns (uint256 poolAssetAmount)
    {
        poolAssetAmount = vaultAssetAmount;
    }

    /// @dev frxETH is the Vault asset and the pool asset so return the frxETH amount
    /// @param poolAssetAmount Amount of frxETH to convert to OETH
    function _toOTokens(uint256 poolAssetAmount)
        internal
        pure
        override
        returns (uint256 oethAmount)
    {
        // TODO - does this need to be converted to OETH amount using the Oracle?
        oethAmount = poolAssetAmount;
    }

    /***************************************
                Curve Pool Deposits
    ****************************************/

    /// @dev Adds frxETH and/or OETH to the Curve pool
    /// @param amounts The amount of Curve pool assets and OTokens to add to the pool
    function _addLiquidityToPool(
        uint256[2] memory amounts,
        uint256 minMintAmount
    ) internal override returns (uint256 lpDeposited) {
        lpDeposited = curvePool.add_liquidity(amounts, minMintAmount);
    }

    /***************************************
            Curve Pool Withdrawals
    ****************************************/

    /// @dev transfers the specified frxETH amount to the recipient
    function _withdrawAsset(
        address,
        uint256 vaultAssetAmount,
        address _recipient
    ) internal override {
        // Transfer the frxETH to the Vault
        asset.transfer(_recipient, vaultAssetAmount);

        emit Withdrawal(address(asset), address(lpToken), vaultAssetAmount);
    }

    /// @dev transfers the frxETH balance of this strategy contract to the recipient
    function _withdrawAllAsset(address _recipient) internal override {
        uint256 vaultAssets = asset.balanceOf(address(this));

        _withdrawAsset(address(asset), vaultAssets, _recipient);
    }

    /***************************************
                Asset Balance
    ****************************************/

    /**
     * @notice Get the total asset value held in the platform
     * @param _asset      Address of the asset
     * @return balance    Total value of the asset in the platform
     */
    function checkBalance(address _asset)
        public
        view
        override
        returns (uint256 balance)
    {
        require(_asset == address(asset), "Unsupported asset");

        // TODO - check for tokens in this strategy?
        uint256 lpTokens = cvxRewardStaker.balanceOf(address(this));
        if (lpTokens > 0) {
            balance += (lpTokens * curvePool.get_virtual_price()) / 1e18;
        }
    }

    /***************************************
                    Approvals
    ****************************************/

    /**
     * @dev Since we are unwrapping WETH before depositing it to Curve
     *      there is no need to to set an approval for WETH on the Curve
     *      pool
     * @param _asset Address of the asset
     * @param _pToken Address of the Curve LP token
     */
    // solhint-disable-next-line no-unused-vars
    function _abstractSetPToken(address _asset, address _pToken)
        internal
        override
    {}

    function _approveBase() internal override {
        // Approve Curve pool for frxETH and OETH (required for adding liquidity)
        // slither-disable-next-line unused-return
        oToken.approve(platformAddress, type(uint256).max);
        // slither-disable-next-line unused-return
        asset.approve(platformAddress, type(uint256).max);

        // Approve Convex deposit contract to transfer Curve pool LP tokens
        // This is needed for deposits if Curve pool LP tokens into the Convex rewards pool
        // slither-disable-next-line unused-return
        lpToken.approve(cvxDepositorAddress, type(uint256).max);
    }
}
