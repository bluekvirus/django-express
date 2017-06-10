;(function(app){

	app.setup({
		//navigate region for context
		navRegion: 'context',
		//setup layout
		layout: {
			split: ['4em:Header', '1:context'],
			bars: false
		},
		icings: {
			'default': {left:'72%', top:'4em', bottom: '0%', right: 0, 'overflow-y': 'auto', 'overflow-x': 'hidden'}
		},

		//view source
		viewSrcs: 'js', //set this to a folder path to enable view dynamic loading.
		//---------------------------------------------------------------------------------------------
		fullScreen: true, //this will put <body> to be full screen sized (window.innerHeight).
		//---------------------------------------------------------------------------------------------
		i18nTransFile: 'i18n.json', //can be {locale}.json
		i18nLocale: '', //if you really want to force the app to certain locale other than browser preference. (Still override-able by ?locale=.. in url)
		//---------------------------------------------------------------------------------------------
		//baseAjaxURI: '/api/v1', //modify this to fit your own backend apis. e.g index.php?q= or '/api'
		timeout: 5 * 60 * 1000 //general communication timeout (ms), e.g when using app.remote()
	});

	app.addInitializer(function(){
		app.global = app.global || {};
		if(!window.location.href.includes('#navigate')){
			window.location.href = '#navigate/Models/Models.Display';
			// window.location.href = '#navigate/Models/Models.Menu';
		}
	});
})(Application);
