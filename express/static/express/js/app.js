;;(function(app){

	var _currentView = '';
	app.view('Header', {
		template: '@view/header.html',
		coop:['context-switched'],
		actions: {
			goto: function($el){
				var context = $el.data('context');
				if( context ){
					app.navigate(context);
				}
			},
			'load-cm': function(){
				var Cm = app.get('Cm');
				(new Cm()).overlay({
					class: 'overlay-cm',
					effect: false
				});
			}
		},
		onReady: function(){
			var that = this,
				flag = false;

			//initialize tooltip
			this.$el.find('[data-toggle="tooltip"]').tooltip();

		},
		onContextSwitched: function(ctx){
			_.defer(function(argument){
				this.$el.find('.active').removeClass('active');
				if(ctx === 'Models'){
					this.$el.find('[data-context="Models/Models.IndvsTable"]').addClass('active')
				}else{
					this.$el.find('[data-context="' + ctx + '"]').addClass('active');
				}
			}.bind(this));
		}
	});
})(Application);
;/**
 * Sample CONTEXT script.
 *
 * @author Stagejs.CLI
 * @created Mon Aug 29 2016 12:51:43 GMT-0700 (PDT)
 */
;(function(app){
    app.page('Models', {
        template: [
            '<div style="height: 100%; width: 100%; display: flex; flex-flow: row; justify-content: flex-start; position: relative;">',
                '<div style="flex: 0 0 220px;" view="Models.MenuCt"></div>',
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

;;(function(app){

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

;/**
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
;(function(app){

	app.context('Mockups', {
		
		className: 'wrapper-full container-fluid',
		template: '<div region="mockups"></div>',

		data: {
			mockups: [

				//breadcrumb
				{tpl: 'breadcrumb.html'},

				//navbars
				{tpl: 'nav-bar.html', className: 'navbar-default'},
				{tpl: 'nav-bar.html', className: 'navbar-inverse'},

				//boxes
				{tpl: 'boxes.html', onReady: function(){
					if(Modernizr.chrome){
						this.$el.find('[warning="chrome"]').removeClass('hidden');
					}
				}},

				//containers
				{tpl: 'containers.html'},			

				//buttons
				{tpl: 'buttons.html',},

				//typography
				{tpl: 'typography.html'},

				//indicators (alert, lable, badge and progress bar)
				{tpl: 'indicators.html'},

				//navigators
				{tpl: 'navs.html'},

				//tooltips/popovers & modal
				{tpl: 'dialogs.html'},

				//table
				{tpl: 'table.html'},

				//forms
				{tpl: 'forms.html'},

				//copyright of the mockup collections above
				{tpl: 'copyright.html'}

		]},

		onReady: function(){
			_.each(this.get('mockups'), function(m){
				/////////////////////////////////////////////////////////////////////////
				///Manually managed view life cycle..without this.show('region',...)..///
				/////////////////////////////////////////////////////////////////////////
				//1. create it
				var view = app.view({
					className: 'wrapper-full',
					template: '@mockups/' + m.tpl,
					onRender: function(){
						this.$el.find('> div').addClass(m.className);
					},
					onReady: function(){
						if(m.onReady) m.onReady.call(this);
					}
				}, true);
				//2. render and insert it into DOM
				this.getRegion('mockups').$el.append(view.render().el);
				//3. connect the view life-cycle event seq: --render--[[show]]--ready 
				view.triggerMethod('show'); 
				//4. tell the views to close themselves upon parent view close
				view.listenTo(this, 'close', function(){
					view.close();
				});
				//(ref: /lib+-/marionette/view.js, we refined the seq and added a ready e.)
			}, this);
		}

	});

})(Application);
;/**
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
;/**
 *
 * @author Andy Fan
 * @created Tue May 14 2017 17:33:43 GMT-0800 (PST)
 */
;
(function(app) {

    app.view('Models.Display', {
        template: '@view/models/display.html',
        svg: {
            topo: function(paper) {
                // console.log(this.cur);
                var that = this;
                app.remote({
                    url: '/express/models',
                    params: {
                        app: (that.cur || '')
                    }
                }).then(function(data) {
                    that.data = {};
                    that.data['raw'] = _.clone(data);
                    var indvSizes = [{
                        circle: 20,
                        text: 22,
                        charge: -1200,
                        distance: 120
                    }];

                    function getDimn(len) {
                        return indvSizes[0];
                    }
                    var dimn = getDimn(data.length);
                    var links = [];
                    _.each(data, function(v, k) {
                        _.each(v.relations, function(r, name) {
                            if (r.relation === 'one_to_one' || k === r.related_model) {
                                links.push({
                                    source: k,
                                    target: r.related_model,
                                    type: k === r.related_model ? 'selft_to_self' : r.relation,
                                    type: r.relation,
                                    order: k === r.related_model ? 0 : 1,
                                });
                            } else {
                                links.push({
                                    source: k,
                                    target: r.related_model,
                                    type: k === r.related_model ? 'selft_to_self' : r.relation,
                                    type: r.relation,
                                    // order: 1,
                                    order: k === r.related_model ? 0 : 1,
                                });
                            }
                        });
                    });
                    var nodes = {}, linkPaths = {}, nodePaths = {};

                    // Compute the distinct nodes from the links.
                    links.forEach(function(link) {
                        link.source = nodes[link.source] || (nodes[link.source] = {
                            name: link.source,
                            title: data[link.source].verbose_name + '(' + link.source + ')',
                            vname: data[link.source].verbose_name || _.last(link.source.split('.')),
                        });
                        link.target = nodes[link.target] || (nodes[link.target] = {
                            name: link.target,
                            title: data[link.target] ? data[link.target].verbose_name + '(' + link.target + ')' : link.target,
                            vname: data[link.target] ? data[link.target].verbose_name : _.last(link.target.split('.')),
                        });
                        if(linkPaths[link.target.name + link.source.name]){
                            // reverse link exist, modify reverse link attr
                            linkPaths[link.source.name + link.target.name] = {offset: {x: '0em', y: '1.5em'}, archOrder: 0};
                            linkPaths[link.target.name + link.source.name] = {offset: {x: '0em', y: '-1em'}, archOrder: 1};
                        }else{
                            linkPaths[link.source.name + link.target.name] = {offset: {x: '0em', y: '-1em'}, archOrder: 2};
                        }
                        if(!nodePaths[link.source.name]){
                            nodePaths[link.source.name] = {self: null, peers: [], degree: 0};
                        }
                        nodePaths[link.source.name].peers.push(link.target.name);
                        nodePaths[link.source.name].degree++;
                        if(!nodePaths[link.target.name]){
                            nodePaths[link.target.name] = {self: null, peers: [], degree: 0};
                        }
                        nodePaths[link.target.name].peers.push(link.source.name);
                        nodePaths[link.target.name].degree++;
                    });
                    if(links.length < 1){
                        _.each(data, function(v, k) {
                            nodes[k] = {
                                name: k,
                                title: v.verbose_name + '(' + k + ')',
                                vname: v.verbose_name || _.last(k.split('.')),
                            }
                        });
                    }
                    var width = paper.getSize().width,
                        height = paper.getSize().height;

                    // var force = d3.layout.force()
                    var force = d3.layout.force()
                        .nodes(d3.values(nodes))
                        .links(links)
                        .size([width, height])
                        .linkDistance(dimn.distance)
                        .charge(dimn.charge)
                        .on("tick", tick)
                        .start();

                    var svg = paper.d3
                        .attr("width", width)
                        .attr("height", height);

                    var refYs = {
                        "order0": -1.5,
                        "order1": 0,
                        "order2": 1.5
                    };

                    // Per-type markers, as they don't inherit styles.
                    svg.append("defs").selectAll("marker")
                        .data(['circle'])
                        .enter().append("marker")
                        .attr("id", function(d) {
                            return d;
                        })
                        .attr("viewBox", "0 -7 16 16")
                        .attr("refX", 0)
                        .attr("refY", 0)
                        .attr("markerWidth", 12)
                        .attr("markerHeight", 12)
                        .attr("orient", "auto")
                        .append("path")
                        .attr("d", function(d) {
                            return "M0,0A3,3 0 1,0 6,0 A3,3 0 1,0 0,0z";
                        })
                        .attr("fill", 'black');

                    var stroke_widths = {
                            "many_to_one": 2,
                            "one_to_one": 1,
                            "many_to_many": 4,
                        },
                        relationTitle = {
                            "many_to_one": 'm : 1',
                            "one_to_one": '1 : 1',
                            "many_to_many": 'm : m'
                        },
                        circleStroke = '#333';

                    var path = svg.append("g").selectAll("path")
                        .data(_.filter(force.links(), function(d, k){
                            return d.source.name !== d.target.name;
                        }))
                        .enter().append("path")
                        .attr("stroke-width", function(d) {
                            if(d.source.name === d.target.name){
                                return 1;
                            }
                            return stroke_widths[d.type];
                        })
                        .attr("class", function(d) {
                            return "link " + d.type;
                        })
                    .attr("marker-end", function(d) {
                        if(d.source.name === d.target.name){
                            return "url(#order" + d.order + ")"; 
                        }else{
                            return '';
                        }
                    });

                    var circle = svg.append("g").selectAll("circle")
                        .data(force.nodes())
                        .enter().append("circle")
                        .attr("r", dimn.circle)
                        .attr("stroke", circleStroke)
                        .on('click', function(d, i, j) {
                            circle.attr("stroke", circleStroke);
                            text.attr("stroke", 'none');
                            d3.select(this).attr('stroke', '#44B78B');
                            d3.event.stopPropagation();
                            if(!that.data['raw'][d.name]){
                                // app.curtain('default', false);
                                app.curtain('default', true, 'Models.Fields', {
                                    data: {
                                        mkey: d.name,
                                        items: [],
                                        hdr: {
                                            left: 'Field',
                                            right: 'Type'
                                        }
                                    }
                                });
                                return;
                            }
                            var dd = {};
                            _.each(that.data['raw'][d.name].fields, function(v, k){
                                dd[v.name.split('.').join('-')] = {
                                    first: {
                                        name: _.last(v.name.split('.')),
                                        full_name: v.name,
                                    },
                                    second: {
                                        name: v.type
                                    },
                                    // third: _.last(v.related_model.split('.')),
                                    third: {
                                        name: v.related_model
                                    },
                                };
                            });
                            app.curtain('default', true, 'Models.Fields', {
                                data: {
                                    mkey: d.name,
                                    items: dd,
                                    hdr: {
                                        left: 'Field',
                                        right: 'Type'
                                    }
                                }
                            });
                        }).call(force.drag);

                    _.each(force.nodes(), function(v, k){
                        if(nodePaths[v.name]){
                            nodePaths[v.name].self = v;
                        }else{
                        }
                    });

                    var p = _.filter(force.links(), function(d, k){
                            return d.source.name === d.target.name;
                        });

                    var path2 = svg.append("g").selectAll("path")
                        .data(p)
                        .enter().append("path")
                        .attr("stroke-width", function(d) {
                            if(d.source.name === d.target.name){
                                return 1;
                            }
                            return stroke_widths[d.type];
                        })
                        .attr("class", function(d) {
                            return "link " + d.type;
                        })
                        .attr("marker-end", function(d) {
                            if(d.source.name === d.target.name){
                                return "url(#circle)"; 
                            }else{
                                return '';
                            }
                        });

                    path[0] = _.union(path[0], path2[0]);

                    var r = dimn.circle * 3 / 4,
                    relationTitleMap = {
                        'one_to_one': {
                            left: 'One',
                            right: 'One'
                        },
                        'many_to_many': {
                            left: 'Many',
                            right: 'Many'
                        },
                        'many_to_one': {
                            left: 'Many',
                            right: 'One'
                        }
                    };

                    var text = svg.append("g").selectAll("text")
                        .data(_.union(force.nodes(), force.links()))
                        .enter().append("text")
                        .attr('id', function(d) {
                            if (d.source) {
                                return '';
                            } else {
                                return d.name.split('.').join('_');
                            }
                        })
                        .attr("class", function(d) {
                            if (d.source)
                                return 'relation ' + d.source.name + d.target.name;
                            else
                                return 'node';
                        })
                        .attr("x", function(d) {
                            if (d.source){
                                if(d.source.name !== d.target.name)
                                    return '0em';
                                else
                                    return -r/2;
                            }
                            else
                                return dimn.text;
                        })
                        .attr("y", function(d) {
                            if (d.source){
                                if(d.source.name !== d.target.name)
                                    return linkPaths[d.source.name + d.target.name].offset.y;
                                else
                                    return 0;
                            }
                            else
                                return '.31em';
                        })
                        .on('click', function(d, i) {
                            d3.event.stopPropagation();
                            //restore stroke with default color.
                            circle.attr("stroke", circleStroke);
                            text.attr("stroke", 'none');

                            if(d.source && that.data['raw'][d.source.name]){
                                d3.select(this).attr('stroke', '#44B78B');
                                app.curtain('default', true, 'Models.Relation', {
                                    data: {
                                        mkey: '',
                                        hdr: relationTitleMap[d.type],
                                        items: [{
                                            first: {
                                                full_name: d.source.name,
                                                name: _.last(d.source.name.split('.')),
                                            },
                                            second: {
                                                full_name: d.target.name,
                                                name: _.last(d.target.name.split('.')),
                                            },
                                        }],
                                    }
                                });
                            }
                        });
                        // .text(function(d) {
                        //     if (d.source) {
                        //         var rel = '';
                        //         if (d.source.name === d.target.name) {
                        //             rel = relationTitle[d.type].slice(-3);
                        //         } else {
                        //             rel = relationTitle[d.type];
                        //         }
                        //         return rel;
                        //     } else {
                        //         return d.vname;
                        //     }
                        // });
                    //close curtain and restore stroke
                    svg.on('click', function(d, i) {
                            app.curtain('default', false);
                            circle.attr("stroke", circleStroke);
                            text.attr("stroke", 'none');
                    });

                    function tick() {
                        path.attr("d", linkArc);
                        circle.attr("transform", transformCircle);
                        text.attr("transform", transformText);
                        text.text(function(d){
                            if(d.source){
                                var rel = '';
                                if (d.source.name === d.target.name) {
                                    rel = relationTitle[d.type].slice(-3);
                                } else {
                                    rel = relationTitle[d.type];
                                }
                                if (d.target.x < d.source.x && d.type === 'many_to_one') {
                                    return '1 : m';
                                }
                                return rel;
                            } else {
                                return d.vname;
                            }
                        });
                    }

                    function linkArc(d) {
                        var dx = d.target.x - d.source.x,
                            dy = d.target.y - d.source.y,
                            k = "M" + d.source.x + "," + d.source.y + d.target.x + "," + d.target.y,
                            dr = Math.sqrt(dx * dx + dy * dy);
                        if (d.source.name === d.target.name) {
                            // d.source.x is exactly the center
                            var x = d.source.x, y = d.source.y - r;

                            return "M" + x + "," + y + "A" + r + "," + r + " 0 1,1 " + (x - r) + "," + (d.target.y);
                        } else {
                            if(linkPaths[d.source.name + d.target.name].archOrder === 0){
                                return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + (d.target.x - 0) + "," + d.target.y;
                            }else if(linkPaths[d.source.name + d.target.name].archOrder === 1){
                                return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + (d.target.x + 0) + "," + d.target.y;
                            }else{
                                return "M" + d.source.x + "," + d.source.y + "L" + d.target.x + "," + d.target.y;
                            }
                        }
                    }

                    function transformText(v) {
                        var d;
                        if(v.source){
                            d = v;
                        }else{
                            if(_.isEmpty(nodePaths)){
                                d = v;
                                return "translate(" + d.x + "," + d.y + ")";
                            }else{
                                var target = function(){
                                    return _.min(nodePaths[v.name].peers, function(o){
                                       return  nodePaths[o].degree;
                                    });
                                }();
                                d = _.extend({}, v, {source: nodePaths[v.name].self, target: nodePaths[target].self, isNode: true});
                            }
                        }
                        if (!d.isNode) {
                            var xx = (d.source.x + d.target.x) / 2,
                                yy = (d.source.y + d.target.y) / 2,
                                deg = 0;
                            if(d.source.name === d.target.name)
                                return "translate(" + xx + "," + yy + ") ";

                            if (d.target.x > d.source.x) {
                                if (d.target.y > d.source.y) {
                                    // from left top to right bottom
                                    // console.log("from left top to right bottom");
                                    deg = Math.atan2(d.target.y - d.source.y, d.target.x - d.source.x);
                                    deg = (deg) * (180 / Math.PI);
                                } else {
                                    // from left bottom to right top
                                    // console.log("from left bottom to right top");
                                    deg = Math.atan2(d.source.y - d.target.y, d.target.x - d.source.x);
                                    deg = 0 - (deg) * (180 / Math.PI);
                                }
                            } else {
                                if (d.target.y > d.source.y) {
                                    // from right top to left bottom
                                    // console.log('from right top to left bottom');
                                    deg = Math.atan2(d.target.y - d.source.y, d.source.x - d.target.x);
                                    deg = 0 - (deg) * (180 / Math.PI);
                                } else {
                                    // from right bottom to left top
                                    // console.log('from right bottom to left top');
                                    deg = Math.atan2(d.source.y - d.target.y, d.source.x - d.target.x);
                                    deg = (deg) * (180 / Math.PI);
                                }
                            }
                            return "translate(" + xx + "," + yy + ") " + "rotate(" + deg + ")";
                        } else {
                            var node = d3.select('text#' + d.name.split('.').join('_')).node(),
                            textLen = node ? node.getComputedTextLength() : 0;
                            var xx = (d.source.x + d.target.x) / 2,
                                yy = (d.source.y + d.target.y) / 2,
                                deg = 0;
                            if (d.target.x > d.source.x) {
                                if (d.target.y > d.source.y) {
                                    // from left top to right bottom
                                    // console.log("from left top to right bottom");
                                    deg = Math.atan2(d.target.y - d.source.y, d.target.x - d.source.x);
                                    deg = -(180 - (deg) * (180 / Math.PI));
                                } else {
                                    // from left bottom to right top
                                    // console.log("from left bottom to right top");
                                    deg = Math.atan2(d.source.y - d.target.y, d.target.x - d.source.x);
                                    deg = (180 - (deg) * (180 / Math.PI));
                                }
                            } else {
                                if (d.target.y > d.source.y) {
                                    // from right top to left bottom
                                    // console.log('from right top to left bottom');
                                    deg = Math.atan2(d.target.y - d.source.y, d.source.x - d.target.x);
                                    deg = -(deg) * (180 / Math.PI);
                                } else {
                                    // from right bottom to left top
                                    // console.log('from right bottom to left top');
                                    deg = Math.atan2(d.source.y - d.target.y, d.source.x - d.target.x);
                                    deg = (deg) * (180 / Math.PI);
                                }
                            }
                            if(textLen && ((deg < 0 && -deg > 90) || (deg > 90))){
                                return "translate(" + d.x + "," + d.y + ") " + "rotate(" + deg + ") " + "rotate(180, " + (23 + textLen/2) + ", 0)";
                            }
                            return "translate(" + d.x + "," + d.y + ") " + "rotate(" + deg + ")";
                        }
                    }
                    function transformCircle(d) {
                        return "translate(" + d.x + "," + d.y + ")";
                    }
                }).fail(function(data, textStatus, jqXHR) {
                });

            },
        },
        initialize: function() {
            this.ready = false;
            this.cur = this.data ? this.data.app || '' : '';
            this.baseUrl = 'Models/Models.Display/';
            app.navigate(this.baseUrl + this.cur);

        },
        onBeforeNavigateTo: function(subpath) {
            // console.log(subpath);
            if (!this.ready && subpath) {
                this.cur = subpath;
                app.navigate(this.baseUrl + this.cur);
            }
        },
        onReady: function() {
        },
        actions: {
        },
    });
})(Application);

;/**
 * Sample VIEW script.
 *
 * @author Stagejs.CLI
 * @created Wed Mar 01 2017 16:29:28 GMT-0800 (PST)
 */
;(function(app){

	app.view('Models.MenuCt', {

		template: '<div region="apps"></div>',
		// template: '@view/models/menu.html',
		//data: 'url', {} or [],
		//coop: ['e', 'e'],
		//[editors]: {...},
		
		initialize: function(){
		},
		onReady: function(){
			var that = this;
			app.remote({
			    url: '/express/apps/',
			}).then(function(data){
				that.show('apps', 'Models.Menu', 
					{
						data: {
							apps: data.payload
						}
					}
				);
			});
		},
		//onDataRendered: function(){},
		
		actions: {
		//	dosomething: function(){...},
		//	...
		},
		coop:['context-switched', 'navigate-to'],
		onItemActivated: function($item) {
		    app.navigate('Models/' + $item.data('context'));
		    app.coop('breadcrumbs-change', [{href: 'Models', name: app.global.bcsMap['Models']}, {href: $item.data('context'), name: app.global.bcsMap[$item.data('context')]}]);
		    
		},
		onContextSwitched: function($item) {
			if(window.location.hash.startsWith("#navigate/Models")){
				var sub = window.location.hash.slice("#navigate/Models/".length);
				this.$el.find('[data-context="' + sub + '"]').addClass('actived');
			    app.coop('breadcrumbs-change', [{href: 'Models', name: app.global.bcsMap['Models']}, {href: sub, name: app.global.bcsMap[sub]}]);

			}
		},
	});
	app.view('Models.Menu', {

		template: '@view/models/menu.html',
		
		actions: {
			goto: function(self){
				// console.log(self.data('link'));
				app.coop('show-model', self.data('link'))
			},
		},
		initialize: function(){
		},
		onReady: function(){

		},
	});
})(Application);
;/**
 * Sample VIEW script.
 *
 * @author Stagejs.CLI
 * @created Tue Mar 07 2017 17:40:36 GMT-0800 (PST)
 */
;(function(app){

	app.view('Status', {

		template: '@view/status.html',
		//data: 'url', {} or [],
		//coop: ['e', 'e'],
		//[editors]: {...},
		
		initialize: function(){},
		//onShow: function(){},
		//onDataRendered: function(){},
		
		actions: {
		//	submit: function(){...},
		//	dosomething: function(){...},
		//	...
		},

	});

})(Application);
;
        //do not change this script tag's id="" attr and position.
        Application.run(/*deviceready - Cordova*/);
    
;