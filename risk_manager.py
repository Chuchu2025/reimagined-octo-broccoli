"""
Trading Risk Manager Module

This module provides risk management functionality for trading operations,
including validation of trade sizes, position limits, and daily loss limits.
"""


class RiskLimit:
    """Represents risk limit configuration for trading."""
    
    def __init__(self, max_trade_size=10000, max_position_size=50000, 
                 daily_loss_limit=5000, max_open_positions=10):
        """
        Initialize risk limits.
        
        Args:
            max_trade_size: Maximum size for a single trade
            max_position_size: Maximum total position size
            daily_loss_limit: Maximum allowed daily loss
            max_open_positions: Maximum number of open positions
            
        Raises:
            ValueError: If any parameter is not positive
        """
        if max_trade_size <= 0:
            raise ValueError("max_trade_size must be positive")
        if max_position_size <= 0:
            raise ValueError("max_position_size must be positive")
        if daily_loss_limit <= 0:
            raise ValueError("daily_loss_limit must be positive")
        if max_open_positions <= 0:
            raise ValueError("max_open_positions must be positive")
            
        self.max_trade_size = max_trade_size
        self.max_position_size = max_position_size
        self.daily_loss_limit = daily_loss_limit
        self.max_open_positions = max_open_positions


class RiskManager:
    """Manages trading risk limits and validates trades."""
    
    def __init__(self, risk_limit=None):
        """
        Initialize the risk manager.
        
        Args:
            risk_limit: RiskLimit object with configured limits
        """
        self.risk_limit = risk_limit or RiskLimit()
        self.current_position_size = 0
        self.daily_loss = 0
        self.open_positions = 0
    
    def validate_trade(self, trade_size):
        """
        Validate if a trade can be executed based on risk limits.
        
        Args:
            trade_size: Size of the proposed trade
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if trade_size <= 0:
            return False, "Trade size must be positive"
        
        if trade_size > self.risk_limit.max_trade_size:
            return False, f"Trade size {trade_size} exceeds maximum allowed {self.risk_limit.max_trade_size}"
        
        if self.current_position_size + trade_size > self.risk_limit.max_position_size:
            return False, f"Trade would exceed maximum position size of {self.risk_limit.max_position_size}"
        
        if self.open_positions >= self.risk_limit.max_open_positions:
            return False, f"Maximum open positions ({self.risk_limit.max_open_positions}) reached"
        
        if self.daily_loss >= self.risk_limit.daily_loss_limit:
            return False, f"Daily loss limit of {self.risk_limit.daily_loss_limit} reached"
        
        return True, "Trade approved"
    
    def execute_trade(self, trade_size):
        """
        Execute a trade after validation.
        
        Args:
            trade_size: Size of the trade to execute
            
        Returns:
            bool: True if trade was executed, False otherwise
        """
        is_valid, message = self.validate_trade(trade_size)
        
        if is_valid:
            self.current_position_size += trade_size
            self.open_positions += 1
            return True
        
        return False
    
    def close_position(self, position_size, profit_loss):
        """
        Close a position and update risk metrics.
        
        Args:
            position_size: Size of the position being closed
            profit_loss: Profit (positive) or loss (negative) from the position
            
        Raises:
            ValueError: If position_size is negative or exceeds current position size
        """
        if position_size < 0:
            raise ValueError("position_size cannot be negative")
        if position_size > self.current_position_size:
            raise ValueError(f"position_size {position_size} exceeds current position size {self.current_position_size}")
            
        self.current_position_size -= position_size
        self.open_positions = max(0, self.open_positions - 1)
        
        if profit_loss < 0:
            self.daily_loss += abs(profit_loss)
    
    def reset_daily_limits(self):
        """Reset daily counters (should be called at start of each trading day)."""
        self.daily_loss = 0
    
    def get_risk_status(self):
        """
        Get current risk status.
        
        Returns:
            dict: Current risk metrics
        """
        # Calculate utilization percentages, handling potential division by zero
        # (though RiskLimit validation should prevent zero values)
        position_util = (self.current_position_size / self.risk_limit.max_position_size * 100) if self.risk_limit.max_position_size > 0 else 0
        loss_util = (self.daily_loss / self.risk_limit.daily_loss_limit * 100) if self.risk_limit.daily_loss_limit > 0 else 0
        
        return {
            'current_position_size': self.current_position_size,
            'max_position_size': self.risk_limit.max_position_size,
            'position_utilization': f"{position_util:.1f}%",
            'daily_loss': self.daily_loss,
            'daily_loss_limit': self.risk_limit.daily_loss_limit,
            'loss_limit_utilization': f"{loss_util:.1f}%",
            'open_positions': self.open_positions,
            'max_open_positions': self.risk_limit.max_open_positions
        }
