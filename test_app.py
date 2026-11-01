import unittest
from streamlit.testing.v1 import AppTest

class TestSapTreasurySimulatorEnhanced(unittest.TestCase):
    def test_01_initial_load_and_branding(self):
        """Test initial load, header, and author attribution"""
        at = AppTest.from_file("app.py", default_timeout=30).run()
        self.assertEqual(len(at.exception), 0, f"Exceptions on startup: {at.exception}")
        self.assertTrue("prakush shende" in at.sidebar.markdown[0].value.lower())
        self.assertIn("current_scenario", at.session_state)
        self.assertIn("cfg_threshold", at.session_state)
        print("  [PASS] Test 1: App loaded cleanly with Prakush Shende branding.")

    def test_02_all_seven_scenarios(self):
        """Test all 7 business scenarios in the sidebar dropdown"""
        all_scenarios = [
            ("Scenario 1: Happy Path (Standard POBO EUR 125k)", "04", "ACCP"),
            ("Scenario 2: High-Value Flow ($1.5M USD Dual-Signoff)", "02", "Pending Approval"),
            ("Scenario 3: Bank Rejection & Auto-Rollback (pain.002 AC04)", "08", "RJCT"),
            ("Scenario 4: Insufficient Funds Exception (pain.002 AM04)", "08", "RJCT"),
            ("Scenario 5: Multilateral Intercompany Netting (Zero External Fee)", "04", "Zero External Bank Flow"),
            ("Scenario 6: Cross-Border FX Hedged Settlement (EUR -> JPY)", "04", "Settled via FX Deal"),
            ("Scenario 7: Bank Sanctions / AML Compliance Hold (pain.002 PDNG)", "07", "PDNG")
        ]
        
        for sc_name, exp_status, exp_resp in all_scenarios:
            at = AppTest.from_file("app.py", default_timeout=30).run()
            at.sidebar.selectbox[0].select(sc_name).run()
            self.assertEqual(len(at.exception), 0, f"Error in {sc_name}")
            self.assertIn(exp_status, at.session_state.batch_status)
            self.assertIn(exp_resp, at.session_state.bank_response)
            print(f"  [PASS] Test 2: Verified {sc_name}")

    def test_03_spro_configuration_sandbox(self):
        """Test SPRO Sandbox dynamic configuration slider and policy selector"""
        at = AppTest.from_file("app.py", default_timeout=30).run()
        at.slider[0].set_value(250000.0).run()
        self.assertEqual(len(at.exception), 0)
        self.assertEqual(at.session_state.cfg_threshold, 250000.0)
        print("  [PASS] Test 3: SPRO Configuration Sandbox dynamic threshold adjusted.")

    def test_04_payment_run_and_bcm_approval(self):
        """Test Payment execution and BCM approval button actions"""
        at = AppTest.from_file("app.py", default_timeout=30).run()
        # Find execute button
        for btn in at.button:
            if "Execute Payment Run" in btn.label:
                btn.click().run()
                break
        self.assertEqual(len(at.exception), 0)

        # Test Signer 1 approval
        for btn in at.button:
            if "Signer 1" in btn.label:
                btn.click().run()
                break
        self.assertEqual(len(at.exception), 0)
        print("  [PASS] Test 4: Payment execution and BCM approvals verified.")

    def test_05_xml_and_code_blocks(self):
        """Verify pain.001 XML generation and camt.053 electronic bank statement"""
        at = AppTest.from_file("app.py", default_timeout=30).run()
        code_blocks = [c.value for c in at.code]
        has_xml = any("<Document xmlns=\"urn:iso:std:iso:20022:tech:xsd:pain.001.001.03\"" in c for c in code_blocks)
        self.assertTrue(has_xml, "ISO 20022 pain.001 XML not found")
        has_camt = any("CAMT.053" in c for c in code_blocks)
        self.assertTrue(has_camt, "camt.053 statement code block not found")
        print("  [PASS] Test 5: ISO 20022 XML generation and camt.053 statement verified.")

if __name__ == "__main__":
    unittest.main()
