'use strict';

var yaiaLogin = angular.module('yaia.login', ['ui.router']);

yaiaLogin.config(['$stateProvider', '$urlRouterProvider', function ($stateProvider, $urlRouterProvider) {
  $stateProvider
    .state('login', {url: '/login', templateUrl: 'static/views/login.html', controller: 'LoginCtrl'});
}]);

yaiaLogin.controller('LoginCtrl', ['$scope', function($scope) {
    $scope.login = 'abclogin';
}]);
