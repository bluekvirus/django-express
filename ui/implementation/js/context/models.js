/**
 * Sample CONTEXT script.
 *
 * @author Stagejs.CLI
 * @created Mon Aug 29 2016 12:51:43 GMT-0700 (PDT)
 */
;(function(app){
    app.page('Models', {
        template: [
            '<div style="height: 100%; width: 100%; display: flex; flex-flow: row; justify-content: flex-start; position: relative;">',
                '<div style="flex: 0 0 180px;" view="Models.MenuCt"></div>',
                '<div style="flex: 0 0 3px;background-color: #ddd;"></div>',
                '<div style="flex: 1 1 0px; display: flex; flex-flow: column; justify-content: flex-start;" class="body">',
                    // '<div style="flex: 0 0 38px;" view="BreadCrumbs"></div>',
                    // '<div style="flex: 0 0 1px;background-color: #ddd;"></div>',
                    '<div style="flex: 1 1 0;" region="panel"></div>',
                '</div>',
            '</div>',
        ],
        navRegion: 'panel',
        coop: ['show-model'],
        actions: {
            'remove-filter': function(){
                //appearance
                this.$el.find('.search-filter-placeholder').removeClass('hidden');
                this.$el.find('.search-filter-active').addClass('hidden');
                //metadata
                this.onSearch('');
            },
        },
        initialize: function(){
        },
        onNavigateTo: function(path){
        },
        onShowModel: function(path){
            // console.log(path);
            this.show('panel', 'Models.Display', {
                data: {
                    app: path
                }
            });
            app.curtain('default', false);
        }

    });
})(Application);
