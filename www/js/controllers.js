var app =angular.module('starter.controllers',[])
app.controller("LogCtrl", function($scope, $http, $state,$ionicPopup){
	 $scope.signIn = function($scope){
		 var username = $scope.name;
		 var pWord = $scope.pWord;
		  
		 var urlApi="http://mobileapi-1470711184253.appspot.com/users/login";
		 $http({
				method: 'POST',
				url: urlApi,	
				data:({
					name: username,
					password: pWord 
				}),
				headers: {'Content-Type': "application/x-www-form-urlencoded"}
		}).success(function(response){
			 console.log(response);
			 window.localStorage.setItem("token", response.token );
			 window.localStorage.setItem("pid", response.id);
			 $state.go('list');
		}).error(function(response){
			console.log(status);
			var a = $ionicPopup.alert({
				title: "ERROR!",
				template: "Invalid username or password."});
		});
	 };//end login
	 
	 $scope.register = function($scope){
		 var username = $scope.name;
		 var pWord = $scope.pWord;
		 console.log(username);
		console.log(pWord);
		
		 var urlApi="http://mobileapi-1470711184253.appspot.com/users";
		 $http({
				method: 'POST',
				url: urlApi,	
				data:({
					name: username,
					password: pWord 
				}),
				headers: {'Content-Type': "application/x-www-form-urlencoded"}
		}).success(function(response){
			 console.log(response);
			var a = $ionicPopup.alert({
				title: "Success!",
				template: "User register. Login to use."});
		}).error(function(response){
		 	var a = $ionicPopup.alert({
				title: "ERROR!",
				template: "Username taken."});
		});
	 };//end register
});//end ctrl

app.controller('ListCtrl', function($scope, $http, $state){
	token = window.localStorage.getItem("token");
	pid = window.localStorage.getItem("pid");
	urlApi = 'http://mobileapi-1470711184253.appspot.com/projects/';
	
	
	$http({
			method:"GET",
			url: urlApi+pid,
			params: {token: token}
	}).success(function(response){
		var id = response.project_id;
		var title = response.title;
		$scope.data = id;
		$scope.title = title;
		console.log(id);
		console.log(title);
	});

	
	$scope.deleteProj= function(id, $index){
		console.log(id);
		$http({
			method:"DELETE",
			url: urlApi + id,
			params: {token: token}	
		}).success(function(res){
			console.log('Project'+ id +' deleted');
		});
		$scope.data.splice($index, 1);
	};
	
	$scope.logout = function() {
        window.localStorage.removeItem("username");
        window.localStorage.removeItem("password");
		$state.go('login');
    };
	
}); //end list

app.controller('AddCtrl', function($scope, $http, $ionicPopup){
	var urlApi = 'http://mobileapi-1470711184253.appspot.com/projects';

	$scope.submits=function(){
		var title = $scope.data.title;
		console.log(title);
		var whom = $scope.data.whom;
		console.log(whom);
		var comm= $scope.data.commisioned;
		console.log(comm);
		var desc = $scope.data.descr;
		console.log(desc);
		
		token = window.localStorage.getItem("token");
		pid = window.localStorage.getItem("pid")
				
		$http({
				method: 'POST',
				url: urlApi,	
				data:({
						token: token,
						title: title,
						descr: desc,
						comm: comm,
						whom: whom,
						user: pid}),
				headers: {'Content-Type': "application/x-www-form-urlencoded"}
		}).success(function(res){
			var a = $ionicPopup.alert({
				title: "Success!",
				template: "Project added."
			});
			console.log(res);
			$scope.data={};
			$scope.addForm.$setPristine();
			$scope.addForm.$setUntouched();
		});
	};

});	 //end add

app.controller('ViewCtrl', function($scope, $http, $cordovaLocalNotification, $ionicPopup){
	var urlApi = 'http://mobileapi-1470711184253.appspot.com/projects/';
	var pid = $scope.id;
	console.log(pid);
	$scope.data={};
	
	token = window.localStorage.getItem("token");
	
	$http({
			method:"GET",
			url: urlApi + pid,
			params: {token:token}
	}).success(function(results){
		$scope.data.title = results.title;
		$scope.data.descr = results.description;
		$scope.data.whom = results.whom;
		$scope.data.comm = results.commisioned;	
		console.log(results);
	});
	
	//http://devdactic.com/local-notifications-ionic/
	//http://www.gajotres.net/how-to-use-local-notifications-with-ionic-framework
	$scope.$on("cordovaLocalNotification:added",function(pid,state,json){
			alert("Added notification");
	});
	
	$scope.addNotify=function(){
		var msg = $scope.notify.msg;
		var alarmTime = new Date();
		alarmTime.setMinutes(alarmTime.getMinutes()+1);
		$cordovaLocalNotification.schedule({
			id: pid,
			title: "Craft Keeper",
			text: msg,
			at: alarmTime
		}).then(function(results){
			console.log("Notification set");
			$scope.notify.msg="";
				var a = $ionicPopup.alert({
				title: "Success!",
				template: "Notification added."
			});
		});
	};
	
	
}); //end view

app.controller('EditCtrl', function($scope, $http, $ionicPopup){
	var urlApi = 'http://mobileapi-1470711184253.appspot.com/projects/';
	var pid=$scope.id;
	console.log(pid);
	token = window.localStorage.getItem("token");

	//get edit initial values
	$http({
			method:"GET",
			url: urlApi + pid,
			params:{token: token}
	}).success(function(results){
		$scope.edit = {
						title: results.title,
						descr: results.description,
						whom: results.whom,
						comm: results.commisioned};		
	});	

	//put edit
	$scope.edits=function(){
		var object ={
		title: $scope.edit.title,
		whom: $scope.edit.whom,
		comm:  $scope.edit.comm,
		descr: $scope.edit.descr,
		token: token};
		console.log(object);
		
		$http({
				method: 'PUT',
				url: urlApi+pid,
				params: object,
				header: "Content-Type: application/x-www-form-urlencoded"
			}).success(function(data, status, header, config){
				var a = $ionicPopup.alert({
				title: "Success!",
				template: "Project updated."});
				console.log(data);
				console.log(status);
		}). error(function(data, status, header, config){
				console.log(status);
		});		
	};	
	
}); // end edit
	