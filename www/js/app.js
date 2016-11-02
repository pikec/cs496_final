// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
angular.module('starter', ['ionic', 'starter.controllers', 'ngCordova'])

.run(function($ionicPlatform) {
  $ionicPlatform.ready(function() {
    if(window.cordova && window.cordova.plugins.Keyboard) {
      // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
      // for form inputs)
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);

      // Don't remove this line unless you know what you are doing. It stops the viewport
      // from snapping when text inputs are focused. Ionic handles this internally for
      // a much nicer keyboard experience.
      cordova.plugins.Keyboard.disableScroll(true);
    }
    if(window.StatusBar) {
      StatusBar.styleDefault();
    }
	
	$ionicPlatform.registerBackButtonAction(function(e){
	e.preventDefault();
	}, 100);
 });
})

.config(function($stateProvider, $urlRouterProvider){
	$stateProvider
	.state('login', {
		url: '/login',
		templateUrl: 'templates/login.html',
		controller: 'LogCtrl'
	})
	.state('list', {
		url: '/list',
		templateUrl: 'templates/listProjects.html',
		controller: 'ListCtrl'
	})
	.state('add',{
		url:'/add',
		templateUrl: 'templates/addProject.html',
		controller: 'AddCtrl'
	})
	.state('view',{
		url:'/view/:id',
		templateUrl: 'templates/viewProject.html',
		controller: function($scope, $stateParams){
			$scope.id=$stateParams.id;
		}
	})
	.state('edit',{
		url:'/edit/:id',
		templateUrl: 'templates/editProject.html',
		controller: function($scope, $stateParams){
			$scope.id=$stateParams.id;
		}
	});
	
	$urlRouterProvider.otherwise('/login');
})


//http://stackoverflow.com/questions/11442632/how-can-i-post-data-as-form-data-instead-of-a-request-payload/
.config(['$httpProvider', function ($httpProvider) {
  // Intercept POST requests, convert to standard form encoding
  $httpProvider.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
  $httpProvider.defaults.transformRequest.unshift(function (data, headersGetter) {
    var key, result = [];

    if (typeof data === "string")
      return data;

    for (key in data) {
      if (data.hasOwnProperty(key))
        result.push(encodeURIComponent(key) + "=" + encodeURIComponent(data[key]));
    }
    return result.join("&");
  });
}]);