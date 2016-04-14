'use strict';

var yaiaWelcome = angular.module('yaia.welcome', ['ui.router']);

yaiaWelcome.config(['$stateProvider', '$urlRouterProvider', function ($stateProvider, $urlRouterProvider) {
  $stateProvider
    .state('anon.welcome', {url: '/welcome', templateUrl: 'static/views/partials/welcome.html', controller: 'WelcomeCtrl'});
}]);

yaiaWelcome.controller('WelcomeCtrl', ['$scope', function($scope) {
    $scope.name = 'plaese login';
}]);
