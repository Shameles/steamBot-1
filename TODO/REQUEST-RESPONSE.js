// Unknown
new Ajax.Request( 'http://steamcommunity.com/market/removelisting/' + listingid, {
	method: 'post',
	parameters: {
		sessionid: g_sessionID
	},
	onSuccess: function( transport ) { RemoveListingDialog.OnSuccess( transport ); },
	onFailure: function( transport ) { RemoveListingDialog.OnFailure( transport ); }
} );

// Cancelling a buy order
new Ajax.Request( 'http://steamcommunity.com/market/cancelbuyorder/', {
	method: 'post',
	parameters: {
		sessionid: g_sessionID,
		buy_orderid: this.m_llBuyOrderID
	},
	onSuccess: function( transport ) { CancelMarketBuyOrderDialog.OnSuccess( transport ); },
	onFailure: function( transport ) { CancelMarketBuyOrderDialog.OnFailure( transport ); }
} );

// Creating a buy order
// Request example: sessionid=11ea671dc3c52f6123b96609&currency=3&appid=730&market_hash_name=Chroma+2+Case&price_total=15&quantity=1
// Response example: {"success":1,"buy_orderid":"270235744"}
$J.ajax( {
	url: 'https://steamcommunity.com/market/createbuyorder/',
	type: 'POST',
	data: {
		sessionid: g_sessionID,
		currency: g_rgWalletInfo['wallet_currency'],
		appid: this.m_unAppId, // ITEM?
		market_hash_name: this.m_strMarketHashName,
		price_total: price_total,
		quantity: quantity
	},
	crossDomain: true,
	xhrFields: { withCredentials: true }
} ).done( function ( data ) {
	CreateBuyOrderDialog.OnCreateBuyOrderComplete( { responseJSON: data } );
} ).fail( function( jqxhr ) {
	// jquery doesn't parse json on fail
	var data = $J.parseJSON( jqxhr.responseText );
	CreateBuyOrderDialog.OnCreateBuyOrderComplete( { responseJSON: data } );
} );

// Buy order status
// Request example: http://steamcommunity.com/market/getbuyorderstatus/?sessionid=21ea671dc3c59f6123d90609&buy_orderid=277246355
// Response example: {"success":1,"active":1,"purchased":0,"quantity":"1","quantity_remaining":"1","purchases":[]}
$J.ajax( {
	url: 'http://steamcommunity.com/market/getbuyorderstatus/',
	type: 'GET',
	data: {
		sessionid: g_sessionID,
		buy_orderid: buy_orderid
	}
} ).done( function ( data ) {
	CreateBuyOrderDialog.OnPollForBuyOrderCompletionSuccess( buy_orderid, { responseJSON: data } );
} ).fail( function( jqxhr ) {
	CreateBuyOrderDialog.BuyOrderPlaced();
} );

// List all your buy orders (?)
$J.ajax( {
	url: 'https://steamcommunity.com/market/buylisting/' + listingid,
	type: 'POST',
	data: {
		sessionid: g_sessionID,
		currency: g_rgWalletInfo['wallet_currency'],
		subtotal: this.m_nSubtotal,
		fee: this.m_nFeeAmount,
		total: this.m_nTotal,
		quantity: 1
	},
	crossDomain: true,
	xhrFields: { withCredentials: true }
} ).done( function ( data ) {
	BuyItemDialog.OnSuccess( { responseJSON: data } );
} ).fail( function( jqxhr ) {
	// jquery doesn't parse json on fail
	var data = $J.parseJSON( jqxhr.responseText );
	BuyItemDialog.OnFailure( { responseJSON: data } );
} );

// Recent purchases and sales
new Ajax.Request( 'http://steamcommunity.com/market/recent', {
	method: 'get',
	parameters: {
		country: g_strCountryCode,
		language: g_strLanguage,
		currency: typeof( g_rgWalletInfo ) != 'undefined' ? g_rgWalletInfo['wallet_currency'] : 1			//time: g_rgRecents[type]['time'],
		//listing: g_rgRecents[type]['listing']
	},
	onSuccess: function( transport ) {
		if ( transport.responseJSON )
		{
			var response = transport.responseJSON;

			if ( response.assets.length != 0 )
			{
				g_rgRecents[type]['time'] = response.last_time;
				g_rgRecents[type]['listing'] = response.last_listing;

				elRows.update( g_htmlSellListingsTableHeader + response.results_html );

				MergeWithAssetArray( response.assets );
				MergeWithListingInfoArray( response.listinginfo );
				MergeWithAppDataArray( response.app_data );
				eval( response.hovers );
			}
		}
	},
	onComplete: function() { g_bBusyLoadingMore = false; }
});

// Shows your market listings
new Ajax.Request( 'http://steamcommunity.com/market/mylistings', {
	method: 'get',
	parameters: {
	},
	onSuccess: function( transport ) {
		if ( transport.responseJSON )
		{
			var response = transport.responseJSON;

			elMyMarketListings.innerHTML = response.results_html;
			$('my_market_activelistings_number').update( response.num_active_listings );

			MergeWithAssetArray( response.assets );
			eval( response.hovers );
		}
	},
	onComplete: function() { g_bBusyLoadingMyMarketListings = false; }
});

// Shows your market history
new Ajax.Request( 'http://steamcommunity.com/market/myhistory', {
	method: 'get',
	parameters: {
	},
	onSuccess: function( transport ) {
		if ( transport.responseJSON )
		{
			var response = transport.responseJSON;

			elMyHistoryContents.innerHTML = response.results_html;

			MergeWithAssetArray( response.assets );
			eval( response.hovers );

			g_oMyHistory = new CAjaxPagingControls(
					{
						query: '',
						total_count: response.total_count,
						pagesize: response.pagesize,
						prefix: 'tabContentsMyMarketHistory',
						class_prefix: 'market'
					}, 'http://steamcommunity.com/market/myhistory/'
			);

			g_oMyHistory.SetResponseHandler( function( response ) {
				MergeWithAssetArray( response.assets );
				eval( response.hovers );
			});
		}
	},
	onComplete: function() { g_bBusyLoadingMarketHistory = false; }
});

// Shows popular items
$J.ajax( {
	url: 'http://steamcommunity.com/market/popular',
	type: 'GET',
	data: {
		country: g_strCountryCode,
		language: g_strLanguage,
		currency: typeof( g_rgWalletInfo ) != 'undefined' ? g_rgWalletInfo['wallet_currency'] : 1,
		count: g_nResultCount
	}
} )...

// Shows the supply and demand of the item requested
$J.ajax( {
	url: 'http://steamcommunity.com/market/itemordershistogram',
	type: 'GET',
	data: {
		country: g_strCountryCode,
		language: g_strLanguage,
		currency: typeof( g_rgWalletInfo ) != 'undefined' && g_rgWalletInfo['wallet_currency'] != 0 ? g_rgWalletInfo['wallet_currency'] : 1,
		item_nameid: item_nameid
	}
} )...

// Shows the latest buyers and sellers for the item requested
$J.ajax( {
	url: 'http://steamcommunity.com/market/itemordersactivity',
	type: 'GET',
	data: {
		country: g_strCountryCode,
		language: g_strLanguage,
		currency: typeof( g_rgWalletInfo ) != 'undefined' && g_rgWalletInfo['wallet_currency'] != 0 ? g_rgWalletInfo['wallet_currency'] : 1,
		item_nameid: this.m_llItemNameID
	}
} )...

// Shows the pricehistory of a specified item
new Ajax.Request( 'http://steamcommunity.com/market/pricehistory/', {
		method: 'get',
		parameters: {
			appid: this.m_item.appid,
			market_hash_name: GetMarketHashName( this.m_item )
		},
		onSuccess: function( transport ) { SellItemDialog.OnPriceHistorySuccess( transport ); },
		onFailure: function( transport ) { SellItemDialog.OnPriceHistoryFailure( transport ); }
} );

// Shows the priceoverview of a specific item
new Ajax.Request( 'http://steamcommunity.com/market/priceoverview/', {
		method: 'get',
		parameters: {
			country: g_strCountryCode,
			currency: typeof( g_rgWalletInfo ) != 'undefined' ? g_rgWalletInfo['wallet_currency'] : 1,
			appid: item.appid,
			market_hash_name: strMarketName
		},
		onSuccess: function( transport ) {
			if ( transport.responseJSON && transport.responseJSON.success )
			{
				var strInfo = '';
				if ( transport.responseJSON.lowest_price )
				{
					strInfo += 'Vanaf: ' + transport.responseJSON.lowest_price + '<br>'
				}
				else
				{
					strInfo += 'There are no listings currently available for this item.' + '<br>';
				}

				if ( transport.responseJSON.volume )
				{
					var strVolume = '%1$s sold in the last 24 hours';
					strVolume = strVolume.replace( '%1$s', transport.responseJSON.volume );
					//strInfo += 'Median price: ' + transport.responseJSON.median_price + '<br>';
					strInfo += 'Volume: ' + strVolume + '<br>';
				}

				elPriceInfoContent.update( strInfo );
			}
		},
		onFailure: function( transport ) { elPriceInfo.hide(); }
} );

// Selling an item
// Request example: sessionid=31da671dc3c57f6123h90609&appid=440&contextid=2&assetid=1117952592&amount=1&price=58 (PRICE IS WHAT YOU RECEIVE)
// Response example: [] (not yet known, having problems sending these)
Javascript code unknown. Help is appreciated.



