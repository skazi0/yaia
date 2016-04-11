'use strict';

var yaiaInvoices = angular.module('yaia.invoices', ['ngRoute', 'yaia.header']);

yaiaInvoices.config(['$routeProvider', function ($routeProvider) {
  $routeProvider
    .when('/invoices', {templateUrl: 'static/views/invoices.html', controller: 'InvoicesCtrl'});
}]);

yaiaInvoices.controller('InvoicesCtrl', ['$scope', function($scope) {
    $scope.todo = 'TODO: invoices will go here';
}]);
