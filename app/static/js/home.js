'use strict';

var yaiaHome = angular.module('yaia.home', ['ngRoute', 'yaia.header']);

yaiaHome.config(['$routeProvider', function ($routeProvider) {
  $routeProvider
    .when('/home', {templateUrl: 'static/views/home.html', controller: 'HomeCtrl'});
}]);

yaiaHome.controller('HomeCtrl', ['$scope', function($scope) {
    $scope.name = 'abc';
}]);
