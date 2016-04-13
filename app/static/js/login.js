'use strict';

var yaiaLogin = angular.module('yaia.login', ['ui.router', 'yaia.auth']);

yaiaLogin.config(['$stateProvider', '$urlRouterProvider', function ($stateProvider, $urlRouterProvider) {
  $stateProvider
    .state('anon.login', {url: '/login', templateUrl: 'static/views/login.html', controller: 'LoginCtrl'});
}]);

yaiaLogin.controller('LoginCtrl', ['$scope', '$state', 'Auth', function($scope, $state, Auth) {
    $scope.signin = function() {
        Auth.login($scope.login, $scope.password, $scope.remember).then(
            function(){
                $state.transitionTo('user.home');
            },
            function(){
                alert('login failed');
            }
        );
    };
}]);
