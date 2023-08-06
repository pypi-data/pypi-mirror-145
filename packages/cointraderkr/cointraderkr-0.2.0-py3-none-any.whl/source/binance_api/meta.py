BINANCE_WS_FMT_MAPPER = {
    'outboundAccountPosition': {
        'e': 'event_type',
        'E': 'event_time',
        'u': 'last_account_update',
        'B': 'balance_array',
        'a': 'asset',
        'f': 'free',
        'l': 'locked'
    },
    'balanceUpdate': {
        'e': 'event_type',
        'E': 'event_time',
        'a': 'asset',
        'd': 'balance_delta',
        'T': 'clear_time'
    },
    'executionReport': {
        'e': 'event_type',
        'E': 'event_time',
        's': 'symbol',
        'c': 'client_order_id',
        'S': 'side',
        'o': 'order_type',
        'f': 'time_in_force',
        'q': 'order_quantity',
        'p': 'order_price',
        'P': 'stop_price',
        'F': 'iceberg_quantity',
        'g': 'order_list_id',
        'C': 'original_client_order_id', # 주문 취소는 이 번호로
        'x': 'current_execution_type',
        'X': 'current_order_status',
        'r': 'order_reject_reason', # error code
        'i': 'order_id',
        'l': 'last_executed_quantity',
        'z': 'cumulative_filled_quantity',
        'L': 'last_executed_price',
        'n': 'commission_amount',
        'N': 'commission_asset',
        'T': 'transaction_time',
        't': 'trade_id',
        'I': 'ignore',
        'w': 'order_on_book',
        'm': 'trade_is_maker_side',
        'M': 'ignore_2',
        'O': 'order_creation_time',
        'Z': 'cumulative_quote_asset_transacted_quantity',
        'Y': 'last_quote_asset_transacted_quantity', # last price * last quantity
        'Q': 'quote_order_qty'
    },
    # OCO order response
    'listStatus': {
        'e': 'event_type',
        'E': 'event_time',
        's': 'symbol',
        'g': 'order_list_id',
        'c': 'contingency_type',
        'l': 'list_status_type',
        'L': 'list_order_status',
        'r': 'list_reject_reason',
        'C': 'list_client_order_id',
        'T': 'transaction_time'
    }
}

# trade
BINANCE_SPOT_AGGTRADE = {
  "e": "Event_type",
  "E": "Event_time",
  "s": "Symbol",
  "a": "Aggregate_trade_ID",
  "p": "Price",
  "q": "Quantity",
  "f": "First_trade_ID",
  "l": "Last_trade_ID",
  "T": "Trade_time",
  "m": "Buyer_is_market_maker",
  "M": "Ignore"
}

BINANCE_FUT_AGGTRADE = {
  "e": "Event_type",
  "E": "Event_time",
  "s": "Symbol",
  "a": "Aggregate_trade_ID",
  "p": "Price",
  "q": "Quantity",
  "f": "First_trade_ID",
  "l": "Last_trade_ID",
  "T": "Trade_time",
  "m": "Buyer_is_market_maker"
}

BINANCE_COINM_FUT_AGGTRADE = {
  'e': 'Event_type',
  'E': 'Event_time',
  'a': 'Aggregate_trade_ID',
  's': 'Symbol',
  'p': 'Price',
  'q': 'Quantity',
  'f': 'First_trade_ID',
  'l': 'Last_trade_ID',
  'T': 'Trade_time',
  'm': 'Buyer_is_market_maker'
}

# order book
BINANCE_FUT_ORDER_BOOK20 = {
  "e": "Event_type",
  "E": "Event_time",
  "T": "Transaction_time",
  "s": "Symbol",
  "U": "U",
  "u": "u",
  "pu": "pu",
  "b": "bids",
  "a": "asks"
}