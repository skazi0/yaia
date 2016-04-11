'use strict';

var yaiaLogin = angular.module('yaia.login', ['ngRoute', 'yaia.header']);

yaiaLogin.config(['$routeProvider', function ($routeProvider) {
  $routeProvider
    .when('/login', {templateUrl: 'static/views/login.html', controller: 'LoginCtrl'});
}]);

yaiaLogin.controller('LoginCtrl', ['$scope', function($scope) {
    $scope.login = 'abclogin';
}]);
