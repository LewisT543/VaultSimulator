from unittest import TestCase
from pyvaultsim import AUTOBNBVault, Simulate

# Run tests in the terminal using python -m unittest discover

class AUTOBNBVaultTest(TestCase):
    def setup(self):
        pass

    def vault_has_balance(self):
        vault = AUTOBNBVault()
        balance = vault.balance
        self.assertGreater(balance, 0)

    def vault_has_defaults(self):
        vault = AUTOBNBVault()

        rewards = vault.rewards
        self.assertEqual(rewards, 0)

        elapsed_days = vault.elapsed_days
        self.assertEqual(elapsed_days, 0)

        usd_in = vault.usd_in
        self.assertEqual(usd_in, 0)
        
        fees_paid = vault.fees_paid
        self.assertEqual(fees_paid, 0)

        
