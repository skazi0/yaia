'use strict';

var yaiaCustomers = angular.module('yaia.customers', ['ui.router']);

yaiaCustomers.config(['$stateProvider', '$urlRouterProvider', function ($stateProvider, $urlRouterProvider) {
  $stateProvider
    .state('user.customers', {url: '/customers', templateUrl: 'static/views/partials/customers.html', controller: 'CustomersCtrl'});
}]);

yaiaCustomers.controller('CustomersCtrl', ['$scope', function($scope) {
    $scope.name = 'customers';
}]);
