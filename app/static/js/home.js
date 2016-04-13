'use strict';

var yaiaHome = angular.module('yaia.home', ['ui.router']);

yaiaHome.config(['$stateProvider', '$urlRouterProvider', function ($stateProvider, $urlRouterProvider) {
  $stateProvider
    .state('home', {url: '/home', templateUrl: 'static/views/home.html', controller: 'HomeCtrl'});
}]);

yaiaHome.controller('HomeCtrl', ['$scope', function($scope) {
    $scope.name = 'abc';
}]);
