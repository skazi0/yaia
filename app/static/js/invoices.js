'use strict';

var yaiaInvoices = angular.module('yaia.invoices', ['ui.router', 'restangular']);

yaiaInvoices.config(['$stateProvider', '$urlRouterProvider', function ($stateProvider, $urlRouterProvider) {
  $stateProvider
    .state('user.invoices', {url: '/invoices', templateUrl: 'static/views/partials/invoices.html', controller: 'InvoicesCtrl', resolve: { $title: function() { return 'Invoices'; }}});
}]);

yaiaInvoices.controller('InvoicesCtrl', ['$scope', 'Restangular', function($scope, Restangular) {
    Restangular.all('invoices').getList().then(
        function(data) {
            $scope.invoices = data;
        }
    );
}]);
