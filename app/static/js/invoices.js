'use strict';

var yaiaInvoices = angular.module('yaia.invoices', ['ui.router']);

yaiaInvoices.config(['$stateProvider', '$urlRouterProvider', function ($stateProvider, $urlRouterProvider) {
  $stateProvider
    .state('invoices', {url: '/invoices', templateUrl: 'static/views/invoices.html', controller: 'InvoicesCtrl'});
}]);

yaiaInvoices.controller('InvoicesCtrl', ['$scope', function($scope) {
    $scope.todo = 'TODO: invoices will go here';
}]);
