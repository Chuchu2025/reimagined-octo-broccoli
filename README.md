# Trading Risk Management System

A Python-based trading risk management system that helps enforce risk limits on trading activities.

## Features

- **Trade Size Validation**: Ensures individual trades don't exceed maximum allowed size
- **Position Limit Management**: Tracks total position size across all open trades
- **Daily Loss Limits**: Prevents further trading when daily loss threshold is reached
- **Maximum Open Positions**: Limits the number of concurrent open positions
- **Risk Status Reporting**: Provides real-time risk metrics and utilization percentages

## Installation

No external dependencies required. Uses Python standard library only.

```bash
# Clone the repository
git clone https://github.com/Chuchu2025/reimagined-octo-broccoli.git
cd reimagined-octo-broccoli
```

## Usage

### Basic Example

```python
from risk_manager import RiskLimit, RiskManager

# Create custom risk limits
limits = RiskLimit(
    max_trade_size=5000,
    max_position_size=20000,
    daily_loss_limit=3000,
    max_open_positions=5
)

# Initialize risk manager
manager = RiskManager(limits)

# Validate and execute a trade
is_valid, message = manager.validate_trade(2000)
if is_valid:
    manager.execute_trade(2000)
    print("Trade executed successfully")
else:
    print(f"Trade rejected: {message}")

# Check risk status
status = manager.get_risk_status()
print(status)
```

### Running the Example

```bash
python example.py
```

## Configuration

Edit `config.py` to adjust default risk limits:

- `MAX_TRADE_SIZE`: Maximum size for a single trade
- `MAX_POSITION_SIZE`: Maximum total position size
- `DAILY_LOSS_LIMIT`: Maximum allowed daily loss
- `MAX_OPEN_POSITIONS`: Maximum number of open positions

## Testing

Run the test suite:

```bash
python -m unittest test_risk_manager.py
```

Or run with verbose output:

```bash
python -m unittest test_risk_manager.py -v
```

## API Reference

### RiskLimit

Configuration class for risk limits.

**Parameters:**
- `max_trade_size` (int): Maximum size for a single trade (default: 10000)
- `max_position_size` (int): Maximum total position size (default: 50000)
- `daily_loss_limit` (int): Maximum allowed daily loss (default: 5000)
- `max_open_positions` (int): Maximum number of open positions (default: 10)

### RiskManager

Main class for managing trading risk.

**Methods:**
- `validate_trade(trade_size)`: Validate if a trade can be executed
- `execute_trade(trade_size)`: Execute a trade after validation
- `close_position(position_size, profit_loss)`: Close a position and update metrics
- `reset_daily_limits()`: Reset daily counters (call at start of trading day)
- `get_risk_status()`: Get current risk metrics

## License

MIT License 
