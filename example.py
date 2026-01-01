"""
Example usage of the Trading Risk Manager
"""

from risk_manager import RiskLimit, RiskManager


def main():
    # Create custom risk limits
    limits = RiskLimit(
        max_trade_size=5000,
        max_position_size=20000,
        daily_loss_limit=3000,
        max_open_positions=5
    )
    
    # Initialize risk manager
    manager = RiskManager(limits)
    
    print("=== Trading Risk Manager Demo ===\n")
    
    # Attempt several trades
    trades = [2000, 3000, 4000, 6000, 1000]
    
    for i, trade_size in enumerate(trades, 1):
        print(f"Trade #{i}: Attempting to trade ${trade_size}")
        is_valid, message = manager.validate_trade(trade_size)
        
        if is_valid:
            manager.execute_trade(trade_size)
            print(f"  ✓ {message}")
        else:
            print(f"  ✗ REJECTED: {message}")
        
        # Show current status
        status = manager.get_risk_status()
        print(f"  Position: ${status['current_position_size']}/{status['max_position_size']} "
              f"({status['position_utilization']})")
        print(f"  Open positions: {status['open_positions']}/{status['max_open_positions']}\n")
    
    # Close a position with loss
    print("Closing position #1 with $500 loss")
    manager.close_position(2000, -500)
    
    status = manager.get_risk_status()
    print(f"Daily loss: ${status['daily_loss']}/{status['daily_loss_limit']} "
          f"({status['loss_limit_utilization']})\n")
    
    # Show final status
    print("=== Final Risk Status ===")
    final_status = manager.get_risk_status()
    for key, value in final_status.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
