// How steam calculates the fee
// nAmount = input value
var publisherFee = typeof this.m_item.market_fee != 'undefined' ? this.m_item.market_fee : g_rgWalletInfo['wallet_publisher_fee_percent_default'];
var info = CalculateAmountToSendForDesiredReceivedAmount( nAmount, publisherFee );
$('market_sell_buyercurrency_input').value = v_currencyformat( info.amount, GetCurrencyCode( g_rgWalletInfo['wallet_currency'] ) );

this.RecalculateTotal( nAmount, quantity );

// On the HTML file the defaults of your wallet are defined
<script type="text/javascript">
// Example of data
var g_rgWalletInfo = {"wallet_currency":3,"wallet_country":"NL","wallet_fee":1,"wallet_fee_minimum":1,"wallet_fee_percent":"0.05","wallet_publisher_fee_percent_default":"0.10","wallet_fee_base":0,"wallet_balance":76,"wallet_delayed_balance":0,"wallet_max_balance":45000,"wallet_trade_max_balance":36000,"success":true,"rwgrsn":-2};

// This is the CalculateAmountToSendForDesirecReceivedAmount function
function CalculateAmountToSendForDesiredReceivedAmount( receivedAmount, publisherFee )
{
	if ( !g_rgWalletInfo['wallet_fee'] )
	{
		return receivedAmount;
	}

	publisherFee = ( typeof publisherFee == 'undefined' ) ? 0 : publisherFee;
	
	// For me this are the defaultStatus
	// ['wallet_fee_precent'] = 0.05
	// ['wallet_fee_minimum'] = 1 (cents)
	// ['wallet_fee_base'] = 0
	var nSteamFee = parseInt( Math.floor( Math.max( receivedAmount * parseFloat( g_rgWalletInfo['wallet_fee_percent'] ), g_rgWalletInfo['wallet_fee_minimum'] ) + parseInt( g_rgWalletInfo['wallet_fee_base'] ) ) );
	var nPublisherFee = parseInt( Math.floor( publisherFee > 0 ? Math.max( receivedAmount * publisherFee, 1 ) : 0 ) );
	var nAmountToSend = receivedAmount + nSteamFee + nPublisherFee;

	return {
		steam_fee: nSteamFee,
		publisher_fee: nPublisherFee,
		fees: nSteamFee + nPublisherFee,
		amount: parseInt( nAmountToSend )
	};
}

// Python version of this code needed. Tried it myself but got stuck on some things. PM me if you want to help.

