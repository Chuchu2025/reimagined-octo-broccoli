"""
Unit tests for the Trading Risk Manager
"""

import unittest
from risk_manager import RiskLimit, RiskManager


class TestRiskLimit(unittest.TestCase):
    """Test RiskLimit configuration."""
    
    def test_default_limits(self):
        """Test default risk limit values."""
        limits = RiskLimit()
        self.assertEqual(limits.max_trade_size, 10000)
        self.assertEqual(limits.max_position_size, 50000)
        self.assertEqual(limits.daily_loss_limit, 5000)
        self.assertEqual(limits.max_open_positions, 10)
    
    def test_custom_limits(self):
        """Test custom risk limit values."""
        limits = RiskLimit(
            max_trade_size=5000,
            max_position_size=25000,
            daily_loss_limit=2500,
            max_open_positions=5
        )
        self.assertEqual(limits.max_trade_size, 5000)
        self.assertEqual(limits.max_position_size, 25000)
        self.assertEqual(limits.daily_loss_limit, 2500)
        self.assertEqual(limits.max_open_positions, 5)
    
    def test_invalid_limits(self):
        """Test that invalid risk limit values raise errors."""
        with self.assertRaises(ValueError):
            RiskLimit(max_trade_size=0)
        with self.assertRaises(ValueError):
            RiskLimit(max_position_size=-100)
        with self.assertRaises(ValueError):
            RiskLimit(daily_loss_limit=0)
        with self.assertRaises(ValueError):
            RiskLimit(max_open_positions=-1)


class TestRiskManager(unittest.TestCase):
    """Test RiskManager functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        limits = RiskLimit(
            max_trade_size=1000,
            max_position_size=5000,
            daily_loss_limit=500,
            max_open_positions=3
        )
        self.manager = RiskManager(limits)
    
    def test_validate_positive_trade_size(self):
        """Test that negative trade sizes are rejected."""
        is_valid, message = self.manager.validate_trade(-100)
        self.assertFalse(is_valid)
        self.assertIn("positive", message)
    
    def test_validate_trade_within_limits(self):
        """Test that valid trades are approved."""
        is_valid, message = self.manager.validate_trade(500)
        self.assertTrue(is_valid)
        self.assertEqual(message, "Trade approved")
    
    def test_validate_trade_exceeds_max_size(self):
        """Test that oversized trades are rejected."""
        is_valid, message = self.manager.validate_trade(1500)
        self.assertFalse(is_valid)
        self.assertIn("exceeds maximum allowed", message)
    
    def test_validate_trade_exceeds_position_limit(self):
        """Test that trades exceeding position limit are rejected."""
        # Directly set position size to near limit to test position limit check
        self.manager.current_position_size = 4500
        self.manager.open_positions = 2  # Under the limit of 3
        
        # Try to add 1000 which would exceed position limit of 5000
        is_valid, message = self.manager.validate_trade(1000)
        self.assertFalse(is_valid)
        self.assertIn("maximum position size", message)
    
    def test_validate_trade_exceeds_open_positions(self):
        """Test that max open positions limit is enforced."""
        self.manager.execute_trade(500)
        self.manager.execute_trade(500)
        self.manager.execute_trade(500)
        # Fourth trade should be rejected
        is_valid, message = self.manager.validate_trade(500)
        self.assertFalse(is_valid)
        self.assertIn("Maximum open positions", message)
    
    def test_execute_trade_success(self):
        """Test successful trade execution."""
        result = self.manager.execute_trade(500)
        self.assertTrue(result)
        self.assertEqual(self.manager.current_position_size, 500)
        self.assertEqual(self.manager.open_positions, 1)
    
    def test_execute_trade_failure(self):
        """Test failed trade execution."""
        result = self.manager.execute_trade(1500)  # Exceeds max trade size
        self.assertFalse(result)
        self.assertEqual(self.manager.current_position_size, 0)
        self.assertEqual(self.manager.open_positions, 0)
    
    def test_close_position(self):
        """Test closing a position."""
        self.manager.execute_trade(500)
        self.manager.close_position(500, 100)
        self.assertEqual(self.manager.current_position_size, 0)
        self.assertEqual(self.manager.open_positions, 0)
    
    def test_close_position_with_loss(self):
        """Test that losses are tracked correctly."""
        self.manager.execute_trade(500)
        self.manager.close_position(500, -200)
        self.assertEqual(self.manager.daily_loss, 200)
    
    def test_close_position_invalid_size(self):
        """Test that invalid position close sizes are rejected."""
        self.manager.execute_trade(500)
        # Try to close more than current position
        with self.assertRaises(ValueError):
            self.manager.close_position(600, 0)
        # Try to close negative size
        with self.assertRaises(ValueError):
            self.manager.close_position(-100, 0)
    
    def test_daily_loss_limit(self):
        """Test that daily loss limit prevents trades."""
        self.manager.execute_trade(500)
        self.manager.close_position(500, -500)
        # Should be at daily loss limit
        is_valid, message = self.manager.validate_trade(500)
        self.assertFalse(is_valid)
        self.assertIn("Daily loss limit", message)
    
    def test_reset_daily_limits(self):
        """Test resetting daily limits."""
        self.manager.daily_loss = 500
        self.manager.reset_daily_limits()
        self.assertEqual(self.manager.daily_loss, 0)
    
    def test_get_risk_status(self):
        """Test risk status reporting."""
        self.manager.execute_trade(500)
        status = self.manager.get_risk_status()
        
        self.assertEqual(status['current_position_size'], 500)
        self.assertEqual(status['max_position_size'], 5000)
        self.assertEqual(status['open_positions'], 1)
        self.assertEqual(status['max_open_positions'], 3)
        self.assertIn('position_utilization', status)
        self.assertIn('loss_limit_utilization', status)


if __name__ == '__main__':
    unittest.main()
