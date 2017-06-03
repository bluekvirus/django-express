/**
 * Sample VIEW script.
 *
 * @author Stagejs.CLI
 * @created Wed May 31 2017 15:45:20 GMT-0700 (PDT)
 */
;(function(app){

	app.view('Models.Fields', {

		template: '@view/models/fields.html',
		
		onReady: function(){
		},
		
		actions: {
		},

	});
	app.view('Models.Relation', {

		template: '@view/models/fields.html',
		
		onReady: function(){
			// this.$el.find('[data-toggle="tooltip"]').tooltip({
			// 	placement: 'right'
			// });
			this.$el.find('[data-toggle="tooltip"]').tooltip();
		},
		
		actions: {
		},

	});

})(Application);