from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class User(AbstractUser):
    username = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    dob = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    zip = models.CharField(max_length=5, blank=True, null=True)


class AccessToken(models.Model):
    username = models.CharField(max_length=150, blank=True, null=True)
    token = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} {self.token}"


class Log(models.Model):
    source = models.CharField(max_length=100, blank=True, null=True)
    ip_address = models.CharField(max_length=30, blank=True, null=True)
    log_level = models.CharField(max_length=20, blank=True, null=True)
    timestamp = models.CharField(max_length=40, blank=True, null=True)
    filename = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.source} {self.ip_address}] ({self.timestamp}) {self.message}"


class Signal_Table(models.Model):
    type = models.CharField(max_length=150, blank=True, null=True)
    strategy_id = models.CharField(max_length=150, blank=True, null=True)
    symbol = models.CharField(max_length=150, blank=True, null=True)
    exchange = models.CharField(max_length=150, blank=True, null=True)
    asset_type = models.CharField(max_length=150, blank=True, null=True)
    log_time = models.CharField(max_length=150, blank=True, null=True)
    signal_type = models.CharField(max_length=50, blank=True, null=True)  # ENTRY, EXIT
    signal_price = models.FloatField(max_length=50, blank=True, null=True)
    order_type = models.CharField(max_length=50, blank=True, null=True)  # MKT, LMT
    signal_uid = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.strategy_id}_{self.exchange}_{self.asset_type}_{self.symbol}_" \
               f"{self.log_time}_{self.signal_type}_{self.order_type}"


class PairSignal_Table(models.Model):
    type = models.CharField(max_length=150, blank=True, null=True)
    strategy_id = models.CharField(max_length=150, blank=True, null=True)
    long_info = models.CharField(max_length=150, blank=True, null=True)
    short_info = models.CharField(max_length=150, blank=True, null=True)
    log_time = models.CharField(max_length=150, blank=True, null=True)
    signal_type = models.CharField(max_length=50, blank=True, null=True)  # ENTRY, EXIT
    long_cur_price = models.FloatField(max_length=50, blank=True, null=True)
    short_cur_price = models.FloatField(max_length=50, blank=True, null=True)
    order_type = models.CharField(max_length=50, blank=True, null=True)  # MKT, LMT
    signal_uid = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.strategy_id}_{self.long_info}_{self.short_info}_" \
               f"{self.log_time}_{self.signal_type}_{self.order_type}"


class Order_Table(models.Model):
    type = models.CharField(max_length=150, blank=True, null=True)
    strategy_id = models.CharField(max_length=150, blank=True, null=True)
    exchange = models.CharField(max_length=150, blank=True, null=True)  # binance, bybit
    source = models.CharField(max_length=150, blank=True, null=True)
    asset_type = models.CharField(max_length=150, blank=True, null=True)  # usdt, coinm, spot, margin
    symbol = models.CharField(max_length=150, blank=True, null=True)
    order_type = models.CharField(max_length=150, blank=True, null=True)  # MKT, LMT
    quantity = models.FloatField(max_length=150, blank=True, null=True)
    price = models.FloatField(max_length=150, blank=True, null=True)
    side = models.CharField(max_length=150, blank=True, null=True)  # BUY, SELL
    direction = models.CharField(max_length=150, blank=True, null=True)  # ENTRY, EXIT
    leverage_size = models.FloatField(max_length=150, blank=True, null=True)
    invest_amount = models.FloatField(max_length=150, blank=True, null=True)
    margin_type = models.CharField(max_length=150, blank=True, null=True)
    est_fill_cost = models.FloatField(max_length=150, blank=True, null=True)
    log_time = models.CharField(max_length=150, blank=True, null=True)
    status = models.CharField(max_length=150, blank=True, null=True)  # Exec 에서 바로 status 수정하기도하고 SuccessEvent 받고 수정하기도하고 -> Exec는 루프둘면서 Status 별 행동 취해주면됨!
    matcher = models.CharField(max_length=150, blank=True, null=True)
    signal_uid = models.CharField(max_length=150, blank=True, null=True)
    order_uid = models.CharField(max_length=150, blank=True, null=True)
    api_order_uid = models.CharField(max_length=150, blank=True, null=True)
    remaining_quantity = models.FloatField(max_length=150, blank=True, null=True)
    paired = models.CharField(max_length=10, blank=True, null=True)
    repay_needed = models.CharField(max_length=10, blank=True, null=True)

    leverage_confirmed = models.CharField(max_length=10, blank=True, null=True) # True, False
    margin_type_confirmed = models.CharField(max_length=10, blank=True, null=True) # True, False
    transfer_confirmed = models.CharField(max_length=10, blank=True, null=True) # True, False
    order_confirmed = models.CharField(max_length=10, blank=True, null=True) # True, False
    repay_confirmed = models.CharField(max_length=10, blank=True, null=True) # True, False

    def __str__(self):
        return f"{self.exchange}_{self.asset_type}_{self.symbol}_{self.side}_{self.quantity}"


class Fill_Table(models.Model):
    type = models.CharField(max_length=150, blank=True, null=True)
    strategy_id = models.CharField(max_length=150, blank=True, null=True)  # TODO :: Not used yet
    accno = models.CharField(max_length=150, blank=True, null=True)  # TODO :: Not used yet
    exchange = models.CharField(max_length=150, blank=True, null=True)  # binance, bybit
    source = models.CharField(max_length=150, blank=True, null=True)
    asset_type = models.CharField(max_length=150, blank=True, null=True)  # usdt, coinm, spot, margin
    log_time = models.CharField(max_length=150, blank=True, null=True)
    symbol = models.CharField(max_length=150, blank=True, null=True)
    filled_quantity = models.FloatField(max_length=150, blank=True, null=True)
    order_quantity = models.FloatField(max_length=150, blank=True, null=True)
    side = models.CharField(max_length=150, blank=True, null=True)  # BUY, SELL
    fill_cost = models.FloatField(max_length=150, blank=True, null=True)
    est_fill_cost = models.FloatField(max_length=150, blank=True, null=True)
    api_order_uid = models.CharField(max_length=150, blank=True, null=True)
    order_uid = models.CharField(max_length=150, blank=True, null=True)
    signal_uid = models.CharField(max_length=150, blank=True, null=True)  # Order 매칭될때 받아오기!
    matcher = models.CharField(max_length=150, blank=True, null=True)
    direction = models.CharField(max_length=150, blank=True, null=True)  # Order 매칭될때 받아오기!
    commission = models.FloatField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"{self.exchange}_{self.asset_type}_{self.symbol}_" \
               f"{self.side}_{self.order_quantity}_{self.filled_quantity}"