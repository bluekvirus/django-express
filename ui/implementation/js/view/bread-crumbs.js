/**
 * Sample VIEW script.
 *
 * @author Stagejs.CLI
 * @created Thu Mar 02 2017 19:36:22 GMT-0800 (PST)
 */
;(function(app){

	app.view('BreadCrumbs', {

		template: '@view/bread-crumbs.html',
		//data: 'url', {} or [],
		coop: ['breadcrumbs-change'],
		//[editors]: {...},
		
		initialize: function(){},
		//onShow: function(){},
		//onDataRendered: function(){},
		onBreadcrumbsChange: function(bcs){
			this.set({bcs: bcs});
		},
		actions: {
		//	submit: function(){...},
		//	dosomething: function(){...},
		//	...
		},

	});

})(Application);