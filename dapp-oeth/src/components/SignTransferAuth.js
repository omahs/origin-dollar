import React, { useState } from 'react'
import { useStoreState } from 'pullstate'
import { fbt } from 'fbt-runtime'
import { ethers } from 'ethers'
import ContractStore from 'stores/ContractStore'
import GetOUSD from 'components/GetOUSD'
import { assetRootPath } from 'utils/image'
import { useAccount, useSigner } from 'wagmi'

const SignTransferAuth = ({}) => {
  const { address: account, isConnected: active } = useAccount()
  const { data: signer } = useSigner()
  const [dstAddress, setDstAddress] = useState('')
  const [sig, setSig] = useState(null)
  const [error, setError] = useState(null)
  const { ognStaking } = useStoreState(ContractStore, (s) => {
    if (s.contracts) {
      return s.contracts
    }
    return {}
  })

  return (
    <>
      <div>
        <div className="content-holder flex-grow d-flex flex-column shadow-div">
          {active && (
            <div>
              {' '}
              on {ognStaking.address} Transfer stakes from {account} to:
              <form
                onSubmit={async (e) => {
                  e.preventDefault()

                  if (!dstAddress || !dstAddress.length) {
                    setError('Please enter a destination address')
                    return
                  }

                  const { utils } = ethers

                  const s = await signer.signMessage(
                    utils.arrayify(
                      utils.solidityPack(
                        ['string', 'address', 'address', 'address'],
                        ['tran', ognStaking.address, account, dstAddress]
                      )
                    )
                  )
                  const sp = utils.splitSignature(s)

                  setSig(JSON.stringify({ r: sp.r, s: sp.s, v: sp.v }))
                }}
              >
                <input
                  type="text"
                  onChange={(e) => {
                    e.preventDefault()
                    setDstAddress(e.target.value)
                  }}
                  required
                  value={dstAddress}
                  placeholder="Destination Address"
                  className="form-control mb-sm-0"
                />
                <button
                  type="submit"
                  className="d-flex align-items-center justify-content-center"
                >
                  Sign Transfer
                </button>
              </form>
              {sig && (
                <div style={{ overflowWrap: 'anywhere' }}>signature: {sig}</div>
              )}
            </div>
          )}
          {!active && (
            <div className="empty-placeholder d-flex flex-column align-items-center justify-content-start">
              <img src={assetRootPath('/images/wallet-icons.svg')} />
              <div className="header-text">
                {fbt('No wallet connected', 'Disconnected dapp message')}
              </div>
              <div className="subtext">
                {fbt(
                  'Please connect an Ethereum wallet',
                  'Disconnected dapp subtext'
                )}
              </div>
              <GetOUSD primary connect trackSource="Dapp widget body" />
            </div>
          )}
        </div>
      </div>
      <style jsx>{`
        .content-holder {
          border-radius: 10px;
          background-color: #ffffff;
          max-width: 716px;
          min-width: 630px;
        }

        .shadow-div {
        }

        .empty-placeholder {
          min-height: 470px;
          height: 100%;
          padding: 70px;
          border-radius: 0 0 10px 10px;
          border-top: solid 1px #141519;
          background-color: #1e1f25;
        }

        .header-text {
          font-size: 22px;
          line-height: 0.86;
          text-align: center;
          color: black;
          margin-top: 23px;
          margin-bottom: 10px;
        }

        .subtext {
          font-size: 14px;
          line-height: 1.36;
          text-align: center;
          color: #828699;
          margin-bottom: 50px;
        }

        @media (max-width: 799px) {
          div {
            width: 100%;
            min-width: 100%;
            max-width: 100%;
          }

          .content-holder {
            max-width: 100%;
            min-width: 100%;
          }
        }
      `}</style>
    </>
  )
}

export default SignTransferAuth
