# Ethereum Transaction Script
The ethereum transaction script performs rudimentary operations related to transaction executions on the Ethereum Blockchain (mainnet or testnets)

## Commands
The following sections detail the operations provided by this script

### Estimate
The `estimate` command is used to provide a point-in-time estimate the total cost (in Gwei) that a transaction between two accounts will take to execute

**flags**
- --amount - The amount (in Gwei) to transfer between accounts
- --from-addr - The address to be deducted the value specified with `--amount`
- --to-addr - The address to be sent the value specified with `--amount`
